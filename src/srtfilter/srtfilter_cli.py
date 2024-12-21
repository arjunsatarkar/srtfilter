#!/usr/bin/env python3
import click
import sys
from . import parse
from .filters import rebreak_lines


@click.command()
@click.argument("in_file_path")
@click.option("--filter", "filter_arg", default="")
def main(in_file_path: str, filter_arg: str):
    with open(in_file_path) as f:
        text = f.read()
    srt = parse.SRT.from_str(text)

    for filter_name in filter_arg.split():
        match filter_name:
            case "rebreak_lines":
                filter_module = rebreak_lines
            case unknown:
                raise InvalidFilterError(unknown)
        srt.events = [filter_module.filter(event) for event in srt.events]

    sys.stdout.write(str(srt))


class InvalidFilterError(Exception):
    pass


if __name__ == "__main__":
    main()
