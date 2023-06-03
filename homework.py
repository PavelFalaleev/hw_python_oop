class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance , speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
            f'Длительность: {self.duration:.3f} ч.;'
            f'Дистанция: {self.distance:.3f} км;'
            f'Ср. скорость: {self.speed:.3f} км/ч;'
            f'Потрачено ккал: {self.calories:.3f}.')
        # Числовые значения при выводе должны быть 
        # отформатированы до тысячных долей 
        # (до третьего знака после запятой).


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000  
    LEN_STEP = 0.65
    

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration  
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())



class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    M_IN_KM = 1000
    M_IN_H = 60
    

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)


    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        M_IN_KM = 1000
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) 
                           * self.weight / M_IN_KM * self.duration * self.M_IN_H) 
        return spent_calories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    koef1 = 0.035
    koef2 = 0.029
    M_IN_H = 60
    koef_H = 100
    koef_m_s = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.koef1 * self.weight + ((self.get_mean_speed() * self.koef_m_s)**2 / (self.height / self.koef_H)) 
                       * self.koef2 * self.weight) * (self.duration * self.M_IN_H))
        return spent_calories 
    


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM = 1000
    LEN_STEP = 1.38
    Koef_swim_1 = 1.1
    Koef_swim_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool


    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool 
                      / self.M_IN_KM / self.duration)  
        return mean_speed
    
    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() 
                           + self.Koef_swim_1) * self.Koef_swim_2 * 
                           self.weight * self.duration)
        return spent_calories 
    
    # Есть и ещё один параметр, который надо переопределить, 
    # ведь расстояние, преодолеваемое за один гребок, 
    # отличается от длины шага. Значит, необходимо 
    # переопределить атрибут LEN_STEP базового класса.
    
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type = {'SWM':Swimming,
            'RUN':Running,
            'WLK':SportsWalking}  

    if workout_type in type:
        
        if workout_type == 'SWM':
            action, duration, weight, length_pool ,count_pool = data
            return type[workout_type](action, duration, weight, length_pool ,count_pool)
                 
        elif workout_type == 'RUN':
            action, duration, weight, = data
            return type[workout_type](action, duration, weight)

        if workout_type == 'WLK':  
            action, duration, weight, height = data
            return type[workout_type](action, duration, weight, height)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

