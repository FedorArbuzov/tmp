from django.utils import timezone

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date
from users.models import StudentInfo, Course, Lesson, Topic, StudentsGroup, Test, Question, Answer, Step, HtmlPage


def create_test(step):
    test1 = Test.objects.create(title='Test 1', description='Description 1', attempts_number=3, assessment_method=True, shuffle=False, pub_date=timezone.now())

    question1 = Question.objects.create(test=test1, text='Question 1', multiple=False, weight=50, comment='Comment 1', order_number=0, attachment_link='https://example.com/file1.pdf')
    question2 = Question.objects.create(test=test1, text='Question 2', multiple=True, weight=50, comment='Comment 2', order_number=1)

    answer1 = Answer.objects.create(question=question1, text='Answer 1', weight=40, order_number=0, comment='Comment 1')
    answer2 = Answer.objects.create(question=question1, text='Answer 2', weight=-50, order_number=1, comment='Comment 2')
    answer3 = Answer.objects.create(question=question1, text='Answer 3', weight=60, order_number=2, comment='Comment 3')
    answer4 = Answer.objects.create(question=question1, text='Answer 4', weight=-50, order_number=3, comment='Comment 4')

    answer5 = Answer.objects.create(question=question2, text='Answer 5', weight=30, order_number=0, comment='Comment 1')
    answer6 = Answer.objects.create(question=question2, text='Answer 6', weight=-20, order_number=1, comment='Comment 2')
    answer7 = Answer.objects.create(question=question2, text='Answer 7', weight=70, order_number=2, comment='Comment 3')
    answer8 = Answer.objects.create(question=question2, text='Answer 8', weight=-80, order_number=3, comment='Comment 4')

    step.test = test1
    step.save()


def create_html(step):
    html = HtmlPage.objects.create(title='Intro python', description='Intro python', content='<p>intro python</p>')
    step.html = html
    step.save()


def create_content_for_topic(topic):
    # Create some lessons for each topic
    lesson1 = Lesson.objects.create(
        topic=topic,
        order_number=0,
        title='Introduction to Python',
        description='Learn about Python and the Python interpreter',
        video_url='https://example.com/intro-to-python.mp4',
    )

    step1 = Step.objects.create(title='Declaring variables 1', lesson=lesson1, order_number=0)
    create_html(step1)


    step2 = Step.objects.create(title='Declaring variables 2', lesson=lesson1, order_number=1)
    create_html(step2)

    step3 = Step.objects.create(title='Declaring variables 3', lesson=lesson1, order_number=2)
    create_test(step3)

    lesson2 = Lesson.objects.create(
        topic=topic,
        order_number=1,
        title='Variables and Data Types',
        description='Learn how to use variables and data types in Python',
        video_url='https://example.com/variables-data-types.mp4',
    )

    step4 = Step.objects.create(title='Declaring variables 1', lesson=lesson2, order_number=0)
    create_html(step4)


    step5 = Step.objects.create(title='Declaring variables 2', lesson=lesson2, order_number=1)
    create_test(step5)


class Command(BaseCommand):
    help = 'Создает несколько тестовых экземпляров StudentInfo'

    def handle(self, *args, **options):
        # Создаем несколько пользователей
        u = User(username='fedor')
        u.set_password('qwerty')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')
        # Создаем несколько экземпляров StudentInfo
        student1 = StudentInfo.objects.create(
            avatar='http://px-dev-s3.platonics.ru:9000/mybucket/avatar.jpg',
            date_birth=date(2000, 1, 1),
            mail='mail1@example.com',
            responsible_1_fio='Responsible1 FIO',
            responsible_2_fio='Responsible2 FIO',
            responsible_1_phone='111-11-11',
            responsible_2_phone='222-22-22',
            responsible_1_mail='responsible1@example.com',
            responsible_2_mail='responsible2@example.com',
            phone='333-33-33',
            user=user1,
        )
        student2 = StudentInfo.objects.create(
            avatar='http://px-dev-s3.platonics.ru:9000/mybucket/avatar.jpg',
            date_birth=date(2000, 2, 2),
            mail='mail2@example.com',
            responsible_1_fio='Responsible1 FIO',
            responsible_2_fio='Responsible2 FIO',
            responsible_1_phone='111-11-11',
            responsible_2_phone='222-22-22',
            responsible_1_mail='responsible1@example.com',
            responsible_2_mail='responsible2@example.com',
            phone='444-44-44',
            user=user2,
        )

        # Create a new course
        course = Course.objects.create(
            title='Python for Beginners',
            description='Learn Python programming from scratch',
            image='https://example.com/python.jpg',
        )

        # Create some topics for the course
        topic1 = Topic.objects.create(
            course=course,
            title='Python Basics',
            description='Learn the basics of Python programming',
            image='https://example.com/python-basics.jpg',
        )

        create_content_for_topic(topic1)

        topic2 = Topic.objects.create(
            course=course,
            title='Functions and Loops',
            description='Learn how to use functions and loops in Python',
            image='https://example.com/functions-loops.jpg',
        )

        create_content_for_topic(topic2)

        students_group = StudentsGroup.objects.create(
            title='5б',
        )

        students_group.users.add(user1)
        students_group.users.add(user2)
        students_group.courses.add(course)



        # Выводим сообщение о создании экземпляров StudentInfo
        self.stdout.write(self.style.SUCCESS(f'Создано {len([student1, student2])} экземпляров StudentInfo'))