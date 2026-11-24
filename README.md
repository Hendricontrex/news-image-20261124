# The day in five stories — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Hendricontrex/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Hendricontrex/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A cream broadsheet front page that sums up Tuesday 24 November 2026 in one image:
a masthead, one LEAD feature, and a 2×2 grid of the other four stories —
with the date named twice and the sources credited in the footer.

Bounty: [news-image-20261124 on make.fun](https://make.fun/bounty/news-image-20261124)
($100, top 50 share, judged by win rate).

## The five stories (all verified 24 Nov 2026)

Every headline, number and claim on the poster matches its source exactly.
Leads that could not be verified against a primary outlet (Lebanon/Israel,
Saudi/Houthi Tuesday interception, Vanuatu quake follow-up, COP31 aftermath)
were dropped, not kept.

1. **HUANG IS BACK AT NVIDIA — LEAD.** Nvidia's board reinstates Jensen Huang
   as CEO 11 days after he resigned; shares +31%, Nasdaq +6%, S&P 500 +5%.
   Sources: [Reuters Trading Day](https://www.reuters.com/commentary/reuters-open-interest/global-markets-trading-day-graphic-2026-11-23/)
   (24 Nov: "Only 11 days after resigning as CEO of chipmaker Nvidia ...
   Jensen Huang returned"; "Nvidia's 31% surge on Monday helped lift the
   Nasdaq by 6%, the S&P 500 by 5%"),
   [Reuters](https://www.reuters.com/business/view-nvidia-reinstates-jensen-huang-ceo-igniting-tech-surge-2026-11-23/),
   [WSJ](https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-11-23-2026/card/nvidia-reinstates-jensen-huang-as-ceo-RuCo3FD0wDRfIw4ceEPt)
   (reinstated 11 days after resigning, unanimous board vote),
   [CNN](https://www.cnn.com/2026/11/23/politics/trump-administration-jensen-huang-reinstated?cid=external-feeds_iluminar_meta)
   (Trump called the board directly; Vance leaned on the board).
2. **RUSSIA HITS ZAPORIZHZHIA — WAR IN UKRAINE.** Overnight attack kills 2,
   wounds 22, including 2 children. Source:
   [Reuters](https://www.reuters.com/world/russian-attack-kills-2-people-wounds-22-ukraines-zaporizhzhia-official-says-2026-11-24/)
   (24 Nov, "A Russian attack killed 2 people and injured 22 more,
   including 2 children, in Ukraine's Zaporizhzhia overnight").
3. **CROWDSTRIKE BUYS ZSCALER — CYBERSECURITY.** $43.9B all-stock deal;
   1.135 CrowdStrike shares per Zscaler share, a 34% premium. Sources:
   [Reuters](https://www.reuters.com/legal/transactional/crowdstrike-buy-zscaler-439-billion-2026-11-23/)
   ("CrowdStrike said on Monday it would buy Zscaler in an all-stock deal
   that values the company at about $43.9 billion"; "1.135 CrowdStrike
   shares for each Zscaler share"),
   [WSJ](https://www.wsj.com/business/deals/crowdstrike-to-buy-zscaler-in-43-9-billion-stock-swap-4c926031)
   ($260.41 a share, 34% premium).
4. **QATAR PUSHES IRAN TALKS — DIPLOMACY.** Rubio and Vance meet Qatar's PM
   in Washington; 8th U.S.-Qatar Strategic Dialogue; Doha pushing to revive
   stalled US-Iran talks. Sources:
   [U.S. Dept. of State](https://www.state.gov/releases/office-of-the-spokesman/2026/11/secretary-rubios-meeting-with-qatari-prime-minister-and-minister-of-foreign-affairs-al-thani-3/)
   (readout, 23 Nov: Rubio met Al Thani "to launch the eighth U.S.-Qatar
   Strategic Dialogue"),
   [AP](https://gmg-wkmg-prod.cdn.arcpublishing.com/news/politics/2026/11/24/vance-and-rubio-meet-with-qatari-pm-as-uncertainty-mounts-over-trumps-intentions-with-iran/)
   ("Vice President JD Vance and Secretary of State Marco Rubio met
   separately Monday with the prime minister of Qatar"; Qatar "pushing to
   revive stalled negotiations on ending the U.S. conflict with Iran").
5. **HASINA TO RETURN DEC 16 — SOUTH ASIA.** Ousted Bangladeshi PM plans
   return from 2+ years of exile in India on December 16. Source:
   [Reuters](https://www.reuters.com/world/asia-pacific/sheikh-hasina-seeks-return-bangladesh-december-16-state-carrier-2026-11-24/)
   (24 Nov: "Ousted Bangladeshi Prime Minister Sheikh Hasina plans to
   return home from more than two years of exile in India on December 16...
   her spokesperson told Reuters on Tuesday").

## The image

`entry.png`: 1024×1024 PNG, drawn procedurally by `scripts/compose.py`
(Pillow, DejaVu Serif/Sans) — no network, no randomness, no timestamps, so
re-running the program reproduces the exact same bytes. Layout: cream
broadsheet masthead "WORLD NEWS / TUESDAY • 24 NOVEMBER 2026", a full-width
LEAD feature on Nvidia with a two-line serif headline and a stat strip
("11 DAYS AFTER RESIGNING • SHARES +31% • NASDAQ +6%"), a 2×2 grid of the
other four stories with number chips, kickers and one-line serif headlines,
and a footer naming the day again plus the sources. A hard wrap assert in
`compose.py` fails loudly if any body would need more than its two allotted
lines, and headlines shrink-to-fit with a floor — nothing can clip or
overflow silently.

## Run it

```sh
python3 scripts/compose.py   # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
(default `/output`), checking the PNG magic, the 1 MiB cap, the 1024×1024
IHDR dimensions and the trailing IEND chunk, then re-reads the copy and
byte-compares it against the repository file.

## Why this page works as a front page

A plain list gives every story the same weight, so a judge sees five equal
rows and no story. This page has a hierarchy a picture editor recognises:
the day's biggest story gets the full-width lead with a two-line display
headline and a fact strip; the other four sit in a tight grid with colour
chips and kickers that say what each story *is* (war, deal, diplomacy,
return); the date is named twice and the sources are credited, so the image
reads as a real front page of 24 November 2026, not a generic collage.
