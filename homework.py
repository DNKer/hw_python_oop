""" FITNess Tracker
Copyright (C) 2022 Authors: Dmitry Korepanov, Yandex practikum
License Free
Version: 1.2. 2022"""

from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Information message about trenning. """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Creation information message about trenning. """
        output_message: str = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')
        return output_message


class Training:
    """Base class of training. """

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOUERS_IN_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """To get a distance in km. """
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """To get average mooving speed. """
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """To get of given up calories. """
        raise NotImplementedError(
            'Define method in %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """To get info message about comtlitting trenning. """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Traning: runnig. """

    CALORIES_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        """To get of given up calories for running. """
        return (
            (
                (self.CALORIES_SPEED_MULTIPLIER * self.get_mean_speed()
                    - self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
            )
            / self.M_IN_KM * (
                self.duration * self.HOUERS_IN_MINUTES
            )
        )


class SportsWalking(Training):
    """Training: walking. """

    WALKING_CALLORIES_MULTIPLIER_1: float = 0.035
    WALKING_CALLORIES_MULTIPLIER_2: float = 0.029
    DEGREE_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """To get of given up calories for SportsWalking. """
        return ((
                self.WALKING_CALLORIES_MULTIPLIER_1
                * self.weight
                + (
                    self.get_mean_speed()
                    ** self.DEGREE_MULTIPLIER
                    // self.height)
                * self.WALKING_CALLORIES_MULTIPLIER_2 * self.weight)
                * (self.duration * self.HOUERS_IN_MINUTES))


class Swimming(Training):
    """Training: swimming. """

    LEN_STEP: float = 1.38   # redef global variable
    SWIMMING_CALLORIES_MULTIPLIER: float = 1.1
    DEGREE_MULTIPLIER: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """To get a mean speed for Swimming. """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """To get of given up calories for Swimming. """
        return ((self.get_mean_speed() + self.SWIMMING_CALLORIES_MULTIPLIER)
                * self.DEGREE_MULTIPLIER * self.weight)


WRONG_WORKOUT = 'Неверный {workout} получили!'
WRONG_DATA = 'В {workout} хотели {expected}! А дали {given} чисел.'
WORKOUTS = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4),
}


def read_package(workout_type: str, data: list) -> Training:
    """To read damp from sensors. """
    if workout_type not in WORKOUTS:
        raise ValueError(WRONG_WORKOUT.format(
            workout=workout_type,
        ))
    class_, expected = WORKOUTS[workout_type]
    if len(data) != expected:
        raise ValueError(WRONG_DATA.format(
            workout=workout_type,
            expected=expected,
            given=len(data),
        ))
    return class_(*data)


def main(training: Training) -> None:
    """Main function. """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
