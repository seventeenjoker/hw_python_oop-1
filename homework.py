from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MSG_CONST: str = (
        'Тип тренировки: {0}; '
        'Длительность: {1:.3f} ч.; '
        'Дистанция: {2:.3f} км; '
        'Ср. скорость: {3:.3f} км/ч; '
        'Потрачено ккал: {4:.3f}.'
    )

    def get_message(self):
        """Возвращает строку сообщения."""
        return self.MSG_CONST.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Метод get_spent_calories не использован!")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            ) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_WEIGHT_SHIFT: float = 0.029
    CM_IN_M: int = 100
    KMH_IN_MSEC: float = 0.278

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float,
    ):
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        return (
            self.CALORIES_MEAN_WEIGHT_MULTIPLIER * self.weight + (
                (self.get_mean_speed() * self.KMH_IN_MSEC)**2 / self.height
            ) * self.CALORIES_MEAN_WEIGHT_SHIFT * self.weight
        ) * self.duration * self.MIN_IN_H


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_WEIGHT_MULTIPLIER: int = 2

    """Тренировка: плавание."""
    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
        ) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (
            self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.CALORIES_MEAN_WEIGHT_MULTIPLIER * self.weight * self.duration


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_map: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if not class_map.get(workout_type):
        assert False, f'Неизвестная тренировка: {workout_type}'
    return class_map[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
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
