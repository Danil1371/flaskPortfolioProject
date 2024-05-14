import os
from uuid import uuid4
from io import BytesIO
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image, UnidentifiedImageError, ImageOps


def compress_image(file):
    try:
        file = Image.open(file)
    except UnidentifiedImageError:
        raise BadRequest('not an image')

    size = 1000, 1000
    file.thumbnail(size)
    if file.mode != 'RGB':
        file = file.convert(mode='RGB')
        file.format = 'JPEG'
    file = ImageOps.exif_transpose(file)
    buffer = BytesIO()
    file.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer


def upload_image(image_file, path):
    if not image_file:
        return None

    upload_dir = current_app.config['APP_DIR'] + "/app" + path

    filename = f"{uuid4()}.jpg"  # OR secure_filename(image_file.filename)
    relative_path = path + filename
    filepath = os.path.join(upload_dir, filename)

    image_file = compress_image(image_file)

    image_file.seek(0)
    image_file = Image.open(image_file)
    image_file.save(filepath)

    return relative_path


def delete_image(path):
    if path:
        filepath = current_app.config['APP_DIR'] + "/app" + path
        if os.path.exists(filepath):
            os.remove(filepath)


def get_image(path):
    return current_app.config['BACKEND_URL'] + path if path else None
