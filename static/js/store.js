// King Street — interações da loja + navegação instantânea (sem recarregar)
// A troca de página é feita via fetch, substituindo apenas o #app, com uma
// transição suave. Tudo continua sendo renderizado pelo servidor (Django).
(function () {
  "use strict";

  // ======================================================================
  // Galeria deslizável do produto
  // ======================================================================
  function initGallery() {
    var gallery = document.getElementById("gallery");
    if (!gallery) return;
    var track = document.getElementById("gallery-track");
    var total = parseInt(gallery.dataset.count || "1", 10);
    var index = 0;
    var startX = 0, startY = 0, deltaX = 0, dragging = false, locked = false, width = 0;

    var dots = Array.prototype.slice.call(document.querySelectorAll("#gallery-dots .dot"));
    var thumbs = Array.prototype.slice.call(document.querySelectorAll("#gallery-thumbs img"));

    function goTo(i) {
      index = Math.max(0, Math.min(total - 1, i));
      track.classList.add("animate");
      track.style.transform = "translateX(" + (-index * 100) + "%)";
      dots.forEach(function (d, k) { d.classList.toggle("active", k === index); });
      thumbs.forEach(function (t, k) { t.classList.toggle("active", k === index); });
    }

    // Setas (desktop)
    var prev = document.getElementById("gallery-prev");
    var next = document.getElementById("gallery-next");
    if (prev) prev.addEventListener("click", function () { goTo(index - 1); });
    if (next) next.addEventListener("click", function () { goTo(index + 1); });

    // Pontinhos e miniaturas
    dots.forEach(function (d) { d.addEventListener("click", function () { goTo(parseInt(d.dataset.index, 10)); }); });
    thumbs.forEach(function (t) { t.addEventListener("click", function () { goTo(parseInt(t.dataset.index, 10)); }); });

    if (total <= 1) return;

    // Arraste com o dedo / mouse
    function onStart(x, y) {
      dragging = true; locked = false;
      startX = x; startY = y; deltaX = 0;
      width = gallery.offsetWidth;
      track.classList.remove("animate");
    }
    function onMove(x, y, e) {
      if (!dragging) return;
      var dx = x - startX, dy = y - startY;
      if (!locked) {
        // Decide se o gesto é horizontal (deslizar foto) ou vertical (rolar página)
        if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
        if (Math.abs(dy) > Math.abs(dx)) { dragging = false; return; }
        locked = true;
      }
      deltaX = dx;
      if (e && e.cancelable) e.preventDefault();
      var pct = (-index * 100) + (dx / width) * 100;
      track.style.transform = "translateX(" + pct + "%)";
    }
    function onEnd() {
      if (!dragging) return;
      dragging = false;
      if (Math.abs(deltaX) > width * 0.2) {
        goTo(index + (deltaX < 0 ? 1 : -1));
      } else {
        goTo(index);
      }
    }

    gallery.addEventListener("touchstart", function (e) { onStart(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
    gallery.addEventListener("touchmove", function (e) { onMove(e.touches[0].clientX, e.touches[0].clientY, e); }, { passive: false });
    gallery.addEventListener("touchend", onEnd);

    gallery.addEventListener("mousedown", function (e) { onStart(e.clientX, e.clientY); e.preventDefault(); });
    window.addEventListener("mousemove", function (e) { if (dragging) onMove(e.clientX, e.clientY, e); });
    window.addEventListener("mouseup", onEnd);
  }

  // ======================================================================
  // Inicialização da página (re-executada a cada navegação)
  // ======================================================================
  function initPage() {
    // ---- Galeria do produto (deslizável com o dedo / arraste) ----
    initGallery();

    // ---- Seleção de variação (cor + tamanho) ----
    var box = document.getElementById("variation-picker");
    if (box) {
      var variations = JSON.parse(box.dataset.variations || "[]");
      var state = { color: null, size: null };
      var hidden = document.getElementById("variation_id");
      var addBtn = document.getElementById("add-to-cart-btn");
      var feedback = document.getElementById("variation-feedback");

      var findVariation = function () {
        return variations.find(function (v) { return v.color === state.color && v.size === state.size; });
      };
      var refresh = function () {
        // Tamanhos que existem para a cor escolhida (a loja não controla quantidade)
        document.querySelectorAll(".pill[data-size]").forEach(function (p) {
          var available = variations.some(function (v) {
            return (!state.color || v.color === state.color) && v.size === p.dataset.size;
          });
          p.classList.toggle("disabled", !available);
        });
        var v = findVariation();
        if (state.color && state.size && v) {
          hidden.value = v.id; addBtn.disabled = false;
          feedback.textContent = "Disponível"; feedback.style.color = "var(--success)";
        } else {
          hidden.value = ""; addBtn.disabled = true;
          if (state.color && state.size) { feedback.textContent = "Combinação indisponível"; feedback.style.color = "var(--danger)"; }
          else { feedback.textContent = "Escolha cor e tamanho"; feedback.style.color = "var(--text-dim)"; }
        }
      };
      box.querySelectorAll(".pill[data-color]").forEach(function (p) {
        p.addEventListener("click", function () {
          if (p.classList.contains("disabled")) return;
          box.querySelectorAll(".pill[data-color]").forEach(function (x) { x.classList.remove("active"); });
          p.classList.add("active"); state.color = p.dataset.color; refresh();
        });
      });
      box.querySelectorAll(".pill[data-size]").forEach(function (p) {
        p.addEventListener("click", function () {
          if (p.classList.contains("disabled")) return;
          box.querySelectorAll(".pill[data-size]").forEach(function (x) { x.classList.remove("active"); });
          p.classList.add("active"); state.size = p.dataset.size; refresh();
        });
      });
      refresh();
    }

    // ---- Controle de quantidade ----
    document.querySelectorAll(".qty").forEach(function (q) {
      var input = q.querySelector("input");
      var max = parseInt(input.getAttribute("max") || "999", 10);
      q.querySelector(".minus").addEventListener("click", function () {
        input.value = Math.max(1, parseInt(input.value || "1", 10) - 1);
      });
      q.querySelector(".plus").addEventListener("click", function () {
        input.value = Math.min(max, parseInt(input.value || "1", 10) + 1);
      });
    });

    // ---- Descrição: "Ler mais" só quando o texto é grande ----
    var descText = document.getElementById("description-text");
    var descToggle = document.getElementById("description-toggle");
    if (descText && descToggle) {
      // Começa recolhido (.clamped). Se couber inteiro, tira o recorte e
      // esconde o botão; senão, o botão alterna entre ler mais / ler menos.
      if (descText.scrollHeight - descText.clientHeight > 4) {
        descToggle.hidden = false;
        descToggle.addEventListener("click", function () {
          var recolhido = descText.classList.toggle("clamped");
          descToggle.textContent = recolhido ? "Ler mais" : "Ler menos";
        });
      } else {
        descText.classList.remove("clamped");
      }
    }

    // ---- Entrega: mostra endereço só quando for "Entrega local" ----
    var deliveryInputs = document.querySelectorAll("input[name='delivery_method']");
    var addressBlock = document.getElementById("address-block");
    if (deliveryInputs.length && addressBlock) {
      var toggleAddress = function () {
        var sel = document.querySelector("input[name='delivery_method']:checked");
        addressBlock.style.display = sel && sel.value === "delivery" ? "block" : "none";
      };
      deliveryInputs.forEach(function (i) { i.addEventListener("change", toggleAddress); });
      toggleAddress();
    }
  }

  // ======================================================================
  // Navegação instantânea (SPA leve)
  // ======================================================================
  var bar;
  function progress(active) {
    bar = bar || document.getElementById("spa-bar");
    if (!bar) return;
    if (active) {
      bar.style.transition = "none"; bar.style.width = "0"; bar.style.opacity = "1";
      requestAnimationFrame(function () { bar.style.transition = "width .4s ease, opacity .3s ease"; bar.style.width = "75%"; });
    } else {
      bar.style.width = "100%";
      setTimeout(function () { bar.style.opacity = "0"; bar.style.width = "0"; }, 220);
    }
  }

  function runScripts(container) {
    container.querySelectorAll("script").forEach(function (old) {
      var s = document.createElement("script");
      if (old.src) { s.src = old.src; } else { s.textContent = old.textContent; }
      document.body.appendChild(s);
    });
  }

  function swap(html, finalUrl, push) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    var newApp = doc.getElementById("app");
    var current = document.getElementById("app");
    if (!newApp || !current) { window.location.assign(finalUrl); return; }

    var apply = function () {
      current.replaceWith(newApp);
      document.title = doc.title;
      runScripts(newApp);
      initPage();
    };
    if (document.startViewTransition) { document.startViewTransition(apply); } else { apply(); }
    if (push) { history.pushState({ spa: true }, "", finalUrl); }
    window.scrollTo({ top: 0 });
  }

  function navigate(url, opts) {
    opts = opts || {};
    progress(true);
    var init = { headers: { "X-SPA": "1" }, credentials: "same-origin", redirect: "follow" };
    if (opts.method === "POST") { init.method = "POST"; init.body = opts.body; }
    fetch(url, init)
      .then(function (r) { return r.text().then(function (t) { return { html: t, url: r.url || url }; }); })
      .then(function (res) { swap(res.html, res.url, opts.push !== false); progress(false); })
      .catch(function () { window.location.assign(url); });
  }

  // ---- Interceptar cliques em links internos ----
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || a.hasAttribute("onclick")) return;
    if (a.target === "_blank" || a.hasAttribute("download") || a.hasAttribute("data-no-spa")) return;
    if (/^(mailto:|tel:)/i.test(href)) return;
    var url;
    try { url = new URL(a.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    e.preventDefault();
    navigate(url.href, { push: true });
  });

  // ---- Interceptar envio de formulários ----
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (form.hasAttribute("data-no-spa")) return;
    var method = (form.getAttribute("method") || "GET").toUpperCase();
    var url;
    try { url = new URL(form.getAttribute("action") || location.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    e.preventDefault();
    if (method === "GET") {
      var params = new URLSearchParams(new FormData(form));
      url.search = params.toString();
      navigate(url.href, { push: true });
    } else {
      navigate(url.href, { method: "POST", body: new FormData(form), push: true });
    }
  });

  // ---- Voltar / avançar do navegador ----
  window.addEventListener("popstate", function () { navigate(location.href, { push: false }); });

  // ---- PWA ----
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/service-worker.js").catch(function () {});
    });
  }

  // ---- Primeira carga ----
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPage);
  } else {
    initPage();
  }
})();
