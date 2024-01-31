#!/usr/bin/env python3

"""
This is the main module that allows you to start the program.
The program informs you about your studies by entering commands.
"""

from json import load

from executor import Executor


def main() -> None:
    """Starts the program."""
    try:
        with open("../config/config.json", "r", encoding="utf-8") as file:
            executor = Executor(load(file))

    except FileNotFoundError:
        print("Фатальная ошибка: не найден файл конфигурации")
        return

    try:
        while True:
            executor.exec(input(">>> "))

    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
