import math


def get_rad_angle(angle: int | float) -> float:
    return math.radians(90 - angle)


def get_cos_angle(angle: float) -> float:
    return math.cos(angle)


def get_sin_angle(angle: float) -> float:
    return math.sin(angle)