import os
import uuid
import mimetypes
import urllib.parse
from datetime import datetime
import boto3
from botocore.client import Config
import botocore.handlers
from django.conf import settings
from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024   # 2 MB for images
MAX_VIDEO_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB for videos

VIDEO_EXTENSIONS = {'.mp4', '.webm', '.ogg', '.mov', '.mkv', '.avi', '.flv', '.m4v'}


def get_s3_client():
    endpoint = getattr(settings, 'SUPABASE_S3_ENDPOINT', os.getenv('SUPABASE_S3_ENDPOINT'))
    access_key = getattr(settings, 'SUPABASE_S3_ACCESS_KEY', os.getenv('SUPABASE_S3_ACCESS_KEY'))
    secret_key = getattr(settings, 'SUPABASE_S3_SECRET_KEY', os.getenv('SUPABASE_S3_SECRET_KEY'))
    region = getattr(settings, 'SUPABASE_REGION_NAME', os.getenv('SUPABASE_REGION_NAME', 'ap-southeast-1'))

    client = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        config=Config(signature_version='s3v4', s3={'addressing_style': 'path'})
    )
    # Supabase buckets might contain spaces (e.g. 'Photo Gallary', 'Video Gallary').
    # Unregister botocore default strict bucket name validator to allow spaces.
    client.meta.events.unregister('before-parameter-build.s3', botocore.handlers.validate_bucket_name)
    return client


def upload_file_to_supabase(file_obj, folder='photos', bucket_name=None, max_size_bytes=None):
    """
    Uploads a Django UploadedFile or file-like object to Supabase Storage via S3 protocol.
    Enforces size limits: 2 MB for images, 50 MB for videos.
    Returns the public CDN URL of the uploaded object.
    """
    if not file_obj:
        return None

    # Determine original filename & extension
    original_name = getattr(file_obj, 'name', 'file')
    _, ext = os.path.splitext(original_name)
    ext_lower = ext.lower() if ext else ''

    # Determine bucket
    bucket = bucket_name or getattr(settings, 'SUPABASE_STORAGE_BUCKET', os.getenv('SUPABASE_STORAGE_BUCKET', 'Photo Gallary'))
    supabase_url = getattr(settings, 'SUPABASE_URL', os.getenv('SUPABASE_URL', 'https://ynmfshvkhnqclpcaxrae.supabase.co')).rstrip('/')

    # Determine if video
    is_video = (
        ext_lower in VIDEO_EXTENSIONS or
        'video' in folder.lower() or
        (bucket_name and 'video' in bucket_name.lower())
    )

    # Size limit validation
    if max_size_bytes is None:
        max_size_bytes = MAX_VIDEO_SIZE_BYTES if is_video else MAX_IMAGE_SIZE_BYTES

    file_size = getattr(file_obj, 'size', None)
    if file_size and file_size > max_size_bytes:
        limit_mb = int(max_size_bytes / (1024 * 1024))
        size_in_mb = round(file_size / (1024 * 1024), 2)
        media_type = 'ভিডিও' if is_video else 'ছবি'
        raise ValidationError(
            f"{media_type} ফাইলের সাইজ সর্বোচ্চ {limit_mb} MB হতে পারবে। আপনার ফাইলের সাইজ {size_in_mb} MB।"
        )

    # Determine content type
    content_type = getattr(file_obj, 'content_type', None)
    if not content_type:
        content_type, _ = mimetypes.guess_type(original_name)
    if not content_type:
        content_type = 'video/mp4' if is_video else 'image/jpeg'

    if not ext:
        ext = '.mp4' if is_video else '.jpg'

    # Generate a unique path: folder/timestamp_uuid.ext
    now = datetime.now()
    clean_folder = folder.strip('/')
    unique_id = uuid.uuid4().hex[:10]
    filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{unique_id}{ext.lower()}"
    key = f"{clean_folder}/{filename}" if clean_folder else filename

    # Read bytes
    if hasattr(file_obj, 'seek'):
        file_obj.seek(0)
    body = file_obj.read()

    # Double check byte length
    if len(body) > max_size_bytes:
        limit_mb = int(max_size_bytes / (1024 * 1024))
        size_in_mb = round(len(body) / (1024 * 1024), 2)
        media_type = 'ভিডিও' if is_video else 'ছবি'
        raise ValidationError(
            f"{media_type} ফাইলের সাইজ সর্বোচ্চ {limit_mb} MB হতে পারবে। আপনার ফাইলের সাইজ {size_in_mb} MB।"
        )

    client = get_s3_client()
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type
    )

    quoted_bucket = urllib.parse.quote(bucket)
    public_url = f"{supabase_url}/storage/v1/object/public/{quoted_bucket}/{key}"
    return public_url
