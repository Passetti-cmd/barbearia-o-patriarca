# Onde editar cada coisa

Dica: no VS Code, `Ctrl+Shift+F` e procure por **`CONFIRMAR`** ou **`TROCAR`** para achar todos os pontos pendentes.

## Textos

Tudo está no `index.html`, dividido por blocos comentados (`01 · HERO`, `02 · SERVIÇOS` etc.).

| O quê | Onde |
| --- | --- |
| Frase do topo | `index.html` → bloco **HERO**, parágrafo `hero__lead` |
| Texto "Sobre" | `index.html` → bloco **SOBRE**, dentro de `about__text` |
| Nome dos barbeiros | `index.html` → bloco **SOBRE**, `<h4>` dentro de `.barber` |
| Título e descrição do Google | `index.html` → `<title>` e `<meta name="description">` no topo |

## Preços e serviços

Os preços estão em **dois lugares**. Mudou um, mude o outro:

1. `index.html` → bloco **SERVIÇOS** (cards de destaque e listas `price-list` de cada aba).
2. `index.html` → JSON-LD no `<head>`, em `"hasOfferCatalog"` (é o que o Google lê).

Para adicionar um serviço, copie uma linha `<li>` da lista e altere nome, tempo e preço.

## Fotos

| Foto | Arquivo | Tamanho ideal |
| --- | --- | --- |
| Portfólio | `assets/img/portfolio/corte-01.jpg` … `corte-08.jpg` | 900 × 1125 px (retrato 4:5) |
| Equipe | `assets/img/equipe/barbeiro-01.jpg`, `barbeiro-02.jpg` | 600 × 750 px |
| Prévia no WhatsApp | `assets/img/og-image.jpg` | 1200 × 630 px |

1. Substitua o arquivo **mantendo o mesmo nome**.
2. Comprima antes em [squoosh.app](https://squoosh.app) (JPG, qualidade ~75, menos de 200 KB cada).
3. No `index.html`, ajuste o `alt` de cada foto descrevendo o corte de verdade (ex.: *"Degradê navalhado com barba desenhada"*). O `alt` ajuda no Google Imagens e em leitores de tela.
4. Para ter mais ou menos fotos, copie/remova um `<li class="gallery__item">`. As fotos com `gallery__item--tall` ocupam duas linhas.

Peça ao dono fotos com **boa luz e fundo limpo**. Se possível, tiradas sempre do mesmo ângulo.

## Horários

Estão em **três lugares** (todos marcados com `CONFIRMAR`):

1. `index.html` → bloco **LOCALIZAÇÃO**, lista `<dl class="hours">` (o que o visitante lê).
2. `index.html` → JSON-LD, `"openingHoursSpecification"` (o que o Google lê).
3. `assets/js/main.js` → `HORARIOS` (alimenta o aviso "Aberto agora").

## Cores e fontes

`assets/css/style.css`, bloco **1. Tokens** no topo. Trocar `--gold` e `--gold-light` muda o destaque do site inteiro.

## Links

| Link | Valor atual |
| --- | --- |
| Booksy | `https://booksy.com/pt-br/1047773_barbearia-o-patriarca_barbearias_3081_sao-paulo` |
| WhatsApp | `https://wa.me/5511947296481` (com mensagem pronta "Vim pelo site…") |
| Instagram | `https://www.instagram.com/barbearia_o_patriarca/` |
| Avalie no Google | busca no Maps; ideal trocar pelo link curto de avaliação (veja abaixo) |

**Link direto para avaliar:** no Perfil da Empresa no Google, o dono clica em **Pedir avaliações** e copia o link (algo como `https://g.page/r/XXXX/review`). Cole no `href` do botão "Avalie a gente no Google".

Para trocar o número de WhatsApp, use buscar e substituir em `5511947296481` no `index.html`.

## Avaliações reais

No bloco **AVALIAÇÕES** do `index.html` há um modelo comentado. Copie, descomente e cole o texto exatamente como está no Google, com o primeiro nome do cliente. Não invente nem edite depoimentos. Enquanto a lista estiver vazia, ela não aparece no site.

## Imagens provisórias

Para recriar os placeholders, os ícones ou a `og-image.jpg` (por exemplo, depois de mudar a nota):

```bash
pip install pillow
```

```bash
python scripts/gerar_imagens.py
```

Cuidado: isso sobrescreve as fotos em `portfolio/` e `equipe/`. Rode só antes de colocar as fotos reais.
