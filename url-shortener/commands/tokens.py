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
