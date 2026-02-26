from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        price=1500,
        user_id=user_id,
        room_id=room_id,
        date_to=date(year=2026, month=2, day=25),
        date_from=date(year=2026, month=2, day=28),
    )
    booking = await db.bookings.add(booking_data)

    booking_db_data = await db.bookings.get_one_or_none(id=booking.id)

    assert booking_db_data
    assert booking_db_data.id == booking.id
    assert booking_db_data.user_id == user_id
    assert booking_db_data.room_id == room_id

    booking_data_to_update = BookingAdd(
        price=2300,
        user_id=user_id,
        room_id=room_id,
        date_to=date(year=2026, month=2, day=26),
        date_from=date(year=2026, month=2, day=27),
    )

    await db.bookings.edit(booking_data_to_update, id=booking.id)
    booking_db_data_updated = await db.bookings.get_one_or_none(id=booking_db_data.id)
    assert booking_db_data_updated.user_id == user_id
    assert booking_db_data_updated.date_to == booking_data_to_update.date_to

    await db.bookings.delete(id=booking_db_data.id)
    deleted_data = await db.bookings.get_one_or_none(id=booking_db_data.id)

    assert deleted_data is None

    await db.commit()
