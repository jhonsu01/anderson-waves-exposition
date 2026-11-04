# Trapped by Chaos

A plain-language exposition of the Anderson model, Simon's Problem 1, and OpenAI's claimed proof that weak disorder leaves waves free in three dimensions and above.

**This is exposition only. It claims no new mathematical result.** All the mathematics is due to the cited authors. The essay and video were prepared with AI assistance (Claude, Anthropic).

- **Problem:** Extended states in the Anderson model in dimension 3, JSP-001035, [MathDB #389103](https://mathdb.com/p/389103/extended-states-in-the-anderson-model-in-dimension-3)
- **Category:** Exposition
- **Author:** @jhonsu777
- **Contact:** 2xrqx82e2@mozmail.com
- **Version:** v1.0, 4 November 2026 (UTC). Not independently reviewed.
- **Video:** <https://youtu.be/M4zTA3CYW_c>

## Status of the result

MathDB lists this problem as open and calls the claim unverified. We know of no independent mathematical review of OpenAI's manuscript. This package explains the claim. It does not vouch for it.

## Contents

| Path | What it is |
| --- | --- |
| `essay/essay_en.pdf` | The essay |
| `essay/essay_en.md` | Essay source |
| `video/anderson_en.mp4` | Narrated video, about 4:19, 1080p (attached to the release, not stored in git) |
| `video/anderson_en.srt` | Subtitles (timing is approximate) |
| `video/video_script.md` | Narration script |
| `checks/anderson_checks.py` | Small numerical simulation used in the essay |
| `verification/` | Logs and scripts from our Lean run |
| `production/` | Scripts that generate the animation, audio and sound effects |
| `NOTICE.md` | Licenses and credits |
| `SHA256SUMS.txt` | File checksums |

## What we ran

On commit `38116e1a` of Yao Xu's `cadamcat/anderson-ac-lean4`, in a Linux container:

- `scripts/verify.sh` completed 9,780 build jobs and reported `verify: OK`.
- `AndersonAC.Blueprint.anderson_challenge` depends only on `propext`, `Classical.choice` and `Quot.sound`.
- `Verification/NonVacuity.lean`, taken from the author's later `main` branch because it is not in that commit, was checked against the compiled code with the same three axioms.
- `leanchecker --fresh` replayed the module `AndersonAC.Blueprint.Main` and everything it depends on through Lean's kernel, from scratch. It took about 20 minutes and exited with code 0, with no errors.
- `checks/anderson_checks.py` runs a small simulation on tiny grids. It illustrates the idea and proves nothing.

## What we did not check

- We read the introduction and the plan of OpenAI's manuscript, not all of its pages. We did not verify the written proof.
- We did not run Comparator on this project, because it has no Comparator configuration.
- Whether the Lean statement faithfully matches Simon's question. We read it and give our reading, which is not an expert certification.
- We did not reread the classical papers line by line.
- This exposition has not been independently reviewed.

## Reproducing

```bash
python checks/anderson_checks.py
```

The scripts in `production/` and `verification/` contain absolute paths from the original machine and need editing to run elsewhere.
