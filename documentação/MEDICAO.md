# Medição de resultados (GoatCounter)

O [GoatCounter](https://www.goatcounter.com) é um contador de visitas gratuito, de código aberto, **sem cookies** e sem coletar dados pessoais. Por isso o site não precisa de banner de consentimento (LGPD).

O contador **vem desligado**. Nenhum dado é enviado até você colocar seu código.

## Ativar

1. Crie a conta em [goatcounter.com/signup](https://www.goatcounter.com/signup).
2. Escolha o código do site, por exemplo `opatriarca` (o painel fica em `opatriarca.goatcounter.com`).
3. Abra `assets/js/main.js` e preencha:

   ```js
   var GOATCOUNTER_CODE = 'opatriarca';
   ```

4. Publique. Visitas de `localhost` não são contadas, então teste pelo link do GitHub Pages.

> Esse código não é segredo nem senha: ele só diz para qual painel as visitas vão. Mesmo assim, se preferir, ative só depois da apresentação.

## Eventos registrados

Cada botão tem um atributo `data-goatcounter-click`. O GoatCounter conta os cliques automaticamente:

| Evento | Botões | Mede |
| --- | --- | --- |
| `agendar-booksy` | Hero, cabeçalho, menu mobile, Serviços, chamada final, rodapé | Intenção de agendar |
| `whatsapp` | Hero, Localização, chamada final, rodapé, botão flutuante | Contato direto |
| `avaliar-google` | Seção Avaliações | Novas avaliações |
| `ver-avaliacoes-google` | Seção Avaliações | Interesse na reputação |
| `rota-maps` | Localização | Intenção de visitar |
| `instagram` | Portfólio, rodapé | Tráfego para o Instagram |

O atributo `data-goatcounter-title` guarda **de qual seção** veio o clique (ex.: "Hero", "Botão flutuante"). No painel, abra o evento para ver essa divisão e descobrir qual botão converte mais.

## Comparar antes e depois (para o relatório)

1. **Antes:** anote com o dono, por 2 a 4 semanas antes do site, quantos agendamentos chegaram pelo Booksy e quantas conversas novas no WhatsApp por semana. O Perfil da Empresa no Google também mostra cliques em "Site", "Ligar" e "Rotas".
2. **Depois:** com o site no ar e o link no Google, Instagram e Booksy, compare pelo mesmo período:
   - visitas no site (GoatCounter → *Pageviews*)
   - cliques em `agendar-booksy` e `whatsapp`
   - cliques em `avaliar-google` e o número de avaliações no Google
   - de onde vieram as visitas (GoatCounter → *Referrers*: Google, Instagram, WhatsApp)
3. **Taxa de conversão:** `(cliques em agendar + whatsapp) ÷ visitas`. Acompanhe semana a semana para ver se mudanças no site (fotos novas, texto) melhoram o número.

Dica: o WhatsApp abre com a mensagem *"Vim pelo site…"*, então o dono também consegue contar na mão quantos clientes chegaram pelo site.
