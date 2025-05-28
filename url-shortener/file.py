"""
В файле запуска прописываем наверху что ниб одно для запуска скрипта
#! /usr/bin/env -S uv run --script -> если установлен uv глобально
#! /usr/bin/env python -> если активировано виртуальное окружение

"""

import typer

from rich import print

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(
    help="Функция принимает аргумент [bold][green][italic]'name'[/italic][/green][/bold] на вход, но он не обязателен так как значение по дефолту установлено"
)
def func(name: str = typer.Argument(default="Python")) -> None:
    print(
        f"Этот текст из func функции. Аргумент переданный: [bold][red][italic]{name}[/italic][/red][/bold]"
    )


@app.callback()
def callback() -> None:
    """
    Тут описание работы этой утилиты CLI
    """
    pass


if __name__ == "__main__":
    app()
