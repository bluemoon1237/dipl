from django.contrib import admin
from .models import *

admin.site.site_header = 'TUES Questionnaire'
admin.site.site_title = 'TUES Questionnaire'


class TeacherModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(TeacherModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator=request.user)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super(TeacherModelAdmin, self).save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.creator == request.user or request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.userprofile.is_teacher

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.creator == request.user or request.user.is_superuser


class TeacherInline(admin.TabularInline):
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.creator == request.user or request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.userprofile.is_teacher

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.creator == request.user or request.user.is_superuser


class AnswerInline(TeacherInline):
    model = Answer
    min_num = 2
    extra = 0


class QuestionAdmin(TeacherModelAdmin):
    fieldsets = [
        (None, {'fields': ['body', 'category', 'points']}),
    ]

    inlines = [AnswerInline]


class QuestionInline(TeacherInline):
    model = Template.questions.through
    min_num = 1
    extra = 0
    verbose_name = "question"
    verbose_name_plural = "questions"


class TemplateAdmin(TeacherModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]

    inlines = [QuestionInline]


class CategoryAdmin(TeacherModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]


class CourseAdmin(TeacherModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        # (None, {'fields': ['participants']}),
        ('Dates', {'fields': ['start_date', 'end_date']}),
    ]


class AssignmentAdmin(TeacherModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['template', 'course']}),
        (None, {'fields': ['due_date']}),
        (None, {'fields': ['time_limit', 'allowed_attempts']}),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Template, TemplateAdmin)
