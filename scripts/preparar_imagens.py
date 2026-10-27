"""
Prepara as imagens do site a partir das fotos originais.

- Recorta e comprime as fotos do portfólio e da equipe
- Gera o logo dourado com fundo transparente (usado no site)
- Gera favicon, ícones do app e a imagem de compartilhamento (og-image)

Uso (na raiz do projeto):
    pip install pillow
    python scripts/preparar_imagens.py

As fotos originais ficam em fotos_originais/ (fora do Git, por serem
pesadas). Para trocar uma foto: coloque o arquivo novo lá, ajuste a
lista PORTFOLIO ou EQUIPE abaixo e rode o script de novo.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / "fotos_originais"
IMG = RAIZ / "assets" / "img"

FUNDO = (13, 12, 11)
DOURADO = (201, 164, 103)
DOURADO_CLARO = (226, 196, 142)
TEXTO = (239, 232, 220)
APAGADO = (168, 159, 145)

# Portfólio: (arquivo original, arquivo final). Fotos quadradas, máx. 900 px.
PORTFOLIO = [
    ("degrade-alto-barba-perfil.jpg", "corte-01.jpg"),
    ("kids-risco-desenhado.jpg", "corte-02.jpg"),
    ("taper-costas-textura.jpg", "corte-03.jpg"),
    ("slick-back-degrade.jpg", "corte-04.jpg"),
    ("barba-cheia-degrade.jpg", "corte-05.jpg"),
    ("corte-cacheado-costas.jpg", "corte-06.jpg"),
    ("social-risco-lateral.jpg", "corte-07.jpg"),
    ("barbeiro-tesoura.jpg", "corte-08.jpg"),
]

# Equipe: (original, final, recorte (esq, topo, dir, base) em frações da foto).
# O recorte enquadra o rosto do barbeiro em retrato 4:5.
EQUIPE = [
    ("barbeiro-pb.png", "barbeiro-01.jpg", (0.20, 0.0, 1.0, 1.0)),
    ("barbeiro-tesoura.jpg", "barbeiro-02.jpg", (0.465, 0.03, 0.932, 0.613)),
]

LADO_MAX = 900
FONTES = Path("C:/Windows/Fonts")


# --- utilidades -------------------------------------------------------------

def abrir(nome):
    """Abre a foto corrigindo a rotação do celular (EXIF) e em RGB."""
    img = Image.open(ORIGINAIS / nome)
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        fundo = Image.new("RGB", img.size, FUNDO)
        fundo.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
        return fundo
    return img.convert("RGB")


def salvar_jpg(img, destino, qualidade=80):
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino, "JPEG", quality=qualidade, optimize=True, progressive=True)
    print(f"  {destino.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}  {destino.stat().st_size // 1024} KB")


def fonte(nomes, tamanho):
    for nome in nomes:
        if (FONTES / nome).exists():
            return ImageFont.truetype(str(FONTES / nome), tamanho)
    return ImageFont.load_default(tamanho)


def condensada(t):
    f = fonte(["bahnschrift.ttf", "arialbd.ttf"], t)
    try:
        f.set_variation_by_name("Bold Condensed")
    except Exception:
        pass
    return f


# --- portfólio e equipe -----------------------------------------------------

def preparar_portfolio():
    print("Portfólio:")
    for original, final in PORTFOLIO:
        img = abrir(original)
        lado = min(img.size)
        img = ImageOps.fit(img, (lado, lado), Image.LANCZOS)  # garante quadrado
        if lado > LADO_MAX:
            img = img.resize((LADO_MAX, LADO_MAX), Image.LANCZOS)
        salvar_jpg(img, IMG / "portfolio" / final)


def preparar_equipe():
    print("Equipe:")
    for original, final, (e, t, d, b) in EQUIPE:
        img = abrir(original)
        w, h = img.size
        img = img.crop((int(e * w), int(t * h), int(d * w), int(b * h)))
        img = ImageOps.fit(img, (img.width, int(img.width * 1.25)), Image.LANCZOS)
        if img.width > 600:
            img = img.resize((600, 750), Image.LANCZOS)
        salvar_jpg(img, IMG / "equipe" / final)


# --- logo, ícones e og-image ------------------------------------------------

def logo_dourado():
    """Logo branco em fundo preto -> logo dourado com fundo transparente.
    O brilho de cada pixel vira a transparência, então o relevo é mantido."""
    img = abrir("logo.jpg")
    escala = 2
    img = img.resize((img.width * escala, img.height * escala), Image.LANCZOS)
    luz = img.convert("L")
    luz = luz.point(lambda v: 0 if v < 28 else min(255, int((v - 28) * 1.25)))

    # degradê dourado de cima (claro) para baixo (escuro)
    cor = Image.new("RGB", img.size)
    d = ImageDraw.Draw(cor)
    for y in range(img.height):
        p = y / img.height
        c = tuple(int(DOURADO_CLARO[i] * (1 - p) + DOURADO[i] * p) for i in range(3))
        d.line((0, y, img.width, y), fill=c)

    final = cor.convert("RGBA")
    final.putalpha(luz)
    final = final.crop(final.getbbox())
    destino = IMG / "logo" / "logo-dourado.webp"
    destino.parent.mkdir(parents=True, exist_ok=True)
    web = final.copy()
    web.thumbnail((480, 480), Image.LANCZOS)  # versão leve para o site
    web.save(destino, "WEBP", quality=88, method=6)  # WebP com transparência: bem mais leve que PNG
    print(f"  {destino.relative_to(RAIZ)}  {web.size[0]}x{web.size[1]}  {destino.stat().st_size // 1024} KB")
    return final


def icones(logo):
    """Ícones: logo inteiro (app) e só o rosto do brasão (favicon)."""
    print("Ícones:")
    pasta = IMG / "icons"
    pasta.mkdir(parents=True, exist_ok=True)

    def quadrado(conteudo, tamanho, margem):
        base = Image.new("RGBA", (tamanho, tamanho), FUNDO + (255,))
        alvo = int(tamanho * (1 - 2 * margem))
        c = conteudo.copy()
        c.thumbnail((alvo, alvo), Image.LANCZOS)
        base.alpha_composite(c, ((tamanho - c.width) // 2, (tamanho - c.height) // 2))
        return base.convert("RGB")

    for nome, tamanho in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
        quadrado(logo, tamanho, 0.08).save(pasta / nome, optimize=True)

    # rosto do brasão, legível em 16-32 px
    w, h = logo.size
    rosto = logo.crop((int(w * 0.27), int(h * 0.14), int(w * 0.73), int(h * 0.80)))
    quadrado(rosto, 64, 0.06).save(pasta / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    quadrado(rosto, 64, 0.06).save(pasta / "favicon.png", optimize=True)
    print("  favicon.ico, favicon.png, apple-touch-icon.png, icon-192.png, icon-512.png")


def og_image(logo):
    print("Compartilhamento:")
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), FUNDO)

    brilho = Image.new("RGB", (w, h), FUNDO)
    d = ImageDraw.Draw(brilho)
    d.ellipse((620, -80, 1300, 600), fill=(70, 56, 34))
    img = Image.blend(img, brilho.filter(ImageFilter.GaussianBlur(170)), 0.9)
    d = ImageDraw.Draw(img)
    for x in range(-h, w, 24):
        d.line((x, h, x + h, 0), fill=(24, 22, 20), width=1)
    d.rectangle((0, 0, 10, h), fill=DOURADO)

    marca = logo.copy()
    marca.thumbnail((440, 440), Image.LANCZOS)
    base = img.convert("RGBA")
    base.alpha_composite(marca, (w - marca.width - 70, (h - marca.height) // 2))
    img = base.convert("RGB")
    d = ImageDraw.Draw(img)

    x = 80
    d.text((x, 120), "Barbearia", font=fonte(["georgiai.ttf"], 58), fill=DOURADO_CLARO)
    d.text((x, 180), "O PATRIARCA", font=condensada(128), fill=TEXTO)
    d.text((x, 340), "Cidade Patriarca · Zona Leste · SP", font=fonte(["segoeui.ttf"], 30), fill=APAGADO)

    y = 440
    d.rounded_rectangle((x, y, x + 116, y + 66), radius=33, fill=DOURADO)
    nota = condensada(46)
    b = d.textbbox((0, 0), "4,9", font=nota)
    d.text((x + (116 - (b[2] - b[0])) / 2 - b[0], y + (66 - (b[3] - b[1])) / 2 - b[1]), "4,9", font=nota, fill=(23, 18, 11))
    d.text((x + 138, y + 2), "★★★★★", font=fonte(["seguisym.ttf"], 34), fill=DOURADO_CLARO)
    d.text((x + 138, y + 38), "+250 avaliações no Google", font=fonte(["segoeui.ttf"], 23), fill=TEXTO)

    salvar_jpg(img, IMG / "og-image.jpg", qualidade=86)


def main():
    if not ORIGINAIS.exists():
        raise SystemExit(f"Pasta {ORIGINAIS} não encontrada.")
    preparar_portfolio()
    preparar_equipe()
    print("Logo:")
    logo = logo_dourado()
    icones(logo)
    og_image(logo)


if __name__ == "__main__":
    main()
