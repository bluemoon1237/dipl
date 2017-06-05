from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from TuesQuestionnaireApp.models import Attempt, Assignment
from TuesQuestionnaireApp.utils import user_is_student, user_is_teacher
import random
import datetime


def start_attempt(request, assignment_id):
    if user_is_student(request.user):
        chosen_assignment = get_object_or_404(Assignment, pk=assignment_id)

        if chosen_assignment.due_date < timezone.now():
            return HttpResponse('Forbidden', status=403)

        seed = random.randint(0, 100000)
        attempt = chosen_assignment.get_curr_user_attempt(request.user)

        if attempt is None:
            attempt = Attempt(assignment=chosen_assignment,
                              start_time=timezone.now(),
                              user=request.user,
                              random_seed=seed,
                              end_time=timezone.now() + datetime.timedelta(minutes=chosen_assignment.time_limit))
            attempt.save()
        elif not attempt.check_time():
            return redirect('finish_attempt', attempt_id=attempt.id)

        curr_question = 1
        question = attempt.get_question(curr_question)

        context = {'attempt': attempt,
                   'question': question,
                   'assignment': chosen_assignment,
                   'curr_question': curr_question,
                   'marked_answers': attempt.get_marked_answers(question.id)}

        return render(request, 'TuesQuestionnaire/attempts/attempt.html', context)


def submit_answers(request):
    if request.method == 'POST' and user_is_student(request.user):
        attempt = get_object_or_404(Attempt, pk=int(request.POST['attempt_id']))
        if attempt.user == request.user:
            if not attempt.check_time():
                url = reverse('finish_attempt', kwargs={'attempt_id':attempt.id})
                response = {
                    'status': 2,  # redirect
                    'url': url
                }
                return JsonResponse(response)

            if request.POST.get('answers[]'):
                converted_answers = [int(a) for a in request.POST.getlist('answers[]')]
                question_id = int(request.POST['question_id'])
                attempt.update_answers(question_id, converted_answers)

            new_question_numb = int(request.POST['newQuestion'])
            new_question = attempt.get_question(new_question_numb)
            marked_answers = attempt.get_marked_answers(new_question.id)
            context = {
                'question': new_question,
                'curr_question': new_question_numb,
                'question_count': attempt.assignment.get_questions_count(),
                'marked_answers': marked_answers
            }
            data = render_to_string('TuesQuestionnaire/attempts/attempt-question.html', context)

            response = {
                'status': 1,  # OK
                'data': data
            }

            return JsonResponse(response)

    return HttpResponse('Unauthorized', status=401)


def finish_attempt(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    attempt.finish()
    context = {
        'attempt_id': attempt_id
    }

    return render(request, 'TuesQuestionnaire/attempts/finish.html', context)


def results(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    if (user_is_student(request.user) and attempt.user == request.user) or user_is_teacher(request.user):
        context = {
            'result_view': attempt.get_result()
        }

        return render(request, 'TuesQuestionnaire/attempts/results.html', context)

    return HttpResponse('Unauthorized', status=401)
