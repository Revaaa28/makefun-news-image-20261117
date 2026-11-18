# The World in One Day — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Revaaa28/makefun-news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Revaaa28/makefun-news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

**Concept.** One image that sums up the whole of Tuesday 17 November 2026:
a classic newspaper broadsheet front page, "THE WORLD IN ONE DAY", with
the date in red under the masthead and 10 stories in a 1 + 3 + 6
structure. The lead story runs as a hero splash — Ukraine striking the
Kerch bridge for a second day, with Russia answering on Kyiv's river
crossings. Three more stories run as pictured panels — Iran's drone
attack on a US radar in Bahrain, the Netanyahu aides' police-tip row,
and the Houthis closing in on Aden. Six more run in a grid — Japan
scrambling jets, the China–Canada tariff deal, US AI-chip curbs, the
Epstein forensic claim, the Uttarakhand bus disaster, and Britain's
settlement sanctions — plus an "also today" strip (the Gaza aid call and
the Jericho killing).

**Design.** Every story is verified against reporting first published on
17 November 2026 (Reuters, AP, AFP, Al Jazeera, Just Security); claims
are hedged where the reporting hedges ("Tehran says", "reported",
"a TV probe says"). Every letter is rendered by code and every
illustration is drawn with PIL shapes in `compose.py` — no photos, no
copied artwork — so the text is perfectly legible with zero garbling.
Type is kept large on purpose: the masthead, the hero headline and the
panel headlines all still read at 300 px across. `main.py` (Python 3.13,
standard library only) installs the committed `entry.png` into the
output directory; run twice it writes identical bytes.

**Story selection.** The day's most consequential stories, across regions
and fields, not one country's or one beat's:

- *Europe / war:* Ukraine hits the Crimea bridge again; Russia hits Kyiv's crossings.
- *Middle East:* Iran fires drones at a US radar base in Bahrain; Netanyahu aides accused of tipping police before the vote; Houthis close in on Aden; Britain sanctions settlement builders; Western allies press Israel to open Gaza crossings; a settler killing in Jericho.
- *Asia-Pacific:* Japan scrambles jets after suspected Russian planes enter its airspace; Xi and Carney agree deeper tariff cuts.
- *Technology / trade:* the US tightens AI-chip sales to Southeast Asia.
- *United States / law:* a forensic expert says Epstein's death was homicide, not suicide.
- *Asia / disaster:* a bus plunges into a ravine in Uttarakhand.

**How it is made.** `compose.py` draws the broadsheet with PIL
(`entry.png`, 1024×1024, ~117 KB). `main.py` copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
Verify: run `main.py` twice into two directories and compare — the
bytes are identical.

Entry for the make.fun bounty
[news-image-20261117](https://make.fun/bounty/news-image-20261117)
("Sum up 17 November's world news in one image", $250 in prizes).
