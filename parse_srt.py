from __future__ import annotations
import dataclasses
import enum
import itertools
import re
from typing import List


@dataclasses.dataclass
class Event:
    start: str | None = None
    end: str | None = None
    content: str | None = None


class SRT:
    def __init__(self):
        self.events: List[Event] = []

    @staticmethod
    def from_str(text: str) -> SRT:
        class ParseState(enum.Enum):
            COUNTER = enum.auto()
            TIMING = enum.auto()
            CONTENT = enum.auto()

        PARSE_STATES = itertools.cycle(iter(ParseState))
        TIMESTAMP_CAPTURE = r"(\d\d:\d\d:\d\d,\d\d\d)"
        TIMING_REGEX = rf"{TIMESTAMP_CAPTURE} --> {TIMESTAMP_CAPTURE}"

        srt = SRT()
        lines = text.split("\n")
        counter = 1
        state = next(PARSE_STATES)
        event = Event()
        for line_num, line in enumerate(lines, 1):
            if not line:
                match state:
                    case ParseState.CONTENT:
                        srt.events.append(event)
                        event = Event()
                        state = next(PARSE_STATES)
                    case ParseState.COUNTER:
                        pass
                    case _:
                        raise ParseError(f"Unexpected blank line (line {line_num})")
                continue
            match state:
                case ParseState.COUNTER:
                    if int(line) == counter:
                        counter += 1
                        state = next(PARSE_STATES)
                    else:
                        raise ParseError(
                            f"Invalid counter, expected {counter} (line {line_num})"
                        )
                case ParseState.TIMING:
                    match = re.fullmatch(TIMING_REGEX, line)
                    if match is None:
                        raise ParseError(f"Invalid timing info (line {line_num})")
                    event.start, event.end = match[1], match[2]
                    state = next(PARSE_STATES)
                case ParseState.CONTENT:
                    event.content = (
                        event.content if event.content is not None else ""
                    ) + f"{line}\n"
        return srt

    def __str__(self):
        result = ""
        for counter, event in enumerate(self.events, 1):
            result += f"{counter}\n"
            result += f"{event.start} --> {event.end}\n"
            result += f"{event.content}\n"
        return result


class ParseError(Exception):
    pass
