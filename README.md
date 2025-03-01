# srtfilter

Parser for SubRip (SRT) subtitle format and framework for utilities that manipulate it.

Install from PyPI: [`srtfilter`](https://pypi.org/project/srtfilter/).

## Usage

### CLI tool

Parse and reproduce an SRT file (output goes to stdout):

`srtfilter input.srt`

Break lines automatically (to handle existing files with poor line breaks):

`srtfilter --filter rebreak_lines input.srt`

More filters can be added in the `src/srtfilter/filters` directory.

If you want to diff an SRT against an edited version, the output will have a lot of noise if an event was inserted or deleted in the middle (changing all the subsequent numbers). To make this easier to handle, use `--output-format diffable_srt`, which omits those numbers altogether. This is not an actual subtitle format and should not be distributed or used in any player.

### Library

```python
import srtfilter.parse as srtparse
import sys

with open("input.srt") as f:
    srt = srtparse.SRT.from_str(f.read())

for event in srt.events:
    # Make every event start and end a second later
    event.start.second += 1
    event.end.second += 1
    # Capitalize all the displayed text
    event.content = event.content.upper()

# SRT.__str__() produces a valid SRT file from the parsed representation
sys.stdout.write(str(srt))
```

## License

MIT License; see `LICENSE.txt`.

## Roadmap

- [x] Parse SRT
- [x] Make CLI tool modular
- [x] Add filter for breaking lines
- [x] Parse timecodes into their numeric components
- [ ] More filters? As and when use-cases emerge
