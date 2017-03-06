from django.shortcuts import render, redirect, reverse, get_object_or_404
from TuesQuestionnaireApp.models import Course
from TuesQuestionnaireApp.utils import user_is_student


def index(request):
    if user_is_student(request.user):
        user_courses = request.user.attending_courses.all()
        user_courses_ids = (request.user.attending_courses.values_list('id', flat=True))
        other_courses = Course.objects.exclude(id__in=user_courses_ids)
        context = {'user_courses': user_courses,
                   'other_courses': other_courses}
        return render(request, 'TuesQuestionnaire/courses/index.html', context)

    return redirect(reverse('index'))


def enroll(request, course_id):
    if user_is_student(request.user):
        course = get_object_or_404(Course, pk=course_id)
        if not request.user.attending_courses.filter(id = course_id).exists():
            request.user.attending_courses.add(course)

    return redirect(reverse('course_index'))


def details(request, course_id):
    if user_is_student(request.user):
        course = get_object_or_404(Course, pk=course_id)
        assignments = course.assignment_set.order_by('due_date')
        if request.user.attending_courses.filter(id = course_id).exists():
            context = {'course': course,
                       'assignments': assignments}
            return render(request, 'TuesQuestionnaire/courses/details.html', context)

    return redirect(reverse('courses-index'))

