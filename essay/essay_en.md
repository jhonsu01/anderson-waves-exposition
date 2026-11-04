---
title: "Trapped by Chaos"
subtitle: "When can a wave get through a messy world? A plain-language guide to the Anderson model, Simon's Problem 1, and OpenAI's claimed answer"
author: "@jhonsu777 (with AI assistance: Claude, Anthropic)"
date: "Version 1.0, 4 November 2026 (UTC). Exposition only: no new mathematical result is claimed. Not independently reviewed."
---

# Abstract

In 1958 Philip Anderson showed that randomness alone can stop a wave from spreading, with no walls at all. Physicists came to expect that in three dimensions, a weak enough disorder still lets waves through, but proving this on a lattice stayed open for decades. In 2000 Barry Simon listed it as his first problem for the new century. In September 2026, OpenAI released a manuscript claiming a proof, and Yao Xu published a Lean formalization. This essay explains the question to readers with no advanced mathematics, shows a small simulation of our own, reports our rerun of the Lean proof, and says plainly what is still unconfirmed.

# How to read this essay

| Tag | Meaning |
|:--|:----------|
| **[E]** | Established work, from the literature cited below. We did not reread each source line by line. |
| **[P]** | Stated in OpenAI's manuscript. It has no independent review that we know of. |
| **[L]** | Read directly in the Lean source. Reading is not compiling. |
| **[V]** | Output of tools we ran ourselves. Logs are kept with this essay. |
| **[C]** | Our own small simulation, reproducible with `anderson_checks.py`. It illustrates, and it proves nothing. |
| **[M]** | Shown on MathDB when we looked. |

Analogies are teaching aids. All the mathematics is due to the cited authors.

# 1. A wave in a messy world

Picture a long hallway. Shout into it, and the sound travels. Now fill it with random obstacles. You might expect the sound to struggle through more slowly, like a person pushing through a crowd.

Anderson found something stranger. A wave bounces off the obstacles and meets its own echoes. Those echoes can cancel, again and again, until the wave cannot spread at all. It stays trapped near where it started, even though nothing blocks the way. **[E]** This is **Anderson localization**. It helps explain why some disordered materials stop conducting electricity, and it contributed to his Nobel Prize in 1977. **[E]** It has also been observed directly in experiments with matter waves. **[E]**

# 2. The model

Take a grid of sites in $d$ dimensions. Give every site a random "height" $V(x)$, chosen independently and uniformly. A wave $\psi$ hops between neighbours and feels those heights:

$$(H\psi)(x)=\sum_{|y-x|=1}\psi(y)+V(x)\,\psi(x).$$

The size of the randomness is the **disorder**. The whole question is how the waves of $H$ behave:

- **Trapped.** The wave stays in a small region. Mathematicians call this **pure point spectrum**.
- **Free.** The wave spreads out for good. The clean mathematical version is **purely absolutely continuous spectrum**.

These two names are the formal version of "trapped" and "free". The match is a simplification, because spreading out for good is not the same as ordinary diffusion.

# 3. Why dimension matters

A hallway offers one route. A floor offers many. A building offers even more. With more routes, echoes find it harder to cancel. Physicists' scaling theory from 1979 predicts: **[E]**

| Dimension | Expected behaviour |
|:--|:---------|
| 1, a line | Trapped at any disorder. Proved by Kunz and Souillard in 1980. **[E]** |
| 2, a floor | Trapped at any disorder, though only very slowly noticeable when disorder is weak. |
| 3 or more | Weak disorder leaves a range of energies where waves are free. |

We ran a small simulation to see the trend. **[C]** It measures which fraction of the grid a typical state occupies, for states near the middle of the energy range:

| Grid | Weak disorder (width 2) | Strong disorder (width 40) |
|:--|:--|:--|
| Line, 1,000 sites | 3.6 % | 0.13 % |
| Floor, $40\times40$ | 28.6 % | 0.10 % |
| Building, $12\times12\times12$ | 32.9 % | 0.18 % |

On the line we also released a wave and let it run. Without disorder, its width reached about 85 sites; with disorder of width 4, about 5. **[C]**

**Do not read too much into this.** These are tiny grids, and the theorem concerns an infinite one. At this size, the floor looks free even though theory expects localization at much larger scales. The table illustrates the idea, and it proves nothing.

# 4. The question

Strong disorder was understood first. Fröhlich and Spencer, and later Aizenman and Molchanov, proved trapping at strong disorder or at the extreme energies. **[E]** On tree-like graphs, Klein proved that waves stay free under weak disorder. **[E]** Erdős, Salmhofer and Yau showed diffusive behaviour on the lattice for long but finite times, which does not settle the eternal question. **[E]**

The lattice itself remained stuck. In 2000, Barry Simon made it Problem 1 on his list: for dimension three and above, prove that there is a range of energies with purely absolutely continuous spectrum, for suitable small disorder. **[E]**

Why so hard? Every site is random, the grid is infinite, and somewhere there are always rare regions that behave badly. A proof has to control all of them at once, forever.

# 5. OpenAI's claimed proof, in outline

OpenAI's main theorem says: **[P]** for every $d\ge3$ and every sufficiently small disorder $\lambda$, there is a fixed energy interval $I_d$ on which, almost surely, the spectrum is purely absolutely continuous, and the interval lies inside the spectrum. The outline, in plain terms, is:

