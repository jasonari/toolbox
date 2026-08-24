import argparse
import re
import sys
from pathlib import Path
from typing import cast

from utils.logger import logger

GACHA_HISTORY_URL_PATTERN = re.compile(
    rb"https://aki-gm-resources(?:-oversea)?\.aki-game\.(?:net|com)"
    rb"/aki/gacha/index\.html#/record[^\"\s]*"
)


def decode_client_log(content: bytes) -> bytes:
    """Decode the byte transformation used by recent Client.log files."""
    return bytes(byte ^ (0xA5 if byte & 1 else 0xEF) for byte in content)


def find_latest_gacha_history_url(content: bytes) -> str | None:
    # find matches by finditer
    matches = list(GACHA_HISTORY_URL_PATTERN.finditer(content))

    if not matches:
        return None

    return matches[-1].group(0).decode("ascii")


def extract_gacha_history_url(log_file: Path) -> str | None:
    content = log_file.read_bytes()

    for candidate in (content, decode_client_log(content)):
        url = find_latest_gacha_history_url(candidate)
        if url is not None:
            return url

    return None


# parse arguments to Path
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    _ = parser.add_argument(
        "--game-path",
        type=Path,
        required=True,
        help="Wuthering Waves Game Path",
    )

    return parser.parse_args()


def get_client_log_path(game_path: Path) -> Path:
    game_path = game_path.expanduser().resolve()

    if not game_path.is_dir():
        logger.error(f"Game directory does not exist: {game_path}")
        raise FileNotFoundError(f"Game directory does not exist: {game_path}")

    log_file = game_path / "Client" / "Saved" / "Logs" / "Client.log"

    if not log_file.is_file():
        logger.error(f"Log does not exist: {log_file}")

    return log_file


def main() -> int:
    logger.info("Get Gacha Url")

    args = parse_args()
    game_path = cast(Path, args.game_path)

    try:
        log_file = get_client_log_path(game_path)

    except FileNotFoundError as error:
        print(error)
        return 1

    logger.info(f"Found log file: {log_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
