#!/usr/bin/env python3
"""
Given an SRT file, remove existing line breaks and reinsert them automatically
at word boundaries so as not to exceed 42 characters per line, trying to keep
lines within a single subtitle event at roughly the same length.

NOTE: Using this script is *generally a bad idea*; like many aspects of
subtitling, placing line breaks benefits from contextual judgement. However,
if an existing subtitle file has no line breaks or far too many, as is the case
sometimes, this is an easy way to improve readability.
"""
import click
import parse_srt
import math
import sys
import typing

# May still be exceeded if there are no word boundaries to wrap at
MAX_LINE_LENGTH = 42


@click.command()
@click.argument("in_file_path")
def main(in_file_path: str):
    with open(in_file_path) as f:
        text = f.read()
    srt = parse_srt.SRT.from_str(text)

    for event in srt.events:
        event.content = rebreak(event.content)

    sys.stdout.write(str(srt))


def rebreak(text: str) -> str:
    get_target_line_num: typing.Callable[[int], int] = lambda length: math.ceil(
        length / MAX_LINE_LENGTH
    )
    text = " ".join(text.split("\n"))
    target_line_num = get_target_line_num(len(text))

    lines: list[str] = []
    for _ in range(target_line_num):
        partition_at = round(len(text) / target_line_num) - 1

        # Move to a word boundary
        steps_backward = 0
        for steps_backward, c in enumerate(text[partition_at::-1]):
            if c.isspace():
                break
        if partition_at - steps_backward != 0:
            partition_at -= steps_backward
        else:
            # Moving the partition backward would give us an empty line, so
            # move forward instead to ensure we always make progress.
            steps_forward = 0
            for steps_forward, c in enumerate(text[partition_at:]):
                if c.isspace():
                    break
            partition_at += steps_forward

        lines.append(text[: partition_at + 1].strip())
        text = text[partition_at + 1 :]
        target_line_num = get_target_line_num(len(text))

    return ("\n".join(lines) if lines else text) + "\n"


if __name__ == "__main__":
    main()
