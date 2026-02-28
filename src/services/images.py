import shutil

from src.services.base import BaseService
from src.tasks.tasks import resize_and_save_images
from fastapi import UploadFile

class ImagesService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_and_save_images.delay(image_path)