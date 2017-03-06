from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from TuesQuestionnaireApp.models import Assignment, Attempt
from TuesQuestionnaireApp.utils import user_is_student, user_is_teacher


def details(request, assignment_id):
    if user_is_student(request.user):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        filtered_attempts = Attempt.objects.filter(assignment_id=assignment.id).filter(user=request.user)
        if request.user.attending_courses.filter(id=assignment.course_id).exists():
            context = {'assignment': assignment,
                       'attempts': filtered_attempts,
                       'ended': assignment.due_date < timezone.now(),
                       'left_attempts': assignment.allowed_attempts - len(filtered_attempts)}
            return render(request, 'TuesQuestionnaire/assignments/details.html', context)

    return redirect(reverse('courses-index'))


def results(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if user_is_teacher(request.user) and request.user == assignment.creator:
        best_only = int(request.GET.get('best_only', '1'))
        if best_only != 0:
            attempts = assignment.get_best_attempts()
        else:
            attempts = assignment.get_attempts()
        context = {
            'attempts': attempts,
            'assignment_name': assignment.name
        }

        return render(request, 'TuesQuestionnaire/assignments/results.html', context)
