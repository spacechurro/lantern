#!/usr/bin/env python3
"""Lantern checks whether a URL is up."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULTS = {"timeout": 5, "color": True}
CONFIG_NAME = "lantern.toml"


def load_config(path: Path | None = None) -> dict:
    """Read the few keys Lantern understands from a TOML-shaped file.

    The file only needs `key = value` lines. `timeout` is a number and
    `color` is `true` or `false`. Blank lines, comments, and other keys
    are ignored.
    """
    path = path or Path(CONFIG_NAME)
    config = dict(DEFAULTS)
    if not path.exists():
        return config
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key == "timeout":
            config["timeout"] = float(value)
        elif key == "color":
            config["color"] = value == "true"
    return config


def check(url: str, timeout: float) -> tuple[bool, int | None]:
    """Return whether the URL is up, and the final HTTP status if there is one.

    Redirects are followed. Status 200-399 is up. Status 400-599 is down.
    A timeout or a connection failure returns no status.
    """
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return True, response.status
    except urllib.error.HTTPError as error:
        return False, error.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return False, None


def format_result(ok: bool, status: int | None, color: bool) -> str:
    label = "up" if ok else "down"
    detail = str(status) if status is not None else "no response"
    text = f"{label} {detail}"
    if not color or not sys.stdout.isatty():
        return text
    code = "32" if ok else "31"
    return f"\033[{code}m{text}\033[0m"


def add_output_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("url", help="address to request, including https://")
    parser.add_argument(
        "--timeout",
        type=float,
        help="seconds to wait (overrides lantern.toml)",
    )
    color = parser.add_mutually_exclusive_group()
    color.add_argument("--color", dest="color", action="store_true")
    color.add_argument("--no-color", dest="color", action="store_false")
    parser.set_defaults(color=None)


def resolve_output(args: argparse.Namespace, config: dict) -> tuple[float, bool]:
    timeout = config["timeout"] if args.timeout is None else args.timeout
    use_color = config["color"] if args.color is None else args.color
    return timeout, use_color


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lantern",
        description="Check whether a URL is up.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    check_parser = sub.add_parser("check", help="check a URL once")
    add_output_flags(check_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config()
    timeout, use_color = resolve_output(args, config)
    ok, status = check(args.url, timeout)
    print(format_result(ok, status, use_color))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
