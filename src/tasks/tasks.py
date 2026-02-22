from time import sleep
import os
from PIL import Image
from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print('test task finished')

OUTPUT_DIR = "src/static"
os.makedirs(OUTPUT_DIR, exist_ok=True)
INPUT_IMAGE = "input.jpg"

SIZES = [1000, 500, 200]

@celery_instance.task
def resize_and_save_images(
    input_image_path: str,
    output_dir: str = "src/static/images",
    sizes: list[int] = [10000, 100000, 1000],
    quality: int = 85
) -> None:

    os.makedirs(output_dir, exist_ok=True)

    filename, _ = os.path.splitext(os.path.basename(input_image_path))

    with Image.open(input_image_path) as img:
        img = img.convert("RGB")

        for size in sizes:
            resized = img.copy()
            resized.thumbnail((size, size), Image.LANCZOS)

            output_path = os.path.join(
                output_dir,
                f"{filename}_{size}.jpg"
            )

            resized.save(
                output_path,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            print(f"Сохранено: {output_path}")

