from django.core.management.base import BaseCommand
from users.models import Test, Question, Answer
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create test data'

    def handle(self, *args, **options):
        test1 = Test.objects.create(title='Test 1', description='Description 1', attempts_number=3, assessment_method=True, shuffle=False, pub_date=timezone.now())
        self.stdout.write(self.style.SUCCESS(test1.id))

        question1 = Question.objects.create(test=test1, text='Question 1', weight=50, comment='Comment 1', order_number=1, attachment_link='https://example.com/file1.pdf')
        question2 = Question.objects.create(test=test1, text='Question 2', weight=50, comment='Comment 2', order_number=2, attachment_link='https://example.com/file2.pdf')

        answer1 = Answer.objects.create(question=question1, text='Answer 1', weight=40, order_number=1, comment='Comment 1')
        answer2 = Answer.objects.create(question=question1, text='Answer 2', weight=-50, order_number=2, comment='Comment 2')
        answer3 = Answer.objects.create(question=question1, text='Answer 3', weight=60, order_number=3, comment='Comment 3')
        answer4 = Answer.objects.create(question=question1, text='Answer 4', weight=-50, order_number=4, comment='Comment 4')

        answer5 = Answer.objects.create(question=question1, text='Answer 5', weight=40, order_number=1, comment='Comment 1')
        answer6 = Answer.objects.create(question=question1, text='Answer 6', weight=-50, order_number=2, comment='Comment 2')
        answer7 = Answer.objects.create(question=question1, text='Answer 7', weight=60, order_number=3, comment='Comment 3')
        answer8 = Answer.objects.create(question=question1, text='Answer 8', weight=-50, order_number=4, comment='Comment 4')

        self.stdout.write(self.style.SUCCESS('Successfully created tasks data'))