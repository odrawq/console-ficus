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
        print("Фатальная ошибка: не найден файл конфигурации")
        return

    executor = Executor(config)

    try:
        while True:
            executor.exec(input(">>> "))

    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
