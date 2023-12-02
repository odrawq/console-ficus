"""
This module contains a class for executing user commands.
"""

import os
import datetime


class Executor:
    """Executes the user commands."""

    def __init__(self, config: dict) -> None:
        self._config = config

    def exec(self, commands: str) -> None:
        """Executes commands."""
        try:
            for command in commands.split("&&"):
                command = command.strip().split(" ")[0]

                if command:
                    eval(f"self._{command}()")

        except (AttributeError, SyntaxError):
            print(f"{command}: команда не найдена")

    def _exit(self) -> None:
        """Exits the application."""
        raise SystemExit

    def _clear(self) -> None:
        """Clears the console."""
        if os.name == "nt":  # Windows.
            os.system("cls")

        else:  # Non Windows.
            os.system("clear")

    def _help(self) -> None:
        """Prints an application manual."""
        print(
            "&& - логическое \"и\" для объединения команд\n"
            "exit - выйти\n"
            "clear - очистить консоль\n"
            "help - вывести руководство\n"
            "week - вывести тип текущей недели\n"
            "lessons - вывести расписание пар\n"
            "calls - вывести расписание звонков\n"
            "time - вывести время до начала или конца текущей пары"
        )

    def _week(self) -> None:
        """Prints the current week type."""
        if datetime.datetime.today().isocalendar().week % 2 == 0:
            print("Знаменатель")

        else:
            print("Числитель")

    def _lessons(self) -> None:
        """Prints the lessons schedule."""
        days = iter(
            ("Понедельник", "\nВторник", "\nСреда",
             "\nЧетверг", "\nПятница", "\nСуббота")
        )

        for day_info in self._config["lessons"].values():
            print(next(days))

            for lesson_num, lesson_info in day_info.items():
                print(f"{lesson_num}: {lesson_info}")

    def _calls(self) -> None:
        """Prints the calls schedule."""
        print("Основное:")

        for call_num, call_info in self._config["calls"]["main"].items():
            print(f"{call_num}: {call_info['1']} | {call_info['2']}")

        print("\nСубботнее:")

        for call_num, call_info in self._config["calls"]["sat"].items():
            print(f"{call_num}: {call_info}")

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

        if current_weekday < 5:  # Weekdays.
            for call_num, call_info in self._config["calls"]["main"].items():
                call_start_td = datetime.timedelta(
                    hours=int(call_info["1"][:2]),
                    minutes=int(call_info["1"][3:5])
                )
                call_end_td = datetime.timedelta(
                    hours=int(call_info["2"][6:8]),
                    minutes=int(call_info["2"][9:])
                )

                if current_td < call_start_td:  # Non lessons time.
                    print(
                        f"Начало {call_num} пары через "
                        f"{call_start_td - current_td}"
                    )
                    return

                for call_half_num, call_half_info in call_info.items():
                    call_half_start_td = datetime.timedelta(
                        hours=int(call_half_info[:2]),
                        minutes=int(call_half_info[3:5])
                    )
                    call_half_end_td = datetime.timedelta(
                        hours=int(call_half_info[6:8]),
                        minutes=int(call_half_info[9:])
                    )

                    if current_td < call_half_end_td:  # Lessons time.
                        print(
                            f"Конец {call_num} пары через "
                            f"{call_end_td - current_td}"
                        )

                        if call_half_end_td < call_end_td:
                            print(
                                f"Конец {call_half_num} половины через "
                                f"{call_half_end_td - current_td}"
                            )

                        elif current_td < call_half_start_td:
                            print(
                                f"Начало {call_half_num} половины через "
                                f"{call_half_start_td - current_td}"
                            )

                        return

        else:  # Saturday.
            for call_num, call_info in self._config["calls"]["sat"].items():
                call_start_td = datetime.timedelta(
                    hours=int(call_info[:2]),
                    minutes=int(call_info[3:5])
                )
                call_end_td = datetime.timedelta(
                    hours=int(call_info[6:8]),
                    minutes=int(call_info[9:])
                )

                if current_td < call_start_td:
                    print(
                        f"Начало {call_num} пары через "
                        f"{call_start_td - current_td}"
                    )
                    return

                elif current_td < call_end_td:
                    print(
                        f"Конец {call_num} пары через "
                        f"{call_end_td - current_td}"
                    )
                    return

        print("Пары закончились")
