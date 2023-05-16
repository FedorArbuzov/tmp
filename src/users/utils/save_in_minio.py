import random
import string


from minio import Minio
from minio.error import S3Error

def generate_random_name(n=5):
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
    new_file_name = generate_random_name() + file_extension
    # Upload a file to the bucket
    try:
        res = client.fput_object(
            "mybucket",
            new_file_name,
            base64_file,
            f"image/{file_extension}"
        )
        return 'http://px-dev-s3.platonics.ru:9000/mybucket/' + new_file_name
    except S3Error as e:
        return None
