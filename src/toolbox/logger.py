import sys
from collections.abc import Generator
from contextlib import contextmanager
from time import sleep

from rich.console import Console
from rich.status import Status

console = Console()
error_console = Console(stderr=True)


class Spinner:
    _status: Status

    def __init__(self, status: Status) -> None:
        self._status = status

    def update(self, message: str) -> None:
        self._status.update(message)


class Logger:
    @staticmethod
    def info(message: str) -> None:
        console.print(f"  {message}")

    @staticmethod
    def success(message: str) -> None:
        console.print(f"[green]✔[/green] {message}")

    @staticmethod
    def warning(message: str) -> None:
        console.print(f"[yellow]⚠[/yellow] {message}")

    @staticmethod
    def error(message: str, file=sys.stderr) -> None:
        if file is sys.stderr:
            error_console.print(f"[red]✘[/red] {message}")
        else:
            console.print(f"[red]✘[/red] {message}")

    @staticmethod
    def command(message: str) -> None:
        console.print(f"[dim]$ {message}[/dim]")

    @staticmethod
    @contextmanager
    def spinner(message: str) -> Generator[Spinner]:
        with console.status(
            message,
            spinner="dots",
            spinner_style="cyan",
        ) as status:
            yield Spinner(status)


logger = Logger()


if __name__ == "__main__":
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.command("command")
    with logger.spinner("Working...") as spinner:
        sleep(2)
        spinner.update("Installing dependencies...")
        sleep(3)
    logger.success("Done in 5s.")
