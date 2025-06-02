import typer
from rich import print

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(
    help="Приветствие пользователя по [green][italic][bold]name[/bold][/italic][/green]"
)
def hello(name: str = typer.Argument(help="Your name.")) -> None:
    print(f"Hello [green][italic][bold]{name}[/bold][/italic][/green]")
