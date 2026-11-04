# Video script: Trapped by Chaos

Version 1.0, 4 November 2026 (UTC). English narration: Preston.
The analogies are teaching aids. The wave pictures come from a small simulation; they illustrate the idea and prove nothing.

## Scene 1. The strange idea

**Visual:** a wave spreading on a line, then a wave stuck among random bars.

**EN:** Shout down an empty hallway, and the sound travels. Now fill the hallway with random junk. You would expect the sound to get through slowly, like someone pushing through a crowd. In 1958, the physicist Philip Anderson found something much stranger. Randomness alone can stop a wave completely, with no walls at all. Today we ask when that happens, and look at a new proof that nobody has fully confirmed yet.

**ES:** Grita en un pasillo vacío y el sonido viaja. Ahora llena el pasillo de trastos al azar. Esperarías que el sonido pasara despacio, como alguien que se abre paso entre una multitud. En 1958, el físico Philip Anderson encontró algo mucho más extraño. El azar, por sí solo, puede detener por completo una onda, sin ninguna pared. Hoy preguntamos cuándo ocurre eso, y miramos una prueba nueva que nadie ha confirmado del todo.

## Scene 2. Trapped by its own echoes

**Visual:** a real simulation: clean line versus messy line.

**EN:** Here is a real simulation on a computer. On top, a wave moves along a clean line and spreads far. Below, the same wave meets random heights. It bounces, and it meets its own echoes. Those echoes cancel each other, again and again. So the wave stays near where it started, even though nothing blocks the way. In our run, the clean wave reached a width of about eighty-five sites. The messy one stayed near five.

**ES:** Esta es una simulación real en una computadora. Arriba, una onda avanza por una línea limpia y se extiende lejos. Abajo, la misma onda encuentra alturas al azar. Rebota y se topa con sus propios ecos. Esos ecos se cancelan una y otra vez. Así, la onda se queda cerca de donde empezó, aunque nada le bloquee el paso. En nuestra prueba, la onda limpia alcanzó una anchura de unos ochenta y cinco sitios. La desordenada se quedó cerca de cinco.

## Scene 3. More room, more routes

**Visual:** a line, a floor and a building; bars for how much space a wave fills.

**EN:** Now, the shape of the world matters. A hallway gives a wave one route. A floor gives it many. A building gives it even more. With more routes, echoes find it harder to cancel. Physicists predicted this in 1979. In a line, any mess traps the wave. In three dimensions, a little mess should leave waves free. Our small simulation shows that trend, but be careful: these grids are tiny, so it illustrates the idea and proves nothing.

**ES:** Ahora, la forma del mundo importa. Un pasillo da a la onda una sola ruta. Un piso le da muchas. Un edificio, todavía más. Con más rutas, a los ecos les cuesta más cancelarse. Los físicos lo predijeron en 1979. En una línea, cualquier desorden atrapa la onda. En tres dimensiones, un poco de desorden debería dejarla libre. Nuestra pequeña simulación muestra esa tendencia, pero ojo: estas cuadrículas son diminutas, así que ilustra la idea y no demuestra nada.

## Scene 4. The open question

**Visual:** a timeline: 1958, 1980, 2000.

**EN:** Physicists believed it. Mathematicians could not prove it. The trapped side came first: in 1980 for a line, and later for very strong disorder. But the free side, on a real three-dimensional grid, kept resisting. In the year 2000, the mathematician Barry Simon made it problem number one on his list for the new century. Prove that in three dimensions or more, a little disorder leaves a range of energies where waves stay free.

**ES:** Los físicos lo creían. Los matemáticos no podían demostrarlo. El lado atrapado llegó primero: en 1980 para una línea, y más tarde para desorden muy fuerte. Pero el lado libre, en una cuadrícula real de tres dimensiones, seguía resistiendo. En el año 2000, el matemático Barry Simon lo puso como problema número uno de su lista para el nuevo siglo. Demostrar que, en tres dimensiones o más, un poco de desorden deja un rango de energías donde las ondas siguen libres.

## Scene 5. Why it is so hard

**Visual:** a huge random grid with rare bright trouble spots.

**EN:** Why so hard? Because the grid is infinite and every point is random. Somewhere, there is always a rare region that behaves badly. A proof cannot just handle the average. It has to control every trouble spot at once, at every scale, forever. It is like promising that a city's traffic will always flow, when any street could suddenly jam.

**ES:** ¿Por qué es tan difícil? Porque la cuadrícula es infinita y cada punto es aleatorio. En alguna parte, siempre hay una región rara que se porta mal. Una prueba no puede ocuparse solo del promedio. Tiene que controlar cada punto problemático a la vez, a toda escala, para siempre. Es como prometer que el tráfico de una ciudad siempre fluirá, cuando cualquier calle puede atascarse de pronto.

## Scene 6. The claimed proof

**Visual:** digits revealed one by one; a ledger; a failed block set aside.

**EN:** In September 2026, OpenAI released a paper claiming a proof. Here is the plan in plain words. Work on a finite grid. Reveal the randomness one binary digit at a time, and keep strict accounts of how the wave quantities change. If a local step goes wrong, undo it and mark that block as pending, to be cleaned up later. In the end, the accounts turn into a statement about the infinite grid: on a certain range of energies, waves are free.

**ES:** En septiembre de 2026, OpenAI publicó un artículo que afirma una prueba. Este es el plan en palabras sencillas. Trabajar en una cuadrícula finita. Revelar el azar dígito binario a dígito binario y llevar una contabilidad estricta de cómo cambian las cantidades de la onda. Si un paso local sale mal, se deshace y ese bloque se marca como pendiente, para limpiarlo después. Al final, esa contabilidad se convierte en una afirmación sobre la cuadrícula infinita: en cierto rango de energías, las ondas son libres.

## Scene 7. What it does not say

**Visual:** a checklist with claimed and not claimed.

**EN:** It is important to say what this does not claim. It does not find the exact boundary between trapped and free waves. It does not settle ordinary diffusion, which is a separate problem on Simon's list. And in three dimensions, it only shows that a small enough disorder exists, without saying how small. So even if it is right, this is one big step, and not the whole story.

**ES:** Es importante decir lo que esto no afirma. No encuentra el límite exacto entre ondas atrapadas y libres. No resuelve la difusión corriente, que es otro problema de la lista de Simon. Y en tres dimensiones, solo muestra que existe un desorden suficientemente pequeño, sin decir cuánto. Así que, aunque sea correcto, es un gran paso y no toda la historia.

## Scene 8. Checking it by computer

**Visual:** Lean build result; three honest labels.

**EN:** A researcher named Yao Xu turned this into Lean, a program that checks logic step by step. So we ran it ourselves, on a clean machine. It built with no errors, and it relies only on the three standard axioms. That is real evidence. But a computer check has limits. It does not explain the idea. And people still have to confirm that the code asks the same question as the original problem.

**ES:** Un investigador llamado Yao Xu lo convirtió a Lean, un programa que comprueba la lógica paso a paso. Así que lo ejecutamos nosotros, en una máquina limpia. Compiló sin errores y solo usa los tres axiomas estándar. Es una evidencia real. Pero una comprobación por computadora tiene límites. No explica la idea. Y todavía hay personas que deben confirmar que el código hace la misma pregunta que el problema original.

## Scene 9. Where things stand

**Visual:** status list.

**EN:** So where do things stand? MathDB still lists the problem as open, and calls the claim unverified. We know of no independent review by mathematicians. We read the introduction and the plan of the paper, not every page. So please treat this as a striking claim backed by a machine check, and not yet as settled science.

**ES:** Entonces, ¿cómo están las cosas? MathDB todavía marca el problema como abierto y considera la afirmación no verificada. No conocemos ninguna revisión independiente de matemáticos. Leímos la introducción y el plan del artículo, no todas las páginas. Por eso, tómalo como una afirmación notable respaldada por una comprobación automática, no todavía como ciencia establecida.

## Scene 10. The takeaway

**Visual:** the two waves again; credits with sources.

**EN:** Here is the idea in one breath. A wave in a messy world can be trapped by its own echoes, with no walls at all. In a line, that always happens. In three dimensions, a little mess should leave waves free, and now there is a claimed proof, waiting for experts to confirm it. All the mathematics belongs to the people named in the sources. This explanation was made with the help of AI. Sources are in the description.

**ES:** Esta es la idea de un tirón. Una onda en un mundo desordenado puede quedar atrapada por sus propios ecos, sin ninguna pared. En una línea, eso siempre ocurre. En tres dimensiones, un poco de desorden debería dejarla libre, y ahora hay una prueba afirmada, a la espera de que los expertos la confirmen. Toda la matemática pertenece a las personas citadas en las fuentes. Esta explicación se hizo con ayuda de inteligencia artificial. Las fuentes están en la descripción.
