from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Course, Topic, Lesson

class Command(BaseCommand):
    help = 'Create test data for the Course, Topic and Lesson models'

    def handle(self, *args, **kwargs):
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

        topic2 = Topic.objects.create(
            course=course,
            title='Functions and Loops',
            description='Learn how to use functions and loops in Python',
            image='https://example.com/functions-loops.jpg',
        )

        # Create some lessons for each topic
        lesson1 = Lesson.objects.create(
            topic=topic1,
            title='Introduction to Python',
            description='Learn about Python and the Python interpreter',
            video_url='https://example.com/intro-to-python.mp4',
        )

        lesson2 = Lesson.objects.create(
            topic=topic1,
            title='Variables and Data Types',
            description='Learn how to use variables and data types in Python',
            video_url='https://example.com/variables-data-types.mp4',
        )

        lesson3 = Lesson.objects.create(
            topic=topic2,
            title='Functions',
            description='Learn how to define and use functions in Python',
            video_url='https://example.com/functions.mp4',
        )

        lesson4 = Lesson.objects.create(
            topic=topic2,
            title='Loops',
            description='Learn how to use loops in Python',
            video_url='https://example.com/loops.mp4',
        )

        # Print success message
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
