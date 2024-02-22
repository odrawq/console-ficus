#!/usr/bin/env python3

"""
This is the main module that allows you to start the program.
The program informs you about your studies by entering commands.
"""

import json

try:
    from executor import Executor

except ModuleNotFoundError:
    print(
        "Фатальная ошибка: "
        'не найден модуль "executor.py"'
    )
    raise SystemExit

except PermissionError:
    print(
        "Фатальная ошибка: "
        'отказано в доступе при попытке импортировать модуль "executor.py"'
    )
    raise SystemExit


def main() -> None:
    """Starts the program."""
    try:
        with open("../config/config.json", "r", encoding="utf-8") as file:
            executor = Executor(json.load(file))

    except FileNotFoundError:
        print(
            "Фатальная ошибка: "
            'не найден файл "config.json"'
        )
        return

    except PermissionError:
        print(
            "Фатальная ошибка: "
            'отказано в доступе при попытке загрузить файл "config.json"'
        )
        return

    except (json.decoder.JSONDecodeError, AttributeError):
        print(
            "Фатальная ошибка: "
            'файл "config.json" содержит некорректные данные'
        )
        return

    try:
        while True:
            executor.exec(input(">>> "))

    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
