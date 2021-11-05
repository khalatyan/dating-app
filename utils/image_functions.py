import os
from io import BytesIO

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from PIL import Image


# Функция накладывает водяной знак на фото
def watermark_photo(user_photo, email):
    base_image = Image.open(user_photo)
    width, height = base_image.size
    if width < height:
        base_image = base_image.crop((0, 0, width, width)).resize((500, 500))
    else:
        base_image = base_image.crop((0, 0, height, height)).resize((500, 500))

    watermark_path = os.path.join(settings.STATIC_ROOT, 'img/watermark.png')
    watermark = Image.open(watermark_path).resize((100, 100))

    transparent = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (400, 400), mask=watermark)

    buffer = BytesIO()
    transparent.save(buffer, "PNG")
    image_file = InMemoryUploadedFile(buffer, None, f'{email}.png', 'image/png', buffer.getbuffer().nbytes, None)
    return image_file
