"""
Gera as imagens provisórias do site (placeholders, ícones e imagem de
compartilhamento). Rode de novo só se quiser recriar os placeholders.

Uso (na raiz do projeto):
    pip install pillow
    python scripts/gerar_imagens.py

As fotos reais devem SUBSTITUIR os arquivos em assets/img/portfolio e
assets/img/equipe, com os mesmos nomes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "assets" / "img"

FUNDO = (13, 12, 11)
SUPERFICIE = (34, 30, 26)
DOURADO = (201, 164, 103)
DOURADO_CLARO = (226, 196, 142)
TEXTO = (239, 232, 220)
APAGADO = (168, 159, 145)

FONTES = Path("C:/Windows/Fonts")


def fonte(nomes, tamanho):
    """Tenta as fontes em ordem e cai na padrão do Pillow se nenhuma existir."""
    for nome in nomes:
        caminho = FONTES / nome
        if caminho.exists():
            return ImageFont.truetype(str(caminho), tamanho)
    return ImageFont.load_default(tamanho)


def condensada(t):
    f = fonte(["bahnschrift.ttf", "arialbd.ttf"], t)
    try:
        f.set_variation_by_name("Bold Condensed")
    except Exception:
        pass
    return f


def serifada_italica(t):
    return fonte(["georgiai.ttf", "timesi.ttf"], t)


def serifada(t):
    return fonte(["georgiab.ttf", "timesbd.ttf"], t)


def sans(t):
    return fonte(["segoeui.ttf", "arial.ttf"], t)


def fundo_com_brilho(w, h, centro=(0.75, 0.3)):
    """Fundo escuro com brilho dourado suave e listras diagonais finas."""
    img = Image.new("RGB", (w, h), FUNDO)
    brilho = Image.new("RGB", (w, h), FUNDO)
    d = ImageDraw.Draw(brilho)
    cx, cy = int(w * centro[0]), int(h * centro[1])
    r = int(max(w, h) * 0.45)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(70, 56, 34))
    brilho = brilho.filter(ImageFilter.GaussianBlur(r // 2))
    img = Image.blend(img, brilho, 0.85)

    listras = ImageDraw.Draw(img)
    for x in range(-h, w, 24):
        listras.line((x, h, x + h, 0), fill=(24, 22, 20), width=1)
    return img


def centralizar(d, texto, f, y, w, cor):
    caixa = d.textbbox((0, 0), texto, font=f)
    d.text(((w - (caixa[2] - caixa[0])) / 2, y), texto, font=f, fill=cor)


def placeholder(caminho, w, h, titulo, subtitulo):
    img = fundo_com_brilho(w, h, centro=(0.5, 0.35))
    d = ImageDraw.Draw(img)
    m = 36
    d.rounded_rectangle((m, m, w - m, h - m), radius=18, outline=(70, 62, 52), width=2)
    centralizar(d, "FOTO", condensada(int(w * 0.07)), h * 0.40, w, DOURADO)
    centralizar(d, titulo, condensada(int(w * 0.11)), h * 0.46, w, TEXTO)
    centralizar(d, subtitulo, sans(int(w * 0.032)), h * 0.58, w, APAGADO)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    img.save(caminho, "JPEG", quality=78, optimize=True, progressive=True)


def og_image(caminho):
    w, h = 1200, 630
    img = fundo_com_brilho(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 10, h), fill=DOURADO)
    x = 90
    d.text((x, 96), "Barbearia", font=serifada_italica(64), fill=DOURADO_CLARO)
    d.text((x, 160), "O PATRIARCA", font=condensada(170), fill=TEXTO)
    d.text((x, 362), "Cidade Patriarca  ·  Zona Leste  ·  São Paulo", font=sans(34), fill=APAGADO)

    # selo de nota
    y = 450
    d.rounded_rectangle((x, y, x + 120, y + 70), radius=35, fill=DOURADO)
    centralizar_em(d, "4,9", condensada(48), (x, y, x + 120, y + 70), (23, 18, 11))
    d.text((x + 145, y + 4), "★★★★★", font=fonte(["seguisym.ttf", "segoeui.ttf"], 36), fill=DOURADO_CLARO)
    d.text((x + 145, y + 42), "+250 avaliações no Google", font=sans(24), fill=TEXTO)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    img.save(caminho, "JPEG", quality=86, optimize=True, progressive=True)


def centralizar_em(d, texto, f, caixa, cor):
    b = d.textbbox((0, 0), texto, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    x = caixa[0] + (caixa[2] - caixa[0] - tw) / 2 - b[0]
    y = caixa[1] + (caixa[3] - caixa[1] - th) / 2 - b[1]
    d.text((x, y), texto, font=f, fill=cor)


def icone(caminho, tamanho, borda=True):
    """Monograma 'P' dourado em fundo escuro."""
    escala = 4  # desenha grande e reduz para suavizar as bordas
    s = tamanho * escala
    img = Image.new("RGB", (s, s), FUNDO)
    d = ImageDraw.Draw(img)
    if borda:
        m = int(s * 0.12)
        d.ellipse((m, m, s - m, s - m), outline=DOURADO, width=max(2, s // 40))
    centralizar_em(d, "P", serifada_italica(int(s * 0.5)), (0, 0, s, s * 1.02), DOURADO_CLARO)
    img = img.resize((tamanho, tamanho), Image.LANCZOS)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    return img


def main():
    # Portfólio: 8 fotos 4:5
    for i in range(1, 9):
        placeholder(IMG / "portfolio" / f"corte-{i:02d}.jpg", 900, 1125,
                    f"CORTE {i:02d}", "substitua pela foto real")

    # Equipe
    for i in range(1, 3):
        placeholder(IMG / "equipe" / f"barbeiro-{i:02d}.jpg", 600, 750,
                    f"BARBEIRO {i:02d}", "substitua pela foto real")

    # Compartilhamento (WhatsApp, Instagram, Facebook...)
    og_image(IMG / "og-image.jpg")

    # Ícones
    icones = IMG / "icons"
    icone(icones / "apple-touch-icon.png", 180).save(icones / "apple-touch-icon.png")
    icone(icones / "icon-192.png", 192).save(icones / "icon-192.png")
    icone(icones / "icon-512.png", 512).save(icones / "icon-512.png")
    icone(icones / "favicon.ico", 64, borda=False).save(icones / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    print("Imagens geradas em", IMG)


if __name__ == "__main__":
    main()
