from django.shortcuts import render, redirect, reverse
from TuesQuestionnaireApp.models import UserProfile


def admin_index(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        if request.user.userprofile.is_teacher:
            return render(request, 'TuesQuestionnaire/teacher/admin-index.html')

    return redirect(reverse('admin:login'))


def index(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        if request.user.userprofile.is_teacher:
            return redirect(reverse('admin_index'))

    return render(request, 'TuesQuestionnaire/index.html')


def choose_role(request):
    if not request.user.is_authenticated or hasattr(request.user, 'userprofile'):
        return redirect(reverse('index'))

    role = int(request.GET.get('role', '-1'))
    if role == 1:
        profile = UserProfile(user=request.user, is_teacher=False)
        profile.save()
    elif role == 2:
        profile = UserProfile(user=request.user, is_teacher=True)
        profile.save()
        request.user.is_staff = True
        request.user.save()
    else:
        return redirect(reverse('index'))

    return redirect(reverse('index'))
