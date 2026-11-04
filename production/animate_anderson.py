"""Renderiza el video de Anderson. Uso: animate_anderson.py <en|es> [--still] [--scene N]

Las ondas de las escenas 1, 2 y 10 son una simulacion real en una linea de 301 sitios.
Ilustran la idea y no demuestran nada. Las demas figuras son esquemas propios.
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "D:/Dev/mathdb-video")
from animate import (BG, BLUE, FPS, GREEN, H, INK, MUTED, ORANGE, PAD, PANEL, RED, W, centered, draw_caption, f_body,
                     f_title, fade, fmt, mix, sentence_cues, text_block, title, wav_seconds, wrap)

BASE = Path("D:/Dev/mathdb-video/anderson")
PROJECT = Path("D:/Dev/docker-phonon/projects/anderson")
WAVE = (56, 189, 248)
TRAP = (250, 204, 21)
BAR = (92, 104, 132)
SEED = 20261104
SIDE = 301
TMAX = 60.0
FRAMES = 240

TEXT = {
    "en": {
        1: {"title": "Trapped by Chaos", "sub": "The Anderson model, for everyone", "free": "Empty hallway: the wave travels", "stuck": "Random heights, no walls: the wave stays"},
        2: {"title": "A real simulation", "clean": "Clean line", "messy": "Random heights", "width": "width", "sites": "sites", "note": "One small run. It illustrates and proves nothing."},
        3: {"title": "More room, more routes", "line": "Line", "floor": "Floor", "building": "Building", "weak": "weak mess", "strong": "strong mess", "what": "Share of the grid a typical wave fills",
            "note": "Tiny grids: this illustrates and proves nothing. For the floor, theory expects trapping at far larger sizes."},
        4: {"title": "Believed, but not proved", "events": [("1958", "Anderson's idea", MUTED), ("1980", "Line: trapped", GREEN), ("1983", "Strong mess: trapped", GREEN), ("2000", "Simon's Problem 1", ORANGE), ("2026", "A claimed proof", RED)], "goal": "3D or more, a little mess: can waves stay free?"},
        5: {"title": "Why it is so hard", "rare": "Somewhere, a rare bad region always exists", "all": "Control them all: at once, at every scale, forever"},
        6: {"title": "The claimed plan", "note": "A cartoon of the plan, not the proof itself", "digits": "1. Reveal the randomness digit by digit", "books": "2. Keep strict accounts", "blocks": "3. A step fails: undo, mark it pending, clean up later", "end": "Result claimed: on a range of energies, waves are free"},
        7: {"title": "What it does not claim", "yes": "Claims: waves free on some energies, for small disorder, 3D and up", "no": ["The exact boundary between trapped and free", "Ordinary diffusion: a separate problem", "How small the disorder must be in 3D"]},
        8: {"title": "Checking it by computer",
            "cards": [("We ran it", "Yao Xu's Lean code built on our machine, with no errors."), ("Axioms", "Only the three standard ones: propext, Classical.choice, Quot.sound."),
                      ("Limit 1", "A computer check does not explain the idea."), ("Limit 2", "People must still confirm that the code asks the original question.")]},
        9: {"title": "Where things stand",
            "cards": [("MathDB", "Lists the problem as open, and the claim as unverified."), ("Review", "We know of no independent review by mathematicians."),
                      ("Us", "We read the introduction and the plan, not every page.")], "bottom": "A striking claim with a machine check. Not yet settled science."},
        10: {"title": "A wave can be trapped by its own echoes", "items": ["All mathematics: the people named in the sources. Explanation made with AI assistance.", "Sources: Anderson; Abrahams et al.; Kunz–Souillard; Simon; OpenAI; Yao Xu."]},
    },
    "es": {
        1: {"title": "Atrapada por el caos", "sub": "El modelo de Anderson, para todo el mundo", "free": "Pasillo vacío: la onda viaja", "stuck": "Alturas al azar, sin paredes: la onda se queda"},
        2: {"title": "Una simulación real", "clean": "Línea limpia", "messy": "Alturas al azar", "width": "anchura", "sites": "sitios", "note": "Una sola prueba pequeña. Ilustra, pero no demuestra nada."},
        3: {"title": "Más espacio, más rutas", "line": "Línea", "floor": "Piso", "building": "Edificio", "weak": "desorden débil", "strong": "desorden fuerte", "what": "Parte de la cuadrícula que ocupa una onda típica",
            "note": "Cuadrículas diminutas: ilustra y no demuestra nada. En el piso, la teoría espera atrapamiento a tamaños mucho mayores."},
        4: {"title": "Se creía, pero no se demostraba", "events": [("1958", "La idea de Anderson", MUTED), ("1980", "Línea: atrapada", GREEN), ("1983", "Desorden fuerte: atrapada", GREEN), ("2000", "Problema 1 de Simon", ORANGE), ("2026", "Una prueba afirmada", RED)], "goal": "En 3D o más, con poco desorden: ¿siguen libres las ondas?"},
        5: {"title": "Por qué es tan difícil", "rare": "En alguna parte, siempre hay una región rara que se porta mal", "all": "Controlarlas todas: a la vez, a toda escala, para siempre"},
        6: {"title": "El plan afirmado", "note": "Un dibujo del plan, no la prueba en sí", "digits": "1. Revelar el azar dígito a dígito", "books": "2. Llevar una contabilidad estricta", "blocks": "3. Falla un paso: deshacer, marcar pendiente, limpiar después", "end": "Resultado afirmado: en un rango de energías, las ondas son libres"},
        7: {"title": "Lo que no afirma", "yes": "Afirma: ondas libres en ciertas energías, con poco desorden, de 3D en adelante", "no": ["El límite exacto entre ondas atrapadas y libres", "La difusión corriente: otro problema", "Cuán pequeño debe ser el desorden en 3D"]},
        8: {"title": "Comprobarlo por computadora",
            "cards": [("Lo ejecutamos", "El código Lean de Yao Xu compiló en nuestra máquina, sin errores."), ("Axiomas", "Solo los tres estándar: propext, Classical.choice, Quot.sound."),
                      ("Límite 1", "Una comprobación por computadora no explica la idea."), ("Límite 2", "Todavía hay personas que deben confirmar que el código hace la pregunta original.")]},
        9: {"title": "Cómo están las cosas",
            "cards": [("MathDB", "Marca el problema como abierto y la afirmación como no verificada."), ("Revisión", "No conocemos ninguna revisión independiente de matemáticos."),
                      ("Nosotros", "Leímos la introducción y el plan, no todas las páginas.")], "bottom": "Una afirmación notable con comprobación automática. Aún no es ciencia establecida."},
        10: {"title": "Una onda puede quedar atrapada por sus propios ecos", "items": ["Toda la matemática: las personas citadas. Explicación hecha con ayuda de IA.", "Fuentes: Anderson; Abrahams y otros; Kunz–Souillard; Simon; OpenAI; Yao Xu."]},
    },
}


def simulate(width, seed):
    """Evoluciona un paquete puntual en una linea periodica. Devuelve alturas, amplitudes por tiempo y anchuras."""
    rng = np.random.default_rng(seed)
    v = rng.uniform(-width / 2, width / 2, SIDE)
    h = np.diag(v)
    for i in range(SIDE):
        j = (i + 1) % SIDE
        h[i, j] = h[j, i] = 1.0
    energies, vectors = np.linalg.eigh(h)
    start = np.zeros(SIDE)
    start[SIDE // 2] = 1
    coeffs = vectors.T @ start
    x = np.arange(SIDE) - SIDE // 2
    amps, widths = [], []
    for time in np.linspace(0, TMAX, FRAMES):
        state = vectors @ (np.exp(-1j * energies * time) * coeffs)
        prob = np.abs(state) ** 2
        amps.append(np.abs(state))
        widths.append(float(np.sqrt(np.sum(x**2 * prob))))
    return v, amps, widths


CLEAN_V, CLEAN, CLEAN_W = simulate(0.0, SEED)
MESSY_V, MESSY, MESSY_W = simulate(4.0, SEED)


def wave(d, x0, x1, base, height, amp, color, heights=None):
    """Dibuja la onda sobre una linea base, con las alturas al azar como barras."""
    dx = (x1 - x0) / (SIDE - 1)
    if heights is not None:
        for i, value in enumerate(heights):
            if i % 2 == 0:
                px = x0 + i * dx
                d.line((px, base + 4, px, base + 4 + abs(value) * 16), fill=BAR, width=2)
    d.line((x0, base, x1, base), fill=(70, 84, 110), width=3)
    pts = [(x0 + i * dx, base - height * min(1.0, a / 0.45)) for i, a in enumerate(amp)]
    d.polygon([(x0, base)] + pts + [(x1, base)], fill=mix(BG, color, 0.55))
    d.line(pts, fill=color, width=3)


def frame_index(p):
    return min(FRAMES - 1, int(max(0.0, min(1.0, p)) * (FRAMES - 1)))


def scene1(d, t, T, x):
    centered(d, W / 2, 60, x["title"], f_title(72), mix(BG, INK, fade(t, 0.3, 1.0)))
    centered(d, W / 2, 150, x["sub"], f_body(38), mix(BG, MUTED, fade(t, 1.0, 1.0)))
    split = T * 0.42
    if t < split:
        wave(d, 180, W - 180, 620, 300, CLEAN[frame_index(t / split)], WAVE)
        centered(d, W / 2, 720, x["free"], f_title(40), mix(BG, WAVE, fade(t, 2.0)))
    else:
        wave(d, 180, W - 180, 620, 300, MESSY[frame_index((t - split) / (T - split - 2))], TRAP, MESSY_V)
        centered(d, W / 2, 750, x["stuck"], f_title(40), mix(BG, TRAP, fade(t, split + 1)))


def scene2(d, t, T, x):
    title(d, x["title"], t)
    i = frame_index(t / (T * 0.8))
    for base, amp, color, label, widths, heights in ((400, CLEAN[i], WAVE, x["clean"], CLEAN_W, None), (710, MESSY[i], TRAP, x["messy"], MESSY_W, MESSY_V)):
        wave(d, 170, W - 170, base, 170, amp, color, heights)
        d.text((170, base - 215), label, font=f_title(36), fill=color)
        value = f"{x['width']}: {widths[i]:.0f} {x['sites']}"
        box = d.textbbox((0, 0), value, font=f_title(36))
        d.text((W - 170 - (box[2] - box[0]), base - 215), value, font=f_title(36), fill=INK)
    centered(d, W / 2, 815, x["note"], f_body(28), mix(BG, MUTED, fade(t, T * 0.8)))


def pictogram(d, kind, cx, cy, k):
    color = mix(BG, WAVE, k)
    if kind == 0:
        for i in range(7):
            px = cx - 120 + i * 40
            d.ellipse((px - 7, cy - 7, px + 7, cy + 7), fill=color)
        d.line((cx - 120, cy, cx + 120, cy), fill=color, width=2)
    elif kind == 1:
        for i in range(5):
            for j in range(5):
                px, py = cx - 80 + i * 40, cy - 70 + j * 35
                d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=color)
    else:
        for layer in (2, 1, 0):
            for i in range(4):
                for j in range(4):
                    px, py = cx - 90 + i * 40 + layer * 24, cy - 60 + j * 34 - layer * 18
                    d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=mix(BG, color, 1 - layer * 0.25))


def scene3(d, t, T, x):
    title(d, x["title"], t)
    data = [(x["line"], 3.6, 0.13), (x["floor"], 28.6, 0.10), (x["building"], 32.9, 0.18)]
    centered(d, W / 2, 135, x["what"], f_body(32), mix(BG, MUTED, fade(t, 0.5)))
    for n, (name, weak, strong) in enumerate(data):
        k = fade(t, T * (0.05 + n * 0.17))
        cx = 360 + n * 600
        pictogram(d, n, cx, 300, k)
        centered(d, cx, 395, name, f_title(42), mix(BG, INK, k))
        grow = min(1.0, max(0.0, (t - T * (0.08 + n * 0.17)) / (T * 0.15)))
        for row, (value, color, label) in enumerate(((weak, GREEN, x["weak"]), (strong, RED, x["strong"]))):
            y = 480 + row * 130
            d.text((cx - 220, y), label, font=f_body(28), fill=mix(BG, MUTED, k))
            length = 400 * value / 35 * grow
            d.rectangle((cx - 220, y + 40, cx - 220 + max(3, length), y + 80), fill=mix(BG, color, k))
            digits = f"{value * grow:.1f} %" if value > 1 else f"{value * grow:.2f} %"
            d.text((cx - 210 + max(3, length), y + 40), digits, font=f_title(30), fill=mix(BG, INK, k))
    fnt = f_body(27)
    y = 770
    for line in wrap(d, x["note"], fnt, 1650):
        centered(d, W / 2, y, line, fnt, mix(BG, ORANGE, fade(t, T * 0.65)))
        y += 36


def scene4(d, t, T, x):
    title(d, x["title"], t)
    y = 440
    d.line((130, y, 1790, y), fill=(70, 84, 110), width=5)
    for i, (year, label, color) in enumerate(x["events"]):
        k = fade(t, T * (0.04 + i * 0.15))
        px = 250 + i * 355
        d.ellipse((px - 15, y - 15, px + 15, y + 15), fill=mix(BG, color, k))
        centered(d, px, y - 90, year, f_title(46), mix(BG, INK, k))
        fnt = f_body(30)
        line_y = y + 36
        for line in wrap(d, label, fnt, 310):
            centered(d, px, line_y, line, fnt, mix(BG, color, k))
            line_y += 38
    k = fade(t, T * 0.75)
    d.rounded_rectangle((180, 650, W - 180, 780), 18, fill=mix(BG, PANEL, k))
    centered(d, W / 2, 688, x["goal"], f_title(38), mix(BG, ORANGE, k))


GRID_RNG = random.Random(31)
GRID = [[GRID_RNG.random() for _ in range(64)] for _ in range(26)]
SPOTS = [(i, j, GRID_RNG.random()) for j, row in enumerate(GRID) for i, v in enumerate(row) if v > 0.982]


def scene5(d, t, T, x):
    title(d, x["title"], t)
    size, left, top = 26, 128, 170
    for j, row in enumerate(GRID):
        for i, value in enumerate(row):
            shade = 26 + int(value * 42)
            d.rectangle((left + i * size, top + j * 20, left + i * size + size - 3, top + j * 20 + 17), fill=(shade, shade + 8, shade + 26))
    for i, j, phase in SPOTS:
        k = fade(t, T * (0.1 + 0.3 * phase))
        px, py = left + i * size + 12, top + j * 20 + 8
        pulse = 0.65 + 0.35 * math.sin(t * 5 + phase * 9)
        d.rectangle((px - 13, py - 9, px + 11, py + 9), fill=mix(BG, mix(RED, ORANGE, pulse), k))
        scale = max(0.0, (t - T * 0.55) / (T * 0.4))
        if scale > 0:
            for ring in (1, 2, 3):
                r = 22 * ring * min(1.0, scale * 1.4)
                if py - r > top - 6:
                    d.rectangle((px - r, py - r, px + r, py + r), outline=mix(BG, ORANGE, 0.75 / ring), width=2)
    centered(d, W / 2, 705, x["rare"], f_title(36), mix(BG, ORANGE, fade(t, T * 0.15)))
    centered(d, W / 2, 770, x["all"], f_title(36), mix(BG, INK, fade(t, T * 0.58)))


DIGITS = random.Random(5)
BITS = [DIGITS.randint(0, 1) for _ in range(24)]


def scene6(d, t, T, x):
    title(d, x["title"], t)
    centered(d, W / 2, 130, x["note"], f_body(28), mix(BG, MUTED, fade(t, 0.3)))
    k = fade(t, T * 0.03)
    d.text((130, 180), x["digits"], font=f_title(34), fill=mix(BG, BLUE, k))
    shown = (t / (T * 0.35)) * len(BITS)
    for i, bit in enumerate(BITS):
        left = 130 + i * 69
        open_cell = i < shown
        d.rounded_rectangle((left, 235, left + 60, 295), 8, fill=mix(BG, PANEL, k), outline=mix(BG, BLUE if open_cell else BAR, k), width=2)
        centered(d, left + 30, 240, str(bit) if open_cell else "?", f_title(36), mix(BG, INK if open_cell else MUTED, k))

    k = fade(t, T * 0.28)
    d.text((130, 330), x["books"], font=f_title(34), fill=mix(BG, GREEN, k))
    for i in range(3):
        y = 390 + i * 34
        level = 0.72 + 0.12 * math.sin(t * (1.1 + i * 0.4) + i * 2)
        d.rectangle((130, y, 1790, y + 22), fill=mix(BG, PANEL, k))
        d.rectangle((130, y, 130 + 1660 * level, y + 22), fill=mix(BG, GREEN, k * 0.8))
    d.line((130 + 1660 * 0.5, 382, 130 + 1660 * 0.5, 496), fill=mix(BG, RED, k), width=4)

    k = fade(t, T * 0.5)
    d.text((130, 520), x["blocks"], font=f_title(34), fill=mix(BG, ORANGE, k))
    fail, clean_at = T * 0.6, T * 0.76
    for i in range(16):
        left = 130 + i * 104
        color = BLUE
        if i == 6 and t > fail:
            color = RED if t < clean_at else GREEN
        d.rectangle((left, 580, left + 92, 660), fill=mix(BG, mix(BG, color, 0.65), k), outline=mix(BG, color, k), width=3)
    if fail < t < clean_at:
        centered(d, 130 + 6 * 104 + 46, 665, "!", f_title(34), RED)
    k = fade(t, T * 0.84)
    d.rounded_rectangle((130, 725, W - 130, 815), 16, fill=mix(BG, PANEL, k))
    centered(d, W / 2, 745, x["end"], f_title(36), mix(BG, WAVE, k))


def mark(d, cx, cy, good, k):
    color = mix(BG, GREEN if good else RED, k)
    if good:
        d.line((cx - 18, cy, cx - 4, cy + 16, cx + 22, cy - 18), fill=color, width=8)
    else:
        d.line((cx - 16, cy - 16, cx + 16, cy + 16), fill=color, width=8)
        d.line((cx - 16, cy + 16, cx + 16, cy - 16), fill=color, width=8)


def scene7(d, t, T, x):
    title(d, x["title"], t)
    k = fade(t, T * 0.04)
    d.rounded_rectangle((130, 170, W - 130, 320), 18, fill=mix(BG, PANEL, k))
    mark(d, 190, 245, True, k)
    text_block(d, 245, 195, x["yes"], f_title(36), mix(BG, INK, k), 1500, 8)
    for i, line in enumerate(x["no"]):
        k = fade(t, T * (0.12 + i * 0.26))
        y = 355 + i * 145
        d.rounded_rectangle((130, y, W - 130, y + 125), 18, fill=mix(BG, PANEL, k))
        mark(d, 190, y + 62, False, k)
        d.text((245, y + 36), line, font=f_body(40), fill=mix(BG, INK, k))


def scene8(d, t, T, x):
    title(d, x["title"], t)
    colors = [GREEN, GREEN, ORANGE, RED]
    for i, (head, body) in enumerate(x["cards"]):
        k = fade(t, T * (0.1 + i * 0.2))
        y = 170 + i * 165
        d.rounded_rectangle((120, y, W - 120, y + 148), 18, fill=mix(BG, PANEL, k))
        d.text((165, y + 18), head, font=f_title(36), fill=mix(BG, colors[i], k))
        text_block(d, 165, y + 70, body, f_body(33), mix(BG, INK, k), 1570, 6)


def scene9(d, t, T, x):
    title(d, x["title"], t)
    colors = [ORANGE, RED, BLUE]
    for i, (head, body) in enumerate(x["cards"]):
        k = fade(t, T * (0.06 + i * 0.22))
        y = 170 + i * 165
        d.rounded_rectangle((120, y, W - 120, y + 148), 18, fill=mix(BG, PANEL, k))
        d.text((165, y + 18), head, font=f_title(36), fill=mix(BG, colors[i], k))
        text_block(d, 165, y + 70, body, f_body(34), mix(BG, INK, k), 1570, 6)
    k = fade(t, T * 0.72)
    fnt = f_title(38)
    y = 690
    for line in wrap(d, x["bottom"], fnt, 1600):
        centered(d, W / 2, y, line, fnt, mix(BG, ORANGE, k))
        y += 50


def scene10(d, t, T, x):
    i = frame_index(t / (T * 0.5))
    wave(d, 170, 900, 400, 220, CLEAN[i], WAVE)
    wave(d, 1020, 1750, 400, 220, MESSY[i], TRAP, MESSY_V)
    fnt = f_title(48)
    y = 545
    for line in wrap(d, x["title"], fnt, 1600):
        centered(d, W / 2, y, line, fnt, mix(BG, INK, fade(t, T * 0.25)))
        y += 60
    for n, line in enumerate(x["items"]):
        centered(d, W / 2, y + 40 + n * 50, line, f_body(30), mix(BG, MUTED, fade(t, T * (0.6 + 0.08 * n))))


DRAW = {1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7, 8: scene8, 9: scene9, 10: scene10}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lang = sys.argv[1]
    still = "--still" in sys.argv
    only = int(sys.argv[sys.argv.index("--scene") + 1]) if "--scene" in sys.argv else None
    print(f"anchura final: limpia {CLEAN_W[-1]:.1f}, desordenada {MESSY_W[-1]:.1f}", flush=True)
    scenes = json.loads((PROJECT / "scenes.json").read_text(encoding="utf-8"))
    out = BASE / lang / "anim"
    out.mkdir(parents=True, exist_ok=True)
    background = Image.new("RGB", (W, H), BG)
    srt, offset, index, timeline = [], 0.0, 1, []
    for scene in scenes:
        n = scene["n"]
        spoken = wav_seconds(PROJECT / "out" / lang / f"scene_{n:02d}.wav")
        duration = spoken + PAD
        cues = sentence_cues(scene[lang], spoken)
        for start, end, text in cues:
            srt.append(f"{index}\n{fmt(offset + start)} --> {fmt(offset + end)}\n{text}\n")
            index += 1
        timeline.append({"n": n, "start": round(offset, 3), "duration": round(duration, 3)})
        offset += duration
        if only and n != only:
            continue
        if still:
            for name, moment in (("a", duration * 0.3), ("b", duration * 0.85)):
                image = background.copy()
                d = ImageDraw.Draw(image)
                DRAW[n](d, moment, duration, TEXT[lang][n])
                draw_caption(d, cues, moment)
                image.save(out / f"still_{n:02d}{name}.png")
            continue
        command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                   "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(out / f"scene_{n:02d}.mp4")]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        for frame in range(int(duration * FPS)):
            moment = frame / FPS
            image = background.copy()
            d = ImageDraw.Draw(image)
            DRAW[n](d, moment, duration, TEXT[lang][n])
            draw_caption(d, cues, moment)
            pipe.stdin.write(image.tobytes())
        pipe.stdin.close()
        pipe.wait()
        print(f"escena {n} lista", flush=True)
    (BASE / lang / f"anderson_{lang}.srt").write_text("\n".join(srt), encoding="utf-8")
    (BASE / lang / "timeline.json").write_text(json.dumps(timeline), encoding="utf-8")
    print("total", round(offset, 1), "s")


if __name__ == "__main__":
    sys.exit(main())
