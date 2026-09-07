import argparse
import re
import string
from pathlib import Path
from typing import cast

import pyperclip

from toolbox.logger import logger

GACHA_HISTORY_URL_PATTERN = re.compile(
    rb"https://aki-gm-resources(?:-oversea)?\.aki-game\.(?:net|com)"
    rb"/aki/gacha/index\.html#/record[^\"\s]*"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    _ = parser.add_argument(
        "--game-path",
        type=Path,
        help="Wuthering Waves Game Path",
    )

    return parser.parse_args()


def find_game_path_from_common_locations() -> Path | None:
    common_paths = [
        Path("Wuthering Waves Game"),
        Path("Wuthering Waves") / "Wuthering Waves Game",
        Path("Games") / "Wuthering Waves Game",
        Path("Games") / "Wuthering Waves" / "Wuthering Waves Game",
    ]

    for drive_letter in string.ascii_uppercase:
        drive = Path(f"{drive_letter}:/")

        if not drive.exists():
            continue

        for relative_path in common_paths:
            game_path = drive / relative_path

            if game_path.is_dir():
                logger.info(f"Game path found: {game_path}")
                return game_path

    return None


def get_client_log_path(game_path: Path) -> Path:
    game_path = game_path.expanduser().resolve()

    if not game_path.is_dir():
        raise FileNotFoundError(f"Game directory does not exist: {game_path}")

    log_file = game_path / "Client" / "Saved" / "Logs" / "Client.log"

    if not log_file.is_file():
        raise FileNotFoundError(f"Log file does not exist: {log_file}")

    logger.info(f"Log file found: {log_file}")
    return log_file


def decode_client_log(content: bytes) -> bytes:
    """Decode the byte transformation used by recent Client.log files."""
    return bytes(byte ^ (0xA5 if byte & 1 else 0xEF) for byte in content)


def find_latest_gacha_history_url(content: bytes) -> str | None:
    matches = list(GACHA_HISTORY_URL_PATTERN.finditer(content))

    if not matches:
        return None

    return matches[-1].group(0).decode("ascii")


def extract_gacha_history_url(log_file: Path) -> str | None:
    with logger.spinner("Getting extrac gacha history url...") as spinner:
        content = log_file.read_bytes()

        spinner.update("Decoding client log...")
        for candidate in (content, decode_client_log(content)):
            url = find_latest_gacha_history_url(candidate)

            if url is not None:
                return url

    return None


def main() -> int:
    args = parse_args()
    game_path = cast(Path | None, args.game_path)

    if game_path is None:
        game_path = find_game_path_from_common_locations()

    if game_path is None:
        logger.error("Game directory not found")
        return 1

    try:
        log_file = get_client_log_path(game_path)
        url = extract_gacha_history_url(log_file)
    except OSError as error:
        logger.error(str(error))
        return 1

    if url is None:
        logger.error("Gacha history URL not found")
        return 1

    logger.info(f"Gacha url found: {url}")
    pyperclip.copy(url)
    logger.success("Copied to clipboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
