from rest_framework import views
from rest_framework import permissions
from django.http import JsonResponse


from users.models import StudentInfo

from users.utils.save_in_minio import save_avatar_in_minio


class ProfileView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        student_info = StudentInfo.objects.get(user=request.user)
        return JsonResponse({
            'avatar': student_info.avatar,
            'phone': student_info.phone,
            'mail': student_info.mail,
            'date_birth': student_info.date_birth,
            'responsible_1': {
                'full_name': student_info.responsible_1_fio,
                'phone': student_info.responsible_1_phone,
                'mail': student_info.responsible_1_mail
            },
            'responsible_2': {
                'full_name': student_info.responsible_2_fio,
                'phone': student_info.responsible_2_phone,
                'mail': student_info.responsible_2_mail
            }
        })