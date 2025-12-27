# TODO: надо бы разбить на файлы
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from time import sleep

from constants import (
    ACTIVITY_DURATION_IN_MINUTES,
    PROBABILITY_OF_ACTIVITY_CHANGE,
    STEP_LEN_IN_METERS,
)
from database import Session
from models import ActivityTypes, FitnessData
from sqlalchemy import select


def calc_new_coordinates(
    lat: float, lon: float, bearing: float, distance_km: float
) -> tuple[float, float]:
    """
    Формулы взяты с https://www.movable-type.co.uk/scripts/latlong.html#dest-point
    """
    R_earth_km = 6371
    delta = distance_km / R_earth_km

    lat_1_radians = math.radians(lat)
    lon_1_radians = math.radians(lon)

    lat_2_radians = math.asin(
        math.sin(lat_1_radians) * math.cos(delta)
        + math.cos(lat_1_radians) * math.sin(delta) * math.cos(bearing)
    )
    lon_2_radians = lon_1_radians + math.atan2(
        math.sin(bearing) * math.sin(delta) * math.cos(lat_1_radians),
        math.cos(delta) - math.sin(lat_1_radians) * math.sin(lat_2_radians),
    )

    lat_2 = math.degrees(lat_2_radians)
    lon_2 = math.degrees(lon_2_radians)

    return round(lat_2, 6), round(lon_2, 6)


class Activity(StrEnum):
    SLEEPING = "sleeping"
    WALKING = "walking"
    RUNNING = "running"
    STANDING = "standing"


def insert_fitness_data(
    recorded_at: datetime,
    activity: Activity,
    steps: int,
    distance_km: float,
    kilocalories: float,
    lat: float,
    lon: float,
) -> None:
    with Session() as session:
        activity_type_id = session.scalar(
            select(ActivityTypes.id).where(ActivityTypes.type_name == activity)
        )
        if activity_type_id is None:
            raise Exception("activity_id is None")

        fd = FitnessData(
            recorded_at=recorded_at,
            activity_type_id=activity_type_id,
            steps=steps,
            distance_km=distance_km,
            kilocalories=kilocalories,
            lat=lat,
            lon=lon,
        )
        session.add(fd)
        session.commit()


@dataclass
class State:
    # dt: datetime = datetime(year=2025, month=12, day=28, hour=12)
    dt: datetime = datetime.now()
    activity: Activity = Activity.STANDING
    lat: float = 43.034119
    lon: float = 131.887695
    angle: float = 0


def get_new_activity(current_activity: Activity) -> Activity:
    if random.random() <= 1 - PROBABILITY_OF_ACTIVITY_CHANGE:
        return current_activity

    if current_activity == Activity.SLEEPING:
        return Activity.STANDING

    elif current_activity == Activity.STANDING:
        return random.choice([Activity.WALKING, Activity.RUNNING])

    elif current_activity == Activity.WALKING:
        return random.choice([Activity.STANDING, Activity.RUNNING])

    elif current_activity == Activity.RUNNING:
        return random.choice([Activity.WALKING, Activity.STANDING])


def create_state() -> State:
    with Session() as session:
        fd = session.scalar(
            select(FitnessData).order_by(FitnessData.recorded_at.desc()).limit(1)
        )
        if fd is None:
            return State()

        activity_type_name = session.scalar(
            select(ActivityTypes.type_name).where(
                ActivityTypes.id == fd.activity_type_id
            )
        )

        if activity_type_name is None:
            raise Exception("в бд странное activity_type_id")

        if activity_type_name == Activity.RUNNING:
            activity = Activity.RUNNING
        elif activity_type_name == Activity.SLEEPING:
            activity = Activity.SLEEPING
        elif activity_type_name == Activity.STANDING:
            activity = Activity.STANDING
        elif activity_type_name == Activity.WALKING:
            activity = Activity.WALKING
        else:
            raise Exception("неопознанное activity_type_name")

        return State(dt=fd.recorded_at, activity=activity, lat=fd.lat, lon=fd.lon)

    raise Exception("какая-то ошибка с бд")


state = create_state()


def generate():
    global state

    if 7 <= state.dt.hour <= 23:
        state.activity = get_new_activity(state.activity)
    else:
        # TODO: надо доработать отход ко сну
        # сейчас сон сразу же после 23, а пробуждение в какое-то время после 7.
        state.activity = Activity.SLEEPING

    # скорость и килокалории взяты из гугла
    match state.activity:
        case Activity.SLEEPING:
            speed_km_h = 0
            kilocalories_h = random.randint(50, 70)
        case Activity.STANDING:
            speed_km_h = 0
            kilocalories_h = 60
        case Activity.WALKING:
            # TODO: скорость и килокалории должны зависеть друг от друга
            speed_km_h = random.randint(5, 6)
            kilocalories_h = random.randint(300, 400)
        case Activity.RUNNING:
            # TODO: скорость и килокалории должны зависеть друг от друга
            speed_km_h = random.randint(10, 12)
            kilocalories_h = random.randint(600, 800)
        case _:
            raise Exception("Нет нужного Activity в match/case")

    kilocalories = kilocalories_h / 60 * ACTIVITY_DURATION_IN_MINUTES
    distance_km = speed_km_h / 60 * ACTIVITY_DURATION_IN_MINUTES

    rotation_angle = random.randint(-45, 45)
    state.angle += rotation_angle

    new_lat, new_lon = calc_new_coordinates(
        lat=state.lat,
        lon=state.lon,
        bearing=state.angle,
        distance_km=distance_km,
    )

    state.lat = new_lat
    state.lon = new_lon

    state.dt += timedelta(minutes=ACTIVITY_DURATION_IN_MINUTES)

    steps = distance_km * 1000 / STEP_LEN_IN_METERS

    insert_fitness_data(
        recorded_at=state.dt,
        activity=state.activity,
        steps=steps,
        distance_km=distance_km,
        kilocalories=kilocalories,
        lat=state.lat,
        lon=state.lon,
    )

    # print(state, kilocalories, steps)
