from __future__ import annotations
import dataclasses
import re


@dataclasses.dataclass
class Event:
    start: str
    end: str
    content: str


class SRT:
    def __init__(self):
        self.events: list[Event] = []

    @staticmethod
    def from_str(text: str) -> SRT:
        TIMESTAMP_CAPTURE = r"(\d\d:\d\d:\d\d,\d\d\d)"
        TIMING_REGEX = rf"{TIMESTAMP_CAPTURE} --> {TIMESTAMP_CAPTURE}"

        srt = SRT()
        counter = 1
        events = [event for event in text.split("\n\n") if event.strip()]
        for event_str in events:
            lines = event_str.split("\n")
            counter_str, timing_str, content_lines = lines[0], lines[1], lines[2:]

            if int(counter_str) != counter:
                raise ParseError(
                    f"Invalid counter '{counter_str}'; expected {counter}", event_str
                )
            counter += 1

            match = re.fullmatch(TIMING_REGEX, timing_str)
            if match is None:
                raise ParseError(f"Invalid timing info '{timing_str}'", event_str)

            content = "\n".join(content_lines + [""])

            srt.events.append(Event(match[1], match[2], content))

        return srt

    def __str__(self):
        result = ""
        for counter, event in enumerate(self.events, 1):
            result += f"{counter}\n"
            result += f"{event.start} --> {event.end}\n"
            result += f"{event.content}\n"
        return result


class ParseError(Exception):
    def __init__(self, reason: str, event_str: str):
        super().__init__(f"{reason}\nwhile parsing event:\n{event_str}")
        self.reason = reason
        self.event_str = event_str
