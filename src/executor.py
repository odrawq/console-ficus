"""This module contains a tool for executing user commands."""

import os
import datetime
from traceback import format_exc


class Executor:
    """Executor for executing user commands."""

    def __init__(self, config: dict) -> None:
        self._config = config
        self._commands = {
            "e": self._exit,
            "exit": self._exit,
            "c": self._clear,
            "clear": self._clear,
            "h": self._help,
            "help": self._help,
            "w": self._week,
            "week": self._week,
            "l": self._lessons,
            "lessons": self._lessons,
            "b": self._bells,
            "bells": self._bells,
            "t": self._time,
            "time": self._time
        }

        print(
            "Console Ficus\n"
            'Напишите "h" или "help" для получения дополнительной информации.'
            "\n         :&@@@@@&#5~"
            "\n          ?@@#!:^?G@@P."
            "\n            ?&@#57~!B@@Y"
            "\n             .J@@@@@@@@@&##B"
            "\n     ^JGB#B5G@&G?!~~!@@J~!!!"
            "\n  .5@@#Y7!?&@&     .?@@P:"
            "\n ?@@J.     .@@.  .B@&5Y#@&^"
            "\nY@&.       G@#  .@@J    ~@@~"
            "\n@@?      ~&@G   5@#      Y@&"
            "\nY@@?~~?G@@#^    G@G      7@@"
            "\n :5#&&#P!.      ~@@:     &@5"
            "\n                 ?@@J:.!&@5!"
            "\n                  .P@@@@#YP"
        )
        self.exec(self._config.get("autoexec", ""))

    def exec(self, commands: str) -> None:
        """Executes commands."""
        for commands in commands.split(";"):
            for command in commands.split("&&"):
                command = command.strip()

                if command:  # Command is not empty.
                    if command in self._commands:  # Command exists.
                        try:
                            self._commands[command]()  # Command execution.

                        except Exception:
                            print(
                                f"{command}: произошла ошибка "
                                "в процессе выполнения команды:\n"
                                f"{format_exc().rstrip()}"
                            )
                            break

                    else:
                        print(f"{command}: команда не найдена")
                        break

    def _exit(self) -> None:
        """Exits the program."""
        raise SystemExit(0)

    def _clear(self) -> None:
        """Clears the console."""
        if os.name == "nt":  # Windows.
            os.system("cls")

        else:  # Non Windows.
            os.system("clear")

    def _help(self) -> None:
        """Prints the program manual."""
        print(
            "Программа информирует об учёбе посредством выполнения команд."
            "\n\nКоманды:\n"
            "e, exit - выйти\n"
            "c, clear - очистить консоль\n"
            "h, help - вывести это руководство\n"
            "w, week - вывести тип текущей недели\n"
            "l, lessons - вывести расписание пар\n"
            "b, bells - вывести расписание звонков\n"
            "t, time - вывести время до начала или конца текущей пары"
            "\n\nОператоры:\n"
            "; - разделить команды\n"
            "&& - разделить команды и прекратить выполнение при ошибке"
        )

    def _week(self) -> None:
        """Prints the current week type."""
        if datetime.datetime.today().isocalendar().week % 2 == 0:
            print("Знаменатель")

        else:
            print("Числитель")

    def _lessons(self) -> None:
        """Prints the lessons schedule."""
        current_weekday = datetime.datetime.today().strftime("%a").lower()
        days = {
            "mon": "Понедельник:",
            "tue": "\nВторник:",
            "wed": "\nСреда:",
            "thu": "\nЧетверг:",
            "fri": "\nПятница:",
            "sat": "\nСуббота:"
        }

        if current_weekday in days:
            days[current_weekday] = days[current_weekday].replace(
                                        ":", " (сегодня):"
                                    )

        for day in days:
            if day in self._config["lessons"]:
                days[day] = days[day].lstrip()  # Removing "\n" from first day.
                break

        for day in days:
            if day in self._config["lessons"]:
                print(days[day])

                for lesson_num, lesson_info in (
                    self._config["lessons"][day].items()
                ):
                    print(f"{lesson_num}: {lesson_info}")

    def _bells(self) -> None:
        """Prints the bells schedule."""
        current_weekday = datetime.datetime.today().weekday()

        if current_weekday < 5:  # Weekdays.
            print("Основное (сегодня):")

        else:
            print("Основное:")

        for bell_num, bell_info in self._config["bells"]["main"].items():
            print(f"{bell_num}: {bell_info['1']}, {bell_info['2']}")

        if current_weekday == 5:  # Saturday.
            print("\nСубботнее (сегодня):")

        else:
            print("\nСубботнее:")

        for bell_num, bell_info in self._config["bells"]["sat"].items():
            print(f"{bell_num}: {bell_info}")

    def _time(self) -> None:
        """Prints the time before the start or end of current lesson."""
        current_datetime = datetime.datetime.today()
        current_weekday = current_datetime.weekday()

        if current_weekday == 6:  # Sunday.
            print("Сегодня не учебный день")
            return

        current_time = current_datetime.time()
        current_td = datetime.timedelta(
            seconds=current_time.second,
            minutes=current_time.minute,
            hours=current_time.hour
        )

        if current_weekday < 5:
            for bell_num, bell_info in self._config["bells"]["main"].items():
                bell_start_td = datetime.timedelta(
                    hours=int(bell_info["1"][:2]),
                    minutes=int(bell_info["1"][3:5])
                )

                if current_td < bell_start_td:  # Non lessons time.
                    print(
                        f"Начало {bell_num} пары через "
                        f"{bell_start_td - current_td}"
                    )
                    return

                bell_end_td = datetime.timedelta(
                    hours=int(bell_info["2"][6:8]),
                    minutes=int(bell_info["2"][9:])
                )

                if current_td < bell_end_td:  # Lessons time.
                    print(
                        f"Конец {bell_num} пары через "
                        f"{bell_end_td - current_td}"
                    )

                    for half_num, half_info in bell_info.items():
                        half_start_td = datetime.timedelta(
                            hours=int(half_info[:2]),
                            minutes=int(half_info[3:5])
                        )

                        if current_td < half_start_td:
                            print(
                                f"Начало {half_num} половины через "
                                f"{half_start_td - current_td}"
                            )
                            return

                        half_end_td = datetime.timedelta(
                            hours=int(half_info[6:8]),
                            minutes=int(half_info[9:])
                        )

                        if current_td < half_end_td < bell_end_td:
                            print(
                                f"Конец {half_num} половины через "
                                f"{half_end_td - current_td}"
                            )
                            return

                    return

        else:
            for bell_num, bell_info in self._config["bells"]["sat"].items():
                bell_start_td = datetime.timedelta(
                    hours=int(bell_info[:2]),
                    minutes=int(bell_info[3:5])
                )

                if current_td < bell_start_td:
                    print(
                        f"Начало {bell_num} пары через "
                        f"{bell_start_td - current_td}"
                    )
                    return

                bell_end_td = datetime.timedelta(
                    hours=int(bell_info[6:8]),
                    minutes=int(bell_info[9:])
                )

                if current_td < bell_end_td:
                    print(
                        f"Конец {bell_num} пары через "
                        f"{bell_end_td - current_td}"
                    )
                    return

        print("Пары закончились")
