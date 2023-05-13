
from minio import Minio
from minio.error import S3Error

# Initialize Minio client
client = Minio(
    "px-dev-s3.platonics.ru:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Create a new bucket
# try:
#     client.make_bucket("my-bucket")
# except S3Error as e:
#     print(e)

# Upload a file to the bucket
try:
    res = client.fput_object(
        "mybucket",
        "avatar.jpg",
        "/home/fedor/Downloads/photo_2020-10-31_00-32-49.jpg",
        "image/jpg"
    )
    print(res)
    print('create file')
except S3Error as e:
    print(e)
