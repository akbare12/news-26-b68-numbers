# THE WORLD IN ONE PAGE — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b68-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b68-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world's news of Thursday, 26 November 2026:
50 stories — 3 heroes, 10 cards, 37 also — plus a world map with 12 pins,
a date check, a timeline and a tag legend. The date is Thursday, verified
against the calendar; no story from 25 November is shown as 26 November
news except where it is tagged `[CL]` with its 25 Nov date.

## Heroes

- **Macy's 100th Thanksgiving Parade delayed by storm** — first weather
  postponement ever; gusts to 60 mph; rescheduled Sat 28 Nov, 08:30 ET.
- **IRGC claims 2 tankers hit by mines** — supertanker carrying over 2M
  barrels said ablaze off Khasab; claim unverified.
- **Trump tariffs: markets rebound** — STOXX +1.6%, MSCI +0.4% as the
  14-partner salvo reads softer than feared.

## Layout (V66)

Masthead, then a two-line date check, then a tall map with a pin index
and the ALSO column on the left, three stacked hero bands and a 2×5 card
grid on the right, a timeline strip and a footer with the tag legend:
`[C]` confirmed · `[R]` reported · `[CL]` claim / 25 Nov event.

## How it is built

`gen.py` (Pillow, build time only) renders `entry.png` at 1024×1024 and
asserts the layout: 50 stories exactly, no duplicated story text, every
tag correct, 12 map pins at real lon/lat positions with clear labels,
and every string measured to fit its column. `main.py` is standard
library only: it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Verification

- `entry.png`: 1024×1024, 217104 bytes
- sha256: `94f3884732ea75a3203284084ad0b87ac1fa117559dbdbd4aaface2b9f6a3db2`
- Stories: 3 heroes + 10 cards + 37 ALSO = 50
- Stdlib-only simulation: `python3 -m venv` without Pillow, run from a
  different working directory into an empty output dir — exit 0, sha matches.
- Layout checks in `gen.py` also pass: 12 pins, 12 labels, no red pixel
  inside any label box, no art line inside any hero label chip.

## License

MIT — see `LICENSE`.
