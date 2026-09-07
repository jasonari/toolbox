from collections.abc import Iterator
from contextlib import contextmanager
from time import sleep

from rich.console import Console
from rich.status import Status
from rich.text import Text


class Spinner:
    def __init__(self, status: Status) -> None:
        self._status = status

    def update(self, message: str) -> None:
        self._status.update(message)


class Logger:
    def __init__(self) -> None:
        self._console = Console()
        self._error_console = Console(stderr=True)

    def info(self, message: str) -> None:
        self._console.print(Text(f"  {message}"))

    def success(self, message: str) -> None:
        self._print_icon("✔", message, "green")

    def warning(self, message: str) -> None:
        self._print_icon("⚠", message, "yellow")

    def error(self, message: str) -> None:
        self._print_icon("✘", message, "red", console=self._error_console)

    def command(self, message: str) -> None:
        text = Text("$ ", style="dim")
        text.append(message, style="dim")
        self._console.print(text)

    @contextmanager
    def spinner(self, message: str) -> Iterator[Spinner]:
        with self._console.status(
            message,
            spinner="dots",
            spinner_style="cyan",
        ) as status:
            yield Spinner(status)

    def _print_icon(
        self,
        icon: str,
        message: str,
        style: str,
        *,
        console: Console | None = None,
    ) -> None:
        output = console or self._console

        text = Text()
        text.append(icon, style=style)
        text.append(f" {message}")
        output.print(text)


logger = Logger()


if __name__ == "__main__":
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.command("uv sync")

    with logger.spinner("Working...") as spinner:
        sleep(2)
        spinner.update("Installing dependencies...")
        sleep(2)

    logger.success("Done in 4s.")
