from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
import random
import datetime


class Category(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Question(models.Model):
    creator = models.ForeignKey(User)
    body = models.CharField(max_length=2000)
    points = models.IntegerField(default=0)
    category = models.ForeignKey(Category)

    def is_multiple_choice(self):
        return sum(a.is_correct for a in self.answer_set.all()) > 1

    # def clean(self):
        # if sum(a.is_correct for a in self.answer_set.all()) < 1:
        #     raise ValidationError('Question must have at least one correct answer')

    def __str__(self):
        return self.body


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Template(models.Model):
    creator = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    creator = models.ForeignKey(User, related_name='owned_courses')
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='attending_courses')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date is after end date')

    def __str__(self):
        return self.name


class Assignment(models.Model):
    creator = models.ForeignKey(User, related_name='placed_assignments')
    name = models.CharField(max_length=200)
    template = models.ForeignKey(Template)
    course = models.ForeignKey(Course)
    due_date = models.DateTimeField()
    time_limit = models.IntegerField(default=1, verbose_name="Time limit(in minutes)")
    allowed_attempts = models.IntegerField(default=1)

    def get_max_points(self):
        return sum(q.points for q in self.template.questions.all())

    def get_questions_count(self):
        return len(self.template.questions.all())

    def get_curr_user_attempt(self, user):
        return self.attempt_set.filter(user=user).filter(finished=False).first()

    def get_attempts(self):
        return self.attempt_set.order_by('end_time')

    def get_best_attempts(self):
        users = self.attempt_set.values('user').distinct()
        best = []
        for user in users:
            attempts = self.attempt_set.filter(user_id=user['user'])
            max_attempt = max(attempts, key=lambda i: i.get_score())
            best.append(max_attempt)
        return sorted(best, key=lambda i: i.end_time)

    def clean(self):
        if self.allowed_attempts < 1:
            raise ValidationError('There must at least one allowed attempt')
        if self.time_limit < 1:
            raise ValidationError('Time limit must be at least one minute')
        if self.due_date is None:
            raise ValidationError('Please add due date')
        if self.due_date > self.course.end_date:
            raise ValidationError('Assignment must end before it\'s course\'s end date')
        if self.due_date < self.course.start_date:
            raise ValidationError('You can\'t place an assignment before it\'s course has started')
        if self.due_date < timezone.now():
            raise ValidationError('You can\'t place an assignment in the past')

    def __str__(self):
        return self.name


class ModifiedQuestionVIew:
    def __init__(self, id, body, points, answers, category, multiple):
        self.id = id
        self.body = body
        self.points = points
        self.answers = answers
        self.category = category
        self.multiple = multiple


class ResultView:
    def __init__(self, score, max_score, started_at, took_time, question_results, user, assignment_name):
        self.score = score
        self.max_score = max_score
        self.started_at = started_at
        self.took_time = took_time
        self.question_results = question_results
        self.user = user
        self.assignment_name = assignment_name


class Attempt(models.Model):
    random_seed = models.IntegerField(default=0)
    assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    finished = models.BooleanField(default=False)

    def get_question(self, question_numb):
        random.seed(self.random_seed)
        questions = list(self.assignment.template.questions.all())
        random.shuffle(questions)
        question = questions[question_numb - 1]
        answers = list(question.answer_set.all())
        random.shuffle(answers)
        view_question = ModifiedQuestionVIew(question.id,
                                             question.body,
                                             question.points,
                                             answers,
                                             question.category,
                                             question.is_multiple_choice())
        return view_question

    def update_answers(self, question_id, answers):
        if not self.finished:
            self.answers.filter(real_answer__question__id=question_id).delete()
            for answer in answers:
                attempt_answer = AttemptAnswer(attempt=self, real_answer_id=answer)
                attempt_answer.save()
            return True

        return False

    def get_marked_answers(self, question_id):
        return [a.real_answer_id for a in self.answers.all() if a.real_answer.question_id == question_id]

    def check_time(self):
        if self.end_time < timezone.now():
            self.finished = True
            self.save()
            return False
        return True

    def finish(self):
        if not self.finished:
            if self.check_time():
                self.end_time = timezone.now()
                self.finished = True
                self.save()

    def get_result(self):
        return ResultView(score=self.get_score(),
                          max_score=self.assignment.get_max_points(),
                          started_at=self.start_time,
                          took_time=self.end_time - self.start_time,
                          question_results=self.get_question_results(),
                          user=self.user,
                          assignment_name=self.assignment.name)

    def get_score(self):
        score = 0
        for question in self.assignment.template.questions.all():
            if self.is_answered_correctly(question):
                score += question.points

        return score

    def get_question_results(self):
        return [(q, self.is_answered_correctly(q)) for q in self.assignment.template.questions.all()]

    def is_answered_correctly(self, question):
        correct = True
        answer_ids = [a.real_answer_id for a in self.answers.all()]
        print(answer_ids)
        for answer in question.answer_set.all():
            if answer.is_correct and answer.id not in answer_ids:
                correct = False
                break

        return correct


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, related_name='answers')
    real_answer = models.ForeignKey(Answer)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
