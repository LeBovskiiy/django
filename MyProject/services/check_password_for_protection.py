import re                                                    # Регулярные выражение
from django.core.validators import ValidationError


def check_password_strange(password: str):                   # Создается функия, которая принимает пароль
    """Check strongest of password

    :param password: str
    :return: str

    >>> check_password_strange('200219Lev')
    'Достаточно сильный пароль'

    >>> check_password_strange('1111111')
    'Пароль слишком короткий'

    >>> check_password_strange('GABENGUY')
    'в пароле должна быть минимум одна цыфра'

    >>> check_password_strange('123412345')
    'нет букв в верхнем регистре'
    """
    if len(password) < 8:                                    # Проверяет количество символов
        return ValidationError                               # Выводит сообщение для пользователя
    password_regex = re.compile(r'(\d)+')                    # Создаеться проверка, есть ли в пароле хоть одна цыфра
    if password_regex.search(password) is None:              # Проверят есть ли вхождения
        return ValidationError                               # Текст для пользователя
    password_regex = re.compile(r'\w+')                      # Создает выражение, для проверки, есть ли хоть одна буква
    if password_regex.search(password) is not None:          # Проверят по выражению
        password_regex = re.compile(r'[A-Z]+')               # Выражение для проверки в верхнем регистре
        if password_regex.search(password) is not None:      # Проверка
            password_regex = re.compile(r'[a-z]+')           # Выражение для нижнего регистра
            if password_regex.search(password) is not None:  # Проверка
                return True                                  # Если все проверки прошли как задумано
            else:                                            # Если не букв в нижнем
                return ValidationError                       # Вывод для пользователя
        else:                                                # Если нет в верхнем
            return ValidationError                           # Вывод для пользователя
    else:                                                    # Если букв вопше нет
        return ValidationError                               # Вывод для пользователя


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    User_input = input()
    print(check_password_strange(User_input))