1. **Work on a finite grid, with a small artificial damping.** The goal is a *certificate*: a set of at least half the sites on which a key quantity stays bounded below as the damping goes to zero.
2. **Reveal the randomness one binary digit at a time.** Each random height is written as a series of random signs. Revealing a sign replaces part of the artificial damping with true randomness.
3. **Keep careful accounts.** Three controls track the state. One of them comes from the Ward identity and acts like an energy budget across space.
4. **Handle failures honestly.** If a local step fails, it is rolled back and that block of sites is marked as pending. Later scales clear small pending groups.
5. **Pass to the true operator.** Spectral averaging turns the certificate into information about the infinite grid, which excludes trapped behaviour on the interval.

The manuscript is explicit about what it does not do: it does not locate the full mobility edge, and it does not settle the separate diffusion question, Simon's Problem 3. **[P]** For $d=3$ the disorder threshold is only shown to exist. **[P]**

We read the introduction and the plan of the proof, not all of its pages. **We did not verify the written proof.**

# 6. What we ran

Yao Xu's repository `cadamcat/anderson-ac-lean4` claims a Lean formalization of this result. **[L]** On commit `38116e1a`, inside a Linux container: **[V]**

- `scripts/verify.sh` completed all 9,780 build jobs and reported `verify: OK`.
- `#print axioms` shows `AndersonAC.Blueprint.anderson_challenge` depends only on `propext`, `Classical.choice` and `Quot.sound`. The same holds for the package theorems it lists.
- Non-vacuity: the file `Verification/NonVacuity.lean` is not in this commit, so we took it from the author's later `main` branch and checked it against the compiled code. It shows that a family of random heights as required does exist, and that the theorem then yields an actual operator and a vector with nonzero spectral weight on the interval. It uses the same three axioms.
- `leanchecker --fresh` replayed the module `AndersonAC.Blueprint.Main` and everything it depends on through Lean's kernel, from scratch. It took about 20 minutes and exited with code 0, with no errors.

**The statement.** We read `AndersonAC/Challenge.lean`. **[L]** It imports only Mathlib, and it says: for every $d\ge3$ there is $\delta>0$ such that for all $a<b$ with $b-a<\delta$ there is a nonempty open interval on which, almost surely, the interval lies in the spectrum, every spectral measure is absolutely continuous, and some vector has nonzero spectral weight. On reading, this seems to match Simon's request in a stronger form. That is our reading, not an expert certification.

**Limits.** The statement file was written by the same project that proved it, so its fidelity needs human review. We did not run Comparator on this project. The author's README says AI assistance was used. **[L]**

# 7. Status, as of this version

- MathDB lists the problem as open, and its progress summary calls the claim unverified. **[M]** When we looked, this problem's page did not show a "Lean verified" mark. **[M]**
- We know of no independent mathematical review of the manuscript.
- If the result holds, it answers the question in Simon's Problem 1 for the uniform model at small disorder. It would not be the whole story of the transition between trapped and free waves.

# 8. The idea in one paragraph

A wave in a messy world can get trapped by its own echoes, with no walls. In a line that always happens. In three dimensions, physicists expect weak disorder to leave waves free, but proving it on an infinite grid resisted for decades. OpenAI claims a proof that reveals the randomness one digit at a time and keeps strict accounts, and a Lean formalization of it compiles on our machine. Experts still have to confirm it. Until they do, this is a striking claim backed by a machine check, not yet settled science.

# References

1. P. W. Anderson. *Absence of diffusion in certain random lattices*, Phys. Rev. 109 (1958).
2. E. Abrahams, P. W. Anderson, D. C. Licciardello, T. V. Ramakrishnan. *Scaling theory of localization*, Phys. Rev. Lett. 42 (1979).
3. H. Kunz, B. Souillard. *Sur le spectre des opérateurs aux différences finies aléatoires*, Comm. Math. Phys. 78 (1980).
4. J. Fröhlich, T. Spencer. *Absence of diffusion in the Anderson tight binding model for large disorder or low energy*, Comm. Math. Phys. 88 (1983).
5. M. Aizenman, S. Molchanov. *Localization at large disorder and at extreme energies*, Comm. Math. Phys. 157 (1993).
6. A. Klein. *Extended states in the Anderson model on the Bethe lattice*, Adv. Math. 133 (1998).
7. B. Simon. *Schrödinger operators in the twenty-first century*, Mathematical Physics 2000.
8. L. Erdős, M. Salmhofer, H.-T. Yau. *Quantum diffusion of the random Schrödinger evolution in the scaling limit*, Acta Math. 200 (2008).
9. J. Billy et al. *Direct observation of Anderson localization of matter waves in a controlled disorder*, Nature 453 (2008).
10. OpenAI. *Absolutely Continuous Spectrum for Weak-Disorder Anderson Models in Dimensions at Least Three*, 2026. <https://github.com/openai/math>
11. Y. Xu. *anderson-ac-lean4*, commit `38116e1a`. <https://github.com/cadamcat/anderson-ac-lean4>
12. MathDB, problem 389103. <https://mathdb.com/p/389103/extended-states-in-the-anderson-model-in-dimension-3>
