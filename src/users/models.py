from django.db import models

from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.


class Test(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    attempts_number = models.IntegerField(null=True, blank=True)
    assessment_method = models.BooleanField()
    shuffle = models.BooleanField()

    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    comment = models.CharField(max_length=250)
    order_number = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    attachment_link = models.CharField(max_length=250)
    multiple = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    order_number = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    comment = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class HtmlPage(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    content = models.TextField()

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    order_number = models.IntegerField(default=None)
    title = models.CharField(max_length=300)
    description = models.TextField()
    video_url = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title


class Step(models.Model):
    title = models.CharField(max_length=300, default='')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='steps', default=None)
    order_number = models.IntegerField(default=0)
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='step', blank=True, null=True)
    html = models.OneToOneField(HtmlPage, on_delete=models.CASCADE, related_name='step', blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class StudentsGroup(models.Model):
    title = models.CharField(max_length=300)

    users = models.ManyToManyField(User, blank=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self) -> str:
        return self.title


class StudentInfo(models.Model):
    avatar = models.CharField(max_length=100, default=None)
    date_birth = models.DateField(default=None)
    mail = models.CharField(max_length=100, default=None)
    responsible_1_fio = models.CharField(max_length=100, default=None)
    responsible_2_fio = models.CharField(max_length=100, default=None)
    responsible_1_phone = models.CharField(max_length=100, default=None)
    responsible_2_phone = models.CharField(max_length=100, default=None)
    responsible_1_mail = models.CharField(max_length=100, default=None)
    responsible_2_mail = models.CharField(max_length=100, default=None)
    
    phone = models.CharField(max_length=100)
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.username


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True, null=True)
    time_spended = models.IntegerField(default=0)
    html = models.ForeignKey(HtmlPage, on_delete=models.CASCADE, blank=True, null=True)
    answers = JSONField(blank=True, null=True)
    total_result = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"