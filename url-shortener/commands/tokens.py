from typing import Annotated

import typer
from rich import print
from typer import Typer

from api.v1.short_url.auth.service import redis_tokens_helper

app = Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(help="Проверка токена. Достаточно в качестве аргумента передать сам токен")
def check(
    token: Annotated[
        str,
        typer.Argument(help="Your token."),
    ],
):
    if redis_tokens_helper.token_exists(token):
        print("Token [green]exists[/green]")
    else:
        print("Token [red]doesn't exist[/red]")


@app.command(help="Get tokens")
def list():
    print(redis_tokens_helper.get_tokens())


@app.command(help="Генерация и сохранение TOKEN в базу данных")
def create():
    print(redis_tokens_helper.generate_token_and_save())


@app.command(help="Добавление своего токена в БД")
def add_token(token: str = typer.Argument(help="Ваш токен")):
    redis_tokens_helper.add_token(token=token)
    print(f"{token} добавлен")


@app.command(help="Удаление токена из БД")
def rm(token: str):
    redis_tokens_helper.delete_token(token)
    print(f"{token} deleted")
