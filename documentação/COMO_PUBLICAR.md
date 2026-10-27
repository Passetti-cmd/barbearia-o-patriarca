# Como publicar no GitHub Pages

Tempo estimado: 10 minutos. Não precisa de build nem de Node.

## 1. Criar o repositório

1. Entre em [github.com/new](https://github.com/new).
2. Nome do repositório: **`barbearia-o-patriarca`** (se usar outro nome, veja o passo 4).
3. Deixe **Public** e **não** marque "Add a README" (o projeto já tem um).
4. Clique em **Create repository**.

## 2. Enviar os arquivos

Na pasta do projeto, pelo terminal:

```bash
git remote add origin https://github.com/passetti-cmd/barbearia-o-patriarca.git
```

```bash
git push -u origin main
```

> O repositório local já vem com o primeiro commit. Se você começou do zero, rode antes `git init`, `git add .` e `git commit -m "feat: site da barbearia"`.

## 3. Ligar o GitHub Pages

1. No repositório, vá em **Settings → Pages**.
2. Em **Source**, escolha **Deploy from a branch**.
3. Branch **`main`**, pasta **`/ (root)`** → **Save**.
4. Espere 1 a 2 minutos. O site fica em:
   `https://passetti-cmd.github.io/barbearia-o-patriarca/`

## 4. Se o endereço for diferente

Se mudar o usuário, o nome do repositório ou usar um domínio próprio, troque o endereço nestes lugares (busque por `passetti-cmd.github.io`):

| Arquivo | O que trocar |
| --- | --- |
| `index.html` | `canonical`, `og:url`, `og:image`, `twitter:image` e as URLs do JSON-LD |
| `sitemap.xml` | todas as `<loc>` |
| `robots.txt` | linha `Sitemap:` |
| `404.html` | o caminho `/barbearia-o-patriarca/` |

## 5. Colocar no Google (o passo que mais traz cliente)

1. **Google Search Console:** acesse [search.google.com/search-console](https://search.google.com/search-console), adicione a propriedade com o endereço do site (opção *Prefixo do URL*), verifique pela tag HTML (cole a `<meta name="google-site-verification">` no `<head>` do `index.html`) e envie o `sitemap.xml` em **Sitemaps**.
2. **Perfil da Empresa no Google:** peça ao dono para colocar o link do site no campo **Site** do perfil da barbearia no Google Maps. Isso liga o site à nota 4,9 e é o que mais ajuda nas buscas locais.
3. **Instagram e Booksy:** colocar o link do site na bio do Instagram e no perfil do Booksy.

## 6. Testar depois de publicar

- [Teste de pesquisa aprimorada](https://search.google.com/test/rich-results) → cole a URL e confira se o `BarberShop` aparece sem erros.
- [PageSpeed Insights](https://pagespeed.web.dev/) → nota de desempenho no celular (bom para o relatório do projeto).
- Mande o link no WhatsApp para você mesmo e confira a prévia com a imagem.
