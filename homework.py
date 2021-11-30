from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Выводит информацию о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    M_IN_HOUR: ClassVar[int] = 60
    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        return ((Training.COEFF_CALORIE_1 * self.get_mean_speed()
                 - Training.COEFF_CALORIE_2)
                * self.weight
                / Training.M_IN_KM
                * self.duration
                * Training.M_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    NEW_COEFF_CALORIE_1: ClassVar[float] = 0.035
    NEW_COEFF_CALORIE_2: ClassVar[float] = 0.029
    def __init__(
            self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.NEW_COEFF_CALORIE_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.NEW_COEFF_CALORIE_2
                 * self.weight
                 )
                * self.duration
                * Training.M_IN_HOUR
                )


@dataclass
class Swimming(Training):
    length_pool: float
    count_pool: float
    CNT: ClassVar[float] = 1.1
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / Training.M_IN_KM
                / self.duration
                )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.CNT) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    operating_modes = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    redirection = operating_modes.get(workout_type)
    if redirection is None:
        raise
    else:
        return redirection(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    show_info = info.get_message()
    print(show_info)


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
