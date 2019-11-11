from storages.backends.s3boto3 import S3Boto3Storage

import secret_key


class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = secret_key.key['AWS_STORAGE_MEDIA_BUCKET_NAME']  # media
    AWS_REGION = 'ap-northeast-2'
    custom_domain = AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (AWS_REGION, bucket_name)
    file_overwrite = False