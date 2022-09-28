""" FITNess Tracker
Copyright (C) 2022 Authors: Dmitry Korepanov, Yandex practikum
License Free
Version: 1.0. """


class InfoMessage:
    """Information message about trenning. """
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.traning_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    pass

    def get_message(self) -> str:
        """Creation information message about trenning. """
        outp: str = (
            f'Тип тренировки: {self.traning_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')
        return outp
    pass


class Training:
    """Base class of training. """

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    pass

    def get_distance(self) -> float:
        """To get a distance in km. """
        return (self.action * self.LEN_STEP) / self.M_IN_KM
    pass

    def get_mean_speed(self) -> float:
        """To get average mooving speed. """
        get_dist_var: float = self.get_distance()
        return (get_dist_var / self.duration)
    pass

    def get_spent_calories(self) -> float:
        """To get of given up calories. """
    pass

    def show_training_info(self) -> InfoMessage:
        """To get info message about comtlitting trenning. """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
    pass


class Running(Training):
    """Traning: runnig. """
    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 18
        coeff_calorie_2: float = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight) / self.M_IN_KM * (self.duration * 60)
    pass


class SportsWalking(Training):
    """Training: walking. """
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        return (coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_2) * (self.duration * 60)
    pass


class Swimming(Training):
    """Training: swimming. """
    LEN_STEP: float = 1.38   # redef global variable

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + 1.1) * 2 * self.weight)
    pass


def read_package(workout_type: str, data: list) -> Training:
    """To read damp from sensors. """
    work_typ_dic = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
    }
    return work_typ_dic[workout_type](*data)


pass


def main(training: Training) -> None:
    """Main function. """
    info = training.show_training_info()
    print(info.get_message())


pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
