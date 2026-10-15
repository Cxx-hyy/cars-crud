from app import database
from app.schemas import CarInput


def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)

    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020


def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)

    first = database.create_car(
        database_path,
        CarInput(make="  Mazda  ", model="  MX-5  ", year=2020, color="  Red  "),
    )
    second = database.create_car(
        database_path,
        CarInput(make="  Mazda  ", model="  MX-6  ", year=2021, color="  Green  "),
    )

    car_before = database.get_car(database_path, first.id)
    assert car_before is not None
    assert car_before.model == "MX-5"

    database.delete_car(database_path, first.id)

    car_after = database.get_car(database_path, first.id)
    assert car_after is None

    second_car = database.get_car(database_path, second.id)
    assert second_car is not None
    assert second_car.model == "MX-6"

    cars = database.list_cars(database_path)
    assert len(cars) == 1
    assert cars[0].model == "MX-6"