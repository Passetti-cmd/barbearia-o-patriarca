# Onde editar cada coisa

Dica: no VS Code, `Ctrl+Shift+F` busca um texto em todos os arquivos de uma vez.

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

| Foto | Arquivo no site | Formato |
| --- | --- | --- |
| Portfólio | `assets/img/portfolio/corte-01.jpg` … `corte-08.jpg` | quadrada, até 900 px |
| Equipe | `assets/img/equipe/barbeiro-01.jpg`, `barbeiro-02.jpg` | retrato 4:5 |
| Logo | `assets/img/logo/logo-dourado.webp` | gerado a partir do logo original |
| Prévia no WhatsApp | `assets/img/og-image.jpg` | 1200 × 630 px |

As fotos são preparadas por um script, a partir dos originais em `fotos_originais/` (pasta fora do Git, porque os arquivos são pesados):

1. Coloque a foto nova em `fotos_originais/`.
2. Em `scripts/preparar_imagens.py`, ajuste a lista `PORTFOLIO` (qual original vira qual `corte-XX.jpg`) ou `EQUIPE` (com o recorte do rosto).
3. Rode o script (comandos abaixo). Ele recorta, redimensiona e comprime tudo.
4. No `index.html`, ajuste o `alt` da foto descrevendo o corte de verdade (ex.: *"Degradê navalhado com barba desenhada"*). O `alt` ajuda no Google Imagens e em leitores de tela.
5. Para ter mais ou menos fotos, copie/remova um `<li class="gallery__item">`. Use múltiplos de 4 (4, 8, 12) para a grade fechar certinha.

Peça ao dono fotos **quadradas, com boa luz**, de preferência mostrando o corte de lado ou de costas.

## Horários

Estão em **três lugares**. Mudou um, mude os outros:

1. `index.html` → bloco **LOCALIZAÇÃO**, lista `<dl class="hours">` (o que o visitante lê).
2. `index.html` → JSON-LD, `"openingHoursSpecification"` (o que o Google lê).
3. `assets/js/main.js` → `HORARIOS` (alimenta o aviso "Aberto agora").

## Cores e fontes

`assets/css/style.css`, bloco **1. Tokens** no topo. Trocar `--gold` e `--gold-light` muda o destaque do site inteiro.

## Links

| Link | Valor atual |
| --- | --- |
| Booksy | `https://booksy.com/pt-br/3081_barbearia-o-patriarca_barbearias_1047773_sao-paulo` |
| WhatsApp | `https://wa.me/5511947296481` (com mensagem pronta "Vim pelo site…") |
| Instagram | `https://www.instagram.com/barbearia_o_patriarca/` |
| Avalie no Google | abre a barbearia no Google Maps |

Para trocar o número de WhatsApp, use buscar e substituir em `5511947296481` no `index.html`.

## Avaliações reais

No bloco **AVALIAÇÕES** do `index.html` há um modelo comentado. Copie, descomente e cole o texto exatamente como está no Google, com o primeiro nome do cliente. Não invente nem edite depoimentos. Enquanto a lista estiver vazia, ela não aparece no site.

## Recriar imagens, logo e ícones

O mesmo script gera o logo dourado, o favicon, os ícones do app e a `og-image.jpg` (rode de novo se mudar a nota ou o logo):

```bash
pip install pillow
```

```bash
python scripts/preparar_imagens.py
```
