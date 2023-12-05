"""
This is the main module that allows you to launch the application.
"""

from json import load

from executor import Executor


def main() -> None:
    """Launches the application."""
    try:
        with open("../config/config.json", "r", encoding="utf-8") as file:
            config = load(file)

    except FileNotFoundError:
        print("Запуск невозможен: не найден файл конфигурации")
        return

    executor = Executor(config)

    while True:
        executor.exec(input(">>> "))


if __name__ == "__main__":
    main()
