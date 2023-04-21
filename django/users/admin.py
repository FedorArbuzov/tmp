from django.contrib import admin

# Register your models here.

from .models import Test, Question, Answer, HtmlPage, Tag, Program, Step, StudentsGroup, StudentInfo

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(HtmlPage)

admin.site.register(Program)
admin.site.register(Step)
admin.site.register(StudentsGroup)
admin.site.register(StudentInfo)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
