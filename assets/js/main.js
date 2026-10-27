/* ==========================================================================
   Barbearia O Patriarca — interações
   JavaScript puro, sem bibliotecas. O site funciona sem JS (links,
   fotos e preços aparecem normalmente); o JS só deixa tudo mais bonito.

   Índice
   1. Configuração (edite aqui)
   2. Utilidades
   3. Cabeçalho e menu mobile
   4. Animações de entrada
   5. Abas de serviços
   6. Brilho dos cards
   7. Lightbox do portfólio
   8. Status "aberto agora"
   9. Contador de visitas (GoatCounter)
   ========================================================================== */

(function () {
  'use strict';

  /* 1. Configuração ------------------------------------------------------- */

  /*
    GoatCounter: contador de visitas gratuito, sem cookies e sem banner.
    1) Crie uma conta em https://www.goatcounter.com/signup
    2) Escolha um código (ex.: "opatriarca" → opatriarca.goatcounter.com)
    3) Coloque só o código aqui entre as aspas.
    Vazio = contador desligado (nada é enviado).
  */
  var GOATCOUNTER_CODE = '';

  /*
    Horário de funcionamento usado no aviso "Aberto agora".
    0 = domingo, 1 = segunda ... 6 = sábado.
    null = fechado. Mantenha igual ao texto do HTML e ao JSON-LD.
  */
  var HORARIOS = {
    0: null,
    1: null,
    2: ['10:00', '20:00'],
    3: ['10:00', '20:00'],
    4: ['10:00', '20:00'],
    5: ['10:00', '20:00'],
    6: ['08:00', '17:00']
  };

  var DIAS = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];

  /* 2. Utilidades --------------------------------------------------------- */

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Avisa o CSS que o JS está ativo (libera as animações de entrada)
  document.documentElement.classList.add('js');

  var ano = $('[data-year]');
  if (ano) ano.textContent = new Date().getFullYear();

  /* 3. Cabeçalho e menu mobile ------------------------------------------- */

  var header = $('[data-header]');
  var nav = $('[data-nav]');
  var toggle = $('[data-menu-toggle]');
  var toggleLabel = $('[data-menu-label]');

  function aoRolar() {
    header.classList.toggle('is-scrolled', window.scrollY > 24);
  }
  aoRolar();
  window.addEventListener('scroll', aoRolar, { passive: true });

  function abrirMenu(abrir) {
    toggle.setAttribute('aria-expanded', String(abrir));
    toggleLabel.textContent = abrir ? 'Fechar menu' : 'Abrir menu';
    nav.classList.toggle('is-open', abrir);
    header.classList.toggle('is-open', abrir);
    document.body.classList.toggle('menu-open', abrir);
    if (abrir) {
      var primeiro = $('a', nav);
      if (primeiro) primeiro.focus();
    }
  }

  toggle.addEventListener('click', function () {
    abrirMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });

  // Fecha ao clicar num link do menu
  $$('a', nav).forEach(function (link) {
    link.addEventListener('click', function () {
      if (nav.classList.contains('is-open')) abrirMenu(false);
    });
  });

  // Fecha com Esc e devolve o foco ao botão
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      abrirMenu(false);
      toggle.focus();
    }
  });

  // Se a tela crescer para desktop com o menu aberto, fecha
  window.matchMedia('(min-width: 960px)').addEventListener('change', function (mq) {
    if (mq.matches) abrirMenu(false);
  });

  /* 4. Animações de entrada ---------------------------------------------- */

  var revelaveis = $$('[data-reveal]');

  // Escalona elementos irmãos para entrarem um depois do outro
  revelaveis.forEach(function (el) {
    var irmaos = $$(':scope > [data-reveal]', el.parentElement);
    var i = irmaos.indexOf(el);
    if (i > 0) el.style.setProperty('--delay', Math.min(i * 0.08, 0.4) + 's');
  });

  if ('IntersectionObserver' in window && !reduzMovimento) {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('is-visible');
          observador.unobserve(entrada.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revelaveis.forEach(function (el) { observador.observe(el); });
  } else {
    revelaveis.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* 5. Abas de serviços (padrão ARIA "tabs", com setas do teclado) ------- */

  var listaAbas = $('[data-tabs]');
  if (listaAbas) {
    var abas = $$('[role="tab"]', listaAbas);
    var paineis = abas.map(function (aba) { return document.getElementById(aba.getAttribute('aria-controls')); });

    function selecionar(indice, focar) {
      abas.forEach(function (aba, i) {
        var ativa = i === indice;
        aba.setAttribute('aria-selected', String(ativa));
        aba.tabIndex = ativa ? 0 : -1;
        paineis[i].hidden = !ativa;
      });
      if (focar) abas[indice].focus();
      abas[indice].scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: reduzMovimento ? 'auto' : 'smooth' });
    }

    abas.forEach(function (aba, i) {
      aba.addEventListener('click', function () { selecionar(i, false); });
      aba.addEventListener('keydown', function (e) {
        var alvo = null;
        if (e.key === 'ArrowRight') alvo = (i + 1) % abas.length;
        if (e.key === 'ArrowLeft') alvo = (i - 1 + abas.length) % abas.length;
        if (e.key === 'Home') alvo = 0;
        if (e.key === 'End') alvo = abas.length - 1;
        if (alvo !== null) { e.preventDefault(); selecionar(alvo, true); }
      });
    });

    // Sem JS todos os painéis aparecem; com JS, só o primeiro
    paineis.forEach(function (p, i) { p.hidden = i !== 0; });
  }

  /* 6. Brilho que acompanha o mouse nos cards (só em telas com mouse) ---- */

  if (window.matchMedia('(hover: hover)').matches) {
    $$('.card').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* 7. Lightbox do portfólio --------------------------------------------- */

  var dialogo = $('[data-lightbox-dialog]');
  var links = $$('[data-lightbox]');

  if (dialogo && typeof dialogo.showModal === 'function' && links.length) {
    var imgGrande = $('[data-lb-img]', dialogo);
    var legenda = $('[data-lb-caption]', dialogo);
    var contador = $('[data-lb-count]', dialogo);
    var atual = 0;
    var origemFoco = null;

    function mostrar(indice) {
      atual = (indice + links.length) % links.length;
      var link = links[atual];
      var miniatura = $('img', link);
      imgGrande.classList.remove('is-changing');
      void imgGrande.offsetWidth; // reinicia a animação
      imgGrande.classList.add('is-changing');
      imgGrande.src = link.getAttribute('href');
      imgGrande.alt = miniatura ? miniatura.alt : '';
      legenda.textContent = miniatura ? miniatura.alt : '';
      contador.textContent = String(atual + 1).padStart(2, '0') + ' / ' + String(links.length).padStart(2, '0');

      // Pré-carrega a próxima foto para a troca ficar instantânea
      var proxima = new Image();
      proxima.src = links[(atual + 1) % links.length].getAttribute('href');
    }

    links.forEach(function (link, i) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        origemFoco = link;
        mostrar(i);
        dialogo.showModal();
        document.body.classList.add('menu-open');
      });
    });

    $('[data-lb-close]', dialogo).addEventListener('click', function () { dialogo.close(); });
    $('[data-lb-prev]', dialogo).addEventListener('click', function () { mostrar(atual - 1); });
    $('[data-lb-next]', dialogo).addEventListener('click', function () { mostrar(atual + 1); });

    dialogo.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') mostrar(atual + 1);
      if (e.key === 'ArrowLeft') mostrar(atual - 1);
    });

    // Clique fora da foto fecha
    dialogo.addEventListener('click', function (e) {
      if (e.target === dialogo || e.target.classList.contains('lightbox__figure')) dialogo.close();
    });

    // Ao fechar (botão, Esc ou clique fora), devolve o foco à miniatura
    dialogo.addEventListener('close', function () {
      document.body.classList.remove('menu-open');
      if (origemFoco) origemFoco.focus();
    });

    // Deslizar o dedo para trocar de foto no celular
    var inicioX = null;
    imgGrande.draggable = false;
    imgGrande.addEventListener('pointerdown', function (e) { inicioX = e.clientX; });
    imgGrande.addEventListener('pointerup', function (e) {
      if (inicioX === null) return;
      var distancia = e.clientX - inicioX;
      if (Math.abs(distancia) > 45) mostrar(atual + (distancia < 0 ? 1 : -1));
      inicioX = null;
    });
  }

  /* 8. Status "aberto agora" (sempre no fuso de São Paulo) --------------- */

  function minutos(hhmm) {
    var p = hhmm.split(':');
    return Number(p[0]) * 60 + Number(p[1]);
  }

  function horaFormatada(hhmm) {
    var p = hhmm.split(':');
    return Number(p[0]) + 'h' + (p[1] !== '00' ? p[1] : '');
  }

  function atualizarStatus() {
    var alvos = $$('[data-open-status]');
    if (!alvos.length || !window.Intl) return;

    var partes = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/Sao_Paulo', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date());
    var mapa = {};
    partes.forEach(function (p) { mapa[p.type] = p.value; });
    var dia = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(mapa.weekday);
    var agora = Number(mapa.hour) * 60 + Number(mapa.minute);

    var hoje = HORARIOS[dia];
    var aberto = hoje && agora >= minutos(hoje[0]) && agora < minutos(hoje[1]);
    var texto;

    if (aberto) {
      texto = 'Aberto agora · até as ' + horaFormatada(hoje[1]);
    } else {
      // Procura o próximo dia/horário de abertura
      for (var i = 0; i < 8; i++) {
        var d = (dia + i) % 7;
        var h = HORARIOS[d];
        if (!h) continue;
        if (i === 0 && agora >= minutos(h[0])) continue;
        var quando = i === 0 ? 'hoje' : i === 1 ? 'amanhã' : DIAS[d];
        texto = 'Fechado agora · abre ' + quando + ' às ' + horaFormatada(h[0]);
        break;
      }
    }

    alvos.forEach(function (el) {
      el.textContent = texto || '';
      el.classList.toggle('is-open', Boolean(aberto));
      el.hidden = !texto;
    });
  }

  atualizarStatus();
  setInterval(atualizarStatus, 60 * 1000);

  /* 9. Contador de visitas (GoatCounter) ---------------------------------
     O script oficial conta a visita e também os cliques em qualquer
     elemento com o atributo data-goatcounter-click (já colocados nos
     botões de Agendar, WhatsApp e Avalie no Google).
     ----------------------------------------------------------------------- */

  if (/^[a-z0-9-]+$/.test(GOATCOUNTER_CODE)) {
    var gc = document.createElement('script');
    gc.async = true;
    gc.src = 'https://gc.zgo.at/count.js';
    gc.setAttribute('data-goatcounter', 'https://' + GOATCOUNTER_CODE + '.goatcounter.com/count');
    document.head.appendChild(gc);
  }
})();
