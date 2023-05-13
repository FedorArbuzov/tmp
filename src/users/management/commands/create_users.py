from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date
from users.models import StudentInfo

class Command(BaseCommand):
    help = 'Создает несколько тестовых экземпляров StudentInfo'

    def handle(self, *args, **options):
        # Создаем несколько пользователей
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
        # Выводим сообщение о создании экземпляров StudentInfo
        self.stdout.write(self.style.SUCCESS(f'Создано {len([student1, student2])} экземпляров StudentInfo'))