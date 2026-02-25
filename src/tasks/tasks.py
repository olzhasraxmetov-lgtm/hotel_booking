import asyncio
from time import sleep
import os
from PIL import Image

from src.database import async_session_maker_null_poll
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print('test task finished')

OUTPUT_DIR = "src/static"
os.makedirs(OUTPUT_DIR, exist_ok=True)
INPUT_IMAGE = "input.jpg"

SIZES = [1000, 500, 200]

# @celery_instance.task
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


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        bookings = await db.bookings.get_bookings_today_with_check_in()
        print(bookings)


@celery_instance.task(name="booking_today_check_in")
def send_emails_to_users_with_today_check_in():
    asyncio.run(get_bookings_with_today_checkin_helper())

