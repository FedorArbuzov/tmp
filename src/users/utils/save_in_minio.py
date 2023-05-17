import io
import base64
import tempfile
import random
import string


from minio import Minio
from minio.error import S3Error

def generate_random_name(n=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def save_avatar_in_minio(base64_file, file_name):

    # Initialize Minio client
    client = Minio(
        "px-dev-s3.platonics.ru:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    file_extension = file_name.split('.')[-1]
    new_file_name = generate_random_name() + '.' + file_extension
    padding_needed = len(base64_file) % 4  # Вычисляем количество символов =, которые нужно добавить
    if padding_needed > 0:
        base64_file += '=' * (4 - padding_needed)  # Добавляем символы = в конец строки
    image_data = base64.b64decode(base64_file)
    temp_file = tempfile.NamedTemporaryFile(suffix='.' + file_extension)
    temp_file.write(image_data)
    temp_file.seek(0)
    print(new_file_name)
    # Upload a file to the bucket
    try:
        res = client.put_object(
            "mybucket",
            new_file_name,
            temp_file,
            len(image_data),
            f"image/{file_extension}"
        )
        return 'http://px-dev-s3.platonics.ru:9000/mybucket/' + new_file_name
    except S3Error as e:
        return None
