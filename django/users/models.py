from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Test(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    attempts_number = models.IntegerField(null=True, blank=True)
    assessment_method = models.BooleanField()
    shuffle = models.BooleanField()

    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    comment = models.CharField(max_length=250)
    attachment_link = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_right = models.BooleanField()
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

class CourseTopic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title

class Lesson(models.Model):
    topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=300)
    description = models.TextField()
    video_url = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title


class Step(models.Model):
    name = models.CharField(max_length=300, default='')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='steps', default=None)
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='step', blank=True, null=True)
    html = models.OneToOneField(HtmlPage, on_delete=models.CASCADE, related_name='step', blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class StudentsGroup(models.Model):
    title = models.CharField(max_length=300)

    users = models.ManyToManyField(User, blank=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self) -> str:
        return self.title


class StudentInfo(models.Model):
    phone = models.CharField(max_length=100)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )