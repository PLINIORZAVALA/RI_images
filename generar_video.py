"""
Genera reel_conceptos.mp4 — narración española (espeak-ng) + diapositivas PIL + MoviePy.
Sin emojis en PIL (no compatible); se usan formas geométricas y texto ASCII.
"""

import os, subprocess, math
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H   = 1280, 720
FPS    = 24
OUT    = "reel_conceptos.mp4"
TMP    = "/tmp/ri_video"
os.makedirs(TMP, exist_ok=True)

# ── paleta ────────────────────────────────────────────────────────────────────
BG     = (10, 10, 15)
WHITE  = (226, 232, 240)
MUTED  = (90, 110, 130)
PURPLE = (167, 139, 250)
CYAN   = (103, 232, 249)
GREEN  = (110, 231, 183)
AMBER  = (252, 211, 77)
RED    = (248, 113, 113)
ORANGE = (251, 146, 60)
PINK   = (244, 114, 182)
INDIGO = (165, 180, 252)

# ── fuentes ───────────────────────────────────────────────────────────────────
_font_cache = {}
def F(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        candidates = [
            f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
            f"/usr/share/fonts/truetype/liberation/LiberationSans{'-Bold' if bold else '-Regular'}.ttf",
        ]
        for p in candidates:
            if os.path.exists(p):
                _font_cache[key] = ImageFont.truetype(p, size); break
        else:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]

# ── helpers ───────────────────────────────────────────────────────────────────
def frame():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def grad(draw, top, bot):
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i]-top[i])*t) for i in range(3))
        draw.line([(0,y),(W,y)], fill=c)

def tw(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2]-bb[0]

def dot_label(draw, x, y, text, color, font=None):
    f = font or F(14, bold=True)
    draw.ellipse([x, y+3, x+8, y+11], fill=color)
    draw.text((x+14, y), text, font=f, fill=WHITE)

def tag(draw, x, y, text, bg, fg):
    f = F(14, bold=True)
    bb = draw.textbbox((0,0), text, font=f)
    pw, ph = 16, 6
    draw.rounded_rectangle([x, y, x+bb[2]+pw*2, y+bb[3]+ph*2], radius=16, fill=bg)
    draw.text((x+pw, y+ph), text, font=f, fill=fg)
    return y + bb[3] + ph*2 + 14

def accent(draw, x, y, w, col, h=4):
    draw.rounded_rectangle([x,y,x+w,y+h], radius=2, fill=col)

def counter_bar(draw, n, total=10):
    # slide counter top-right
    draw.text((W-100, 22), f"{n:02d} / {total:02d}", font=F(18), fill=MUTED)
    # progress bar bottom
    bx, by, bw = 40, H-10, W-80
    draw.rounded_rectangle([bx, by, bx+bw, by+6], radius=3, fill=(20,20,35))
    fill_w = int(bw * n / total)
    if fill_w > 0:
        draw.rounded_rectangle([bx, by, bx+fill_w, by+6], radius=3, fill=PURPLE)

def row_card(draw, x, y, w, h, sym, sym_col, sym_bg, title, desc):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=(16,18,30), outline=(28,28,50))
    # icon box
    draw.rounded_rectangle([x+10, y+10, x+50, y+h-10], radius=10, fill=sym_bg)
    sw = tw(draw, sym, F(16, bold=True))
    draw.text((x+10+(40-sw)//2, y+h//2-10), sym, font=F(16, bold=True), fill=sym_col)
    draw.text((x+60, y+10), title, font=F(15, bold=True), fill=WHITE)
    draw.text((x+60, y+30), desc,  font=F(13),            fill=MUTED)

def pipeline_step(draw, x, y, w, label, col):
    h = 46
    draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=(14,14,24), outline=(25,25,45))
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=col)
    draw.text((x+16, y+13), label, font=F(16, bold=True), fill=WHITE)

# ── TTS ───────────────────────────────────────────────────────────────────────
def tts(text, out_wav):
    subprocess.run(
        ["espeak-ng", "-v", "es-419", "-s", "130", "-p", "52", "-w", out_wav, text],
        check=True, capture_output=True
    )

# ── NARRACIÓN ─────────────────────────────────────────────────────────────────
NARRATIONS = [
    ("Bienvenidos. En este video vamos a explorar los conceptos aplicados en el proyecto "
     "de Análisis de Imágenes R G B, desarrollado en la BUAP para el décimo semestre. "
     "El objetivo es transformar imágenes en datos numéricos y aplicarles análisis estadístico."),
    ("El stack tecnológico usa Python como lenguaje base. "
     "Open C V para leer y procesar imágenes. "
     "Num Pie para operaciones matriciales. "
     "Pandas para datos tabulares y Excel. "
     "Matplotlib y Sci Pie para gráficas y estadística. "
     "Y Tkinter para construir la interfaz gráfica de usuario."),
    ("El primer concepto clave es el procesamiento de imágenes con Open C V. "
     "Se carga cada imagen del corpus, se redimensiona a cien por cien píxeles "
     "para estandarizar el tamaño, y luego se separa en sus tres canales de color: "
     "azul, verde y rojo. El proyecto se enfoca principalmente en el canal rojo."),
    ("La vectorización convierte la matriz bidimensional del canal rojo, "
     "de cien por cien píxeles, en un vector unidimensional de diez mil valores. "
     "Esto se logra con la función flatten de Num Pie. "
     "Cada imagen queda representada como una fila en un archivo Excel."),
    ("El pipeline completo del proyecto fluye en siete etapas: "
     "primero el corpus de imágenes, luego la lectura y redimensionamiento, "
     "después la extracción del canal R, el aplanamiento a vector unidimensional, "
     "el cálculo de estadísticas descriptivas, la regresión lineal con visualización, "
     "y finalmente la exportación de reportes en Excel y gráficos PNG."),
    ("En la etapa de estadísticas descriptivas se calculan ocho métricas sobre "
     "los valores de intensidad del canal rojo, que van de cero a doscientos cincuenta y cinco. "
     "Estas métricas son: media, mediana, moda, varianza, desviación estándar, "
     "rango, primer cuartil y tercer cuartil. Todo se guarda en un archivo Excel."),
    ("La regresión lineal se calcula con Sci Pie usando la función lin regres. "
     "Se ajusta una línea de la forma y igual a m por x más b, "
     "donde m es la pendiente que indica la dirección de la tendencia, "
     "b es la intersección con el eje y, "
     "y el coeficiente R cuadrado indica qué tan bien el modelo lineal explica los datos."),
    ("Los residuos son las diferencias entre los valores reales y los predichos por la recta. "
     "El error estándar S se calcula como la raíz cuadrada de la suma de residuos al cuadrado "
     "dividida entre n menos dos. "
     "Este valor cuantifica la dispersión típica de los puntos alrededor de la línea."),
    ("Con la regla empírica de tres sigma se evalúan los intervalos de confianza. "
     "Se espera que el sesenta y ocho por ciento de los puntos "
     "estén dentro de una desviación estándar, "
     "el noventa y cinco por ciento dentro de dos, "
     "y el noventa y nueve punto siete por ciento dentro de tres. "
     "El programa cuenta cuántos puntos caen en cada banda."),
    ("Finalmente, la arquitectura del sistema sigue el patrón M V C, "
     "separando la lógica de procesamiento de la interfaz Tkinter. "
     "El procesamiento es en batch sobre todo el corpus. "
     "Cada etapa guarda resultados intermedios en Excel. "
     "El desarrollo fue iterativo, con versiones numeradas del cero punto cero al cero punto seis. "
     "Este es el pipeline completo de análisis de imágenes R G B. Gracias."),
]

# ── SLIDES ────────────────────────────────────────────────────────────────────

def slide_01():
    img, d = frame()
    grad(d, (10,8,20), (18,12,38))
    counter_bar(d, 1)
    # big colored square as "logo"
    d.rounded_rectangle([60,60,140,140], radius=20, fill=(40,20,70))
    d.text((78,78), "RGB", font=F(30, bold=True), fill=PURPLE)
    # tag
    y = tag(d, 60, 158, "BUAP · 10 SEMESTRE", (40,18,65), PURPLE)
    d.text((60, y),    "Analisis de",   font=F(52, bold=True), fill=PURPLE)
    d.text((60, y+60), "Imagenes RGB",  font=F(52, bold=True), fill=WHITE)
    accent(d, 60, y+122, 400, PURPLE)
    d.text((60, y+135),
           "De pixeles a estadisticas: pipeline completo de",
           font=F(20), fill=MUTED)
    d.text((60, y+160),
           "vision computacional y regresion lineal.",
           font=F(20), fill=MUTED)
    row_card(d, 60, y+210, W-120, 58,
             "PY", PURPLE, (35,15,60),
             "Stack principal",
             "Python · OpenCV · NumPy · Pandas · Tkinter")
    row_card(d, 60, y+278, W-120, 58,
             "OBJ", CYAN, (8,32,48),
             "Objetivo",
             "Extraer canal R, vectorizar corpus y aplicar regresion lineal")
    return img

def slide_02():
    img, d = frame()
    grad(d, (8,16,14), (14,28,22))
    counter_bar(d, 2)
    y = tag(d, 60, 60, "STACK TECNOLOGICO", (8,38,20), CYAN)
    d.text((60, y),    "Herramientas", font=F(52, bold=True), fill=CYAN)
    d.text((60, y+60), "usadas",       font=F(52, bold=True), fill=WHITE)
    tools = [
        ("PY",  "Python 3",   "Lenguaje principal",           PURPLE),
        ("CV",  "OpenCV",     "Lectura y procesado imgs",      CYAN),
        ("NP",  "NumPy",      "Operaciones matriciales",       GREEN),
        ("PD",  "Pandas",     "Datos tabulares / Excel",       AMBER),
        ("MPL", "Matplotlib", "Graficas y scatter plots",      ORANGE),
        ("SP",  "SciPy",      "Regresion lineal",              RED),
        ("TK",  "Tkinter",    "Interfaz grafica GUI",          INDIGO),
        ("XLS", "Excel xlsx", "Persistencia de datos",         PINK),
    ]
    gx, gy = 60, y+140
    mw, mh = (W-140)//4-2, 58
    for i, (sym, name, desc, col) in enumerate(tools):
        cx = gx + (i%4)*(mw+8)
        cy2 = gy + (i//4)*(mh+8)
        d.rounded_rectangle([cx, cy2, cx+mw, cy2+mh], radius=10,
                             fill=(14,18,26), outline=(26,28,46))
        sym_bg = tuple(int(c*0.14) for c in col)
        d.rounded_rectangle([cx+6, cy2+6, cx+36, cy2+36], radius=8, fill=sym_bg)
        sw = tw(d, sym, F(11, bold=True))
        d.text((cx+6+(30-sw)//2, cy2+13), sym, font=F(11, bold=True), fill=col)
        d.text((cx+8, cy2+38), name, font=F(11, bold=True), fill=WHITE)
    return img

def slide_03():
    img, d = frame()
    grad(d, (8,18,10), (12,26,16))
    counter_bar(d, 3)
    y = tag(d, 60, 60, "PROCESAMIENTO DE IMAGENES", (8,34,14), GREEN)
    d.text((60, y),    "De imagen",  font=F(52, bold=True), fill=GREEN)
    d.text((60, y+60), "a matriz",   font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "OpenCV carga, redimensiona y separa los canales RGB.", font=F(18), fill=MUTED)
    # pixel grid – canal R
    cols = [235,192,169,205,178,214,
            108, 74, 85,114, 92,104,
             58, 46, 54, 64, 58, 45]
    rows_lbl = ["R","G","B"]
    row_col  = [(200,50,50),(50,160,50),(50,80,200)]
    gx2, gy2 = 100, y+175
    cs = 54
    for ri in range(3):
        d.text((gx2-35, gy2+ri*cs+cs//3), rows_lbl[ri],
               font=F(18, bold=True), fill=row_col[ri])
        for ci in range(6):
            val = cols[ri*6+ci]
            alpha = val/255
            cc = tuple(int(c*alpha) for c in row_col[ri])
            bx = gx2+ci*cs; by = gy2+ri*cs
            d.rounded_rectangle([bx+2,by+2,bx+cs-2,by+cs-2], radius=6, fill=cc)
            lbl = str(val)
            d.text((bx+cs//2-len(lbl)*4, by+cs//2-9), lbl, font=F(12,bold=True), fill=WHITE)
    # code block
    cx1, cy1 = 60, gy2+3*cs+14
    d.rounded_rectangle([cx1, cy1, W-60, cy1+100], radius=12, fill=(6,8,16), outline=(22,22,42))
    code = [
        "img = cv2.imread('imagen.jpg')",
        "img = cv2.resize(img, (100, 100))",
        "B, G, R = cv2.split(img)   # <- separa canales",
    ]
    for li, line in enumerate(code):
        d.text((cx1+18, cy1+14+li*26), line, font=F(15), fill=GREEN)
    return img

def slide_04():
    img, d = frame()
    grad(d, (16,12,6), (26,20,8))
    counter_bar(d, 4)
    y = tag(d, 60, 60, "VECTORIZACION", (40,28,6), AMBER)
    d.text((60, y),    "Imagen -> Vector", font=F(52, bold=True), fill=AMBER)
    d.text((60, y+60), "1D",               font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "La matriz 2D del canal R se aplana a 10 000 valores (100x100).", font=F(18), fill=MUTED)
    # formula box
    fy = y+188
    d.rounded_rectangle([60, fy, W-60, fy+72], radius=14, fill=(20,16,4), outline=(58,44,10))
    d.text((120, fy+16), "M 100x100", font=F(32, bold=True), fill=AMBER)
    arr_x = 120+tw(d,"M 100x100",F(32,bold=True))+20
    d.text((arr_x, fy+20), "->  flatten()  ->", font=F(24), fill=MUTED)
    vx = arr_x+tw(d,"->  flatten()  ->",F(24))+20
    d.text((vx, fy+16), "V 10000", font=F(32, bold=True), fill=AMBER)
    # code block
    cy2 = fy+90
    d.rounded_rectangle([60, cy2, W-60, cy2+100], radius=12, fill=(6,8,16), outline=(22,22,42))
    code = [
        "vector_R = R.flatten()          # shape (10000,)",
        "df       = pd.DataFrame([vector_R])",
        "df.to_excel('vectores_unicos.xlsx')",
    ]
    for li, line in enumerate(code):
        d.text((80, cy2+14+li*26), line, font=F(15), fill=GREEN)
    # output card
    oy = cy2+110
    row_card(d, 60, oy, W-120, 62,
             "XLS", AMBER, (36,26,4),
             "vectores_unicos.xlsx",
             "~315 KB  |  un vector de 10 000 valores por imagen")
    return img

def slide_05():
    img, d = frame()
    grad(d, (10,8,22), (16,12,36))
    counter_bar(d, 5)
    y = tag(d, 60, 60, "PIPELINE DE DATOS", (18,14,40), PURPLE)
    d.text((60, y),    "Flujo",    font=F(52, bold=True), fill=PURPLE)
    d.text((60, y+60), "completo", font=F(52, bold=True), fill=WHITE)
    steps = [
        ("Corpus de imagenes  (PNG / JPG)",        PURPLE),
        ("Lectura + Redimensionamiento 100x100",    CYAN),
        ("Extraccion canal R",                      RED),
        ("Aplanamiento a vector 1D",                AMBER),
        ("Estadisticas descriptivas",               GREEN),
        ("Regresion lineal + visualizacion",        INDIGO),
        ("Excel + graficos PNG",                    PINK),
    ]
    sy, sw = y+148, W-120
    for i, (lbl, col) in enumerate(steps):
        pipeline_step(d, 60, sy+i*52, sw, lbl, col)
        if i < len(steps)-1:
            d.text((60+sw//2-4, sy+i*52+46+2), "|", font=F(10), fill=MUTED)
    return img

def slide_06():
    img, d = frame()
    grad(d, (6,16,20), (10,24,30))
    counter_bar(d, 6)
    y = tag(d, 60, 60, "ESTADISTICAS DESCRIPTIVAS", (6,28,38), CYAN)
    d.text((60, y),    "Metricas",   font=F(52, bold=True), fill=CYAN)
    d.text((60, y+60), "por vector", font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "Calculadas sobre intensidades del canal R (0-255).", font=F(18), fill=MUTED)
    metrics = [
        ("mu",  "Media",          CYAN),
        ("Md",  "Mediana",        PURPLE),
        ("Mo",  "Moda",           GREEN),
        ("s2",  "Varianza",       AMBER),
        ("s",   "Desv. estandar", RED),
        ("R",   "Rango",          ORANGE),
        ("Q1",  "1er cuartil",    (52,211,153)),
        ("Q3",  "3er cuartil",    INDIGO),
    ]
    gx2, gy2 = 60, y+190
    mw, mh = (W-140)//4, 82
    for i, (sym, name, col) in enumerate(metrics):
        r, c = i//4, i%4
        mx = gx2 + c*(mw+8)
        my = gy2 + r*(mh+10)
        d.rounded_rectangle([mx, my, mx+mw, my+mh], radius=12,
                             fill=(12,16,26), outline=(22,26,44))
        accent(d, mx+10, my+mh-6, mw-20, col, h=3)
        sw2 = tw(d, sym, F(26, bold=True))
        d.text((mx+(mw-sw2)//2, my+14), sym, font=F(26, bold=True), fill=col)
        sw3 = tw(d, name, F(11))
        d.text((mx+(mw-sw3)//2, my+50), name, font=F(11), fill=MUTED)
    return img

def slide_07():
    img, d = frame()
    grad(d, (14,8,22), (20,12,34))
    counter_bar(d, 7)
    y = tag(d, 60, 60, "REGRESION LINEAL", (28,12,44), PURPLE)
    d.text((60, y),    "Modelo de",  font=F(52, bold=True), fill=PURPLE)
    d.text((60, y+60), "tendencia",  font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "SciPy ajusta la mejor recta sobre la nube de puntos.", font=F(18), fill=MUTED)
    # formula
    fy = y+188
    d.rounded_rectangle([60, fy, W-60, fy+72], radius=14, fill=(18,10,30), outline=(50,28,80))
    cx2 = W//2 - 140
    d.text((cx2,      fy+14), "y  =  ", font=F(38, bold=True), fill=WHITE)
    d.text((cx2+104,  fy+14), "m",      font=F(38, bold=True), fill=RED)
    d.text((cx2+134,  fy+14), " x  +  ",font=F(38, bold=True), fill=WHITE)
    d.text((cx2+256,  fy+14), "b",      font=F(38, bold=True), fill=CYAN)
    # param cards
    params = [
        ("m",  "Pendiente (slope)",        "Direccion y tasa de cambio de la intensidad", RED),
        ("b",  "Interseccion (intercept)", "Valor inicial cuando x = 0",                 CYAN),
        ("R2", "Coef. determinacion",      "Que tan bien explica el modelo los datos (0-1)", GREEN),
    ]
    py2 = fy+84
    for i, (sym, title, desc, col) in enumerate(params):
        row_card(d, 60, py2+i*70, W-120, 62,
                 sym, col, tuple(int(c*0.12) for c in col),
                 title, desc)
    # code
    cy_c = py2+3*70+6
    d.rounded_rectangle([60, cy_c, W-60, cy_c+46], radius=10, fill=(6,6,14), outline=(20,20,40))
    d.text((80, cy_c+12), "m, b, r, p, se = stats.linregress(x, y)", font=F(16), fill=GREEN)
    return img

def slide_08():
    img, d = frame()
    grad(d, (6,18,10), (10,28,16))
    counter_bar(d, 8)
    y = tag(d, 60, 60, "RESIDUOS Y ERROR S", (6,30,12), GREEN)
    d.text((60, y),    "Desviaciones", font=F(52, bold=True), fill=GREEN)
    d.text((60, y+60), "de la linea",  font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "Cada punto tiene una distancia vertical a la recta de regresion.", font=F(18), fill=MUTED)
    formulas = [
        ("e_i  =  y_i  -  y_predicho",          "residuo = valor real - valor predicho"),
        ("S  =  sqrt( Sum(e^2) / (n-2) )",       "error estandar de la regresion"),
    ]
    fy2 = y+195
    for i, (formula, sub) in enumerate(formulas):
        fx, fw, fh = 60, W-120, 86
        cy2 = fy2 + i*(fh+12)
        d.rounded_rectangle([fx, cy2, fx+fw, cy2+fh], radius=14,
                             fill=(10,28,14), outline=(18,52,22))
        d.text((fx+20, cy2+12), formula, font=F(26, bold=True), fill=GREEN)
        d.text((fx+20, cy2+50), sub,     font=F(15),            fill=MUTED)
    cy_card = fy2 + 2*(86+12) + 8
    row_card(d, 60, cy_card, W-120, 64,
             "S", GREEN, (6,22,10),
             "Uso de S",
             "Cuantifica la dispersion tipica de los puntos alrededor de la recta")
    return img

def slide_09():
    img, d = frame()
    grad(d, (18,14,6), (28,22,8))
    counter_bar(d, 9)
    y = tag(d, 60, 60, "INTERVALOS DE CONFIANZA", (36,26,6), AMBER)
    d.text((60, y),    "Regla",    font=F(52, bold=True), fill=AMBER)
    d.text((60, y+60), "3 Sigma",  font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "Cuantos puntos caen dentro de cada banda de confianza.", font=F(18), fill=MUTED)
    bands = [
        ("+-1 sigma  ->  68.27 %", "banda verde",   (14,50,24),  (22,80,36),  GREEN),
        ("+-2 sigma  ->  95.45 %", "banda azul",    (12,26,54),  (18,46,82),  (147,197,253)),
        ("+-3 sigma  ->  99.73 %", "banda amarilla",(36,26,6),   (58,44,10),  AMBER),
    ]
    iy = y+196
    for i, (lbl, sub, bg, outline, col) in enumerate(bands):
        ix, iw, ih = 60, W-120, 70
        cy2 = iy + i*(ih+10)
        d.rounded_rectangle([ix, cy2, ix+iw, cy2+ih], radius=12, fill=bg, outline=outline)
        d.text((ix+20, cy2+12), lbl, font=F(26, bold=True), fill=col)
        d.text((ix+20, cy2+44), sub, font=F(15),            fill=MUTED)
    cy_card = iy + 3*(70+10) + 6
    row_card(d, 60, cy_card, W-120, 62,
             "VIZ", AMBER, (32,22,4),
             "Visualizacion",
             "Scatter + recta + 3 bandas superpuestas -> exportado a PNG")
    return img

def slide_10():
    img, d = frame()
    grad(d, (8,8,16), (14,12,28))
    counter_bar(d, 10)
    y = tag(d, 60, 60, "ARQUITECTURA", (16,14,34), INDIGO)
    d.text((60, y),    "Diseno",     font=F(52, bold=True), fill=INDIGO)
    d.text((60, y+60), "del sistema",font=F(52, bold=True), fill=WHITE)
    d.text((60, y+130), "Iteracion incremental 7 versiones (0.0 -> 0.6) con GUI integrada.", font=F(18), fill=MUTED)
    arch = [
        ("MVC", "Patron MVC",          "Logica Python separada de la vista Tkinter",   INDIGO),
        ("BTH", "Batch processing",    "Corpus completo procesado en un solo ciclo",   GREEN),
        ("XLS", "Persistencia Excel",  "Cada etapa guarda resultados en .xlsx",        AMBER),
        ("ITE", "Desarrollo iterativo","Versionado numerico 0.0 -> 0.6 en el repo",   RED),
    ]
    ay = y+196
    for i, (sym, title, desc, col) in enumerate(arch):
        row_card(d, 60, ay+i*70, W-120, 62,
                 sym, col, tuple(int(c*0.12) for c in col),
                 title, desc)
    fw_y = ay + 4*70 + 10
    ftxt = "RI_images  |  BUAP 10 semestre  |  Python + OpenCV + SciPy"
    d.text((W//2 - tw(d,ftxt,F(14))//2, fw_y), ftxt, font=F(14), fill=MUTED)
    return img

SLIDE_FNS = [slide_01, slide_02, slide_03, slide_04, slide_05,
             slide_06, slide_07, slide_08, slide_09, slide_10]

# ── MAIN ─────────────────────────────────────────────────────────────────────
print("Generando narracion (espeak-ng)...")
audio_paths = []
for i, text in enumerate(NARRATIONS):
    wav = f"{TMP}/audio_{i:02d}.wav"
    tts(text, wav)
    audio_paths.append(wav)
    print(f"  audio {i+1}/10 OK")

print("\nGenerando clips de video...")
clips = []
for i, (fn, audio_path) in enumerate(zip(SLIDE_FNS, audio_paths)):
    frame_path = f"{TMP}/frame_{i:02d}.png"
    fn().save(frame_path)
    audio   = AudioFileClip(audio_path)
    dur     = audio.duration + 0.7
    clip    = ImageClip(frame_path).with_duration(dur).with_audio(audio)
    clips.append(clip)
    print(f"  clip {i+1}/10  ({dur:.1f}s)")

print(f"\nExportando -> {OUT}")
final = concatenate_videoclips(clips, method="compose")
final.write_videofile(
    OUT, fps=FPS, codec="libx264", audio_codec="aac",
    temp_audiofile=f"{TMP}/tmp_audio.mp4",
    remove_temp=True, logger="bar",
)
total = sum(c.duration for c in clips)
print(f"\nVideo listo: {OUT}  ({total:.0f} segundos)")
