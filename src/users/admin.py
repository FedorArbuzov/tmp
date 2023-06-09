from django.contrib import admin

# Register your models here.

from .models import Test, Question, Answer, HtmlPage, Tag, Step, StudentsGroup, StudentInfo, Course, Topic, Lesson, UserAnswer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(HtmlPage)

admin.site.register(Step)
admin.site.register(StudentsGroup)
admin.site.register(StudentInfo)

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lesson)

admin.site.register(UserAnswer)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
