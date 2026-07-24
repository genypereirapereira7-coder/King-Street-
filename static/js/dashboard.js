// King Street — Painel administrativo
// Navegação e envios sem recarregar a página inteira: o conteúdo (#app) é
// buscado no servidor por fetch e trocado no lugar. O painel fica rápido,
// os dados continuam vindo sempre do servidor (nada de cache) e, ao salvar,
// a tela permanece na mesma posição — o aviso aparece numa barrinha.
(function () {
  "use strict";

  var SCROLL_KEY = "ks-painel-scroll";

  // ======================================================================
  // Barra de progresso
  // ======================================================================
  var bar = null, timer = null, largura = 0;

  function progresso(ativo) {
    bar = bar || document.getElementById("nav-progress");
    if (!bar) return;
    if (ativo) {
      if (timer) return;
      largura = 8;
      bar.classList.add("on");
      bar.style.width = largura + "%";
      timer = setInterval(function () {
        largura = Math.min(largura + (90 - largura) * 0.15, 90);
        bar.style.width = largura + "%";
      }, 100);
    } else {
      clearInterval(timer);
      timer = null;
      bar.style.width = "100%";
      setTimeout(function () {
        bar.classList.remove("on");
        bar.style.width = "0";
      }, 220);
    }
  }

  // ======================================================================
  // Barrinha de mensagens (toast)
  // ======================================================================
  function toast(texto, tipo) {
    var caixa = document.getElementById("toasts");
    if (!caixa) return;
    var el = document.createElement("div");
    el.className = "toast " + (tipo || "info");
    el.textContent = texto;
    caixa.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("show"); });
    setTimeout(function () {
      el.classList.remove("show");
      setTimeout(function () { el.remove(); }, 300);
    }, 3200);
  }

  /** Converte o bloco de mensagens do Django em barrinhas flutuantes. */
  function mostrarMensagens(raiz) {
    (raiz || document).querySelectorAll(".messages .msg").forEach(function (m) {
      toast(m.textContent.trim(), m.className.replace("msg", "").trim());
      m.remove();
    });
  }

  // ======================================================================
  // Troca de conteúdo
  // ======================================================================
  function rodarScripts(container) {
    container.querySelectorAll("script").forEach(function (antigo) {
      var s = document.createElement("script");
      if (antigo.src) { s.src = antigo.src; } else { s.textContent = antigo.textContent; }
      document.body.appendChild(s);
      s.remove();
    });
  }

  function trocar(html, urlFinal, opts) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    var novo = doc.getElementById("app");
    var atual = document.getElementById("app");
    // Sessão expirada (caiu na tela de login) ou página fora do painel
    if (!novo || !atual) { window.location.assign(urlFinal); return; }

    atual.replaceWith(novo);
    document.title = doc.title;
    rodarScripts(novo);
    mostrarMensagens(novo);

    if (opts.push) { history.pushState({ painel: true }, "", urlFinal); }

    // Ao salvar/adicionar, a tela fica exatamente onde estava.
    // Ao navegar por um link, começa do topo, como esperado.
    if (opts.manterPosicao) {
      window.scrollTo(0, opts.posicao || 0);
    } else {
      window.scrollTo(0, 0);
    }
  }

  function navegar(url, opts) {
    opts = opts || {};
    progresso(true);
    var init = { headers: { "X-Painel": "1" }, credentials: "same-origin", redirect: "follow" };
    if (opts.method === "POST") { init.method = "POST"; init.body = opts.body; }

    fetch(url, init)
      .then(function (r) {
        return r.text().then(function (t) { return { html: t, url: r.url || url }; });
      })
      .then(function (res) {
        trocar(res.html, res.url, {
          push: opts.push !== false,
          manterPosicao: opts.manterPosicao,
          posicao: opts.posicao,
        });
        progresso(false);
      })
      .catch(function () { window.location.assign(url); });
  }

  // ======================================================================
  // Interceptação de cliques e envios
  // ======================================================================
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    if (a.target === "_blank" || a.hasAttribute("download") || a.hasAttribute("data-recarregar")) return;
    if (/^(mailto:|tel:|https?:\/\/wa\.me)/i.test(href)) return;
    var url;
    try { url = new URL(a.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    // Sair do painel (logout / ver loja) recarrega normalmente
    if (url.pathname.indexOf("/painel/") !== 0) return;
    e.preventDefault();
    navegar(url.href, { push: true });
  });

  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (e.defaultPrevented || form.hasAttribute("data-recarregar")) return;
    var url;
    try { url = new URL(form.getAttribute("action") || location.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;

    var metodo = (form.getAttribute("method") || "GET").toUpperCase();
    e.preventDefault();

    if (metodo === "GET") {
      url.search = new URLSearchParams(new FormData(form)).toString();
      navegar(url.href, { push: true });
      return;
    }

    navegar(url.href, {
      method: "POST",
      body: new FormData(form),
      push: true,
      manterPosicao: true,
      posicao: window.scrollY,
    });
  });

  window.addEventListener("popstate", function () {
    navegar(location.href, { push: false });
  });

  // ======================================================================
  // Primeira carga
  // ======================================================================
  function iniciar() {
    mostrarMensagens(document);
    // Restaura a posição quando a página veio de um recarregamento completo
    var salvo = sessionStorage.getItem(SCROLL_KEY);
    if (salvo) {
      sessionStorage.removeItem(SCROLL_KEY);
      window.scrollTo(0, parseInt(salvo, 10) || 0);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js").catch(function () {});
  }
})();
