// King Street — Ajuste de foto do produto (recorte quadrado)
// Tela simples para o admin posicionar a foto: arrasta para os lados / cima e
// baixo e aproxima com a barra. A foto sai quadrada, do jeito que aparece na
// loja. Sem bibliotecas externas — funciona offline (PWA).
(function () {
  "use strict";

  var OUT = 1000; // tamanho final da imagem (px)

  function overlay() {
    var el = document.createElement("div");
    el.className = "cropper-overlay";
    el.innerHTML =
      '<div class="cropper-box">' +
      '  <div class="cropper-head">' +
      '    <strong>Ajustar foto</strong>' +
      '    <span class="cropper-count" id="cropper-count"></span>' +
      '  </div>' +
      '  <div class="cropper-frame" id="cropper-frame">' +
      '    <img id="cropper-img" alt="" draggable="false">' +
      '    <div class="cropper-grid"></div>' +
      '  </div>' +
      '  <div class="cropper-zoom">' +
      '    <span>➖</span>' +
      '    <input type="range" id="cropper-range" min="1" max="3" step="0.01" value="1">' +
      '    <span>➕</span>' +
      '  </div>' +
      '  <p class="cropper-hint">Arraste a foto para enquadrar e use a barra para aproximar.</p>' +
      '  <div class="cropper-actions">' +
      '    <button type="button" class="btn" id="cropper-cancel">Cancelar</button>' +
      '    <button type="button" class="btn btn-primary" id="cropper-ok">Confirmar</button>' +
      '  </div>' +
      '</div>';
    return el;
  }

  function open(files, opts) {
    files = Array.prototype.slice.call(files);
    if (!files.length) return;
    var onDone = (opts && opts.onDone) || function () {};
    var onCancel = (opts && opts.onCancel) || function () {};

    var el = overlay();
    document.body.appendChild(el);
    document.body.style.overflow = "hidden";

    var frame = el.querySelector("#cropper-frame");
    var img = el.querySelector("#cropper-img");
    var range = el.querySelector("#cropper-range");
    var count = el.querySelector("#cropper-count");

    var resultados = [];
    var i = 0;
    // Estado do enquadramento atual
    var nw = 0, nh = 0, F = 0, coverScale = 1, zoom = 1, ox = 0, oy = 0;

    function fecha() {
      document.body.removeChild(el);
      document.body.style.overflow = "";
    }

    function scale() { return coverScale * zoom; }

    function limita() {
      var dw = nw * scale(), dh = nh * scale();
      // A foto sempre cobre o quadro
      ox = Math.min(0, Math.max(F - dw, ox));
      oy = Math.min(0, Math.max(F - dh, oy));
    }

    function pinta() {
      limita();
      img.style.width = nw * scale() + "px";
      img.style.height = nh * scale() + "px";
      img.style.left = ox + "px";
      img.style.top = oy + "px";
    }

    function carrega(file) {
      var reader = new FileReader();
      reader.onload = function (ev) {
        img.onload = function () {
          nw = img.naturalWidth; nh = img.naturalHeight;
          F = frame.clientWidth;
          coverScale = F / Math.min(nw, nh);
          zoom = 1; range.value = "1";
          // Começa centralizado
          ox = (F - nw * scale()) / 2;
          oy = (F - nh * scale()) / 2;
          pinta();
        };
        img.src = ev.target.result;
      };
      reader.readAsDataURL(file);
      count.textContent = files.length > 1 ? (i + 1) + " de " + files.length : "";
    }

    function recorta(file) {
      var s = scale();
      var sSize = F / s;              // lado do recorte em px naturais
      var sx = (-ox) / s;
      var sy = (-oy) / s;
      var canvas = document.createElement("canvas");
      canvas.width = OUT; canvas.height = OUT;
      var ctx = canvas.getContext("2d");
      ctx.drawImage(img, sx, sy, sSize, sSize, 0, 0, OUT, OUT);
      return new Promise(function (resolve) {
        canvas.toBlob(function (blob) {
          var nome = (file.name || "foto").replace(/\.[^.]+$/, "") + ".jpg";
          resolve(new File([blob], nome, { type: "image/jpeg" }));
        }, "image/jpeg", 0.9);
      });
    }

    function proxima() {
      i += 1;
      if (i >= files.length) {
        fecha();
        onDone(resultados);
      } else {
        carrega(files[i]);
      }
    }

    // ---- Zoom ----
    range.addEventListener("input", function () {
      var frameCenterX = F / 2, frameCenterY = F / 2;
      // Mantém o centro do quadro fixo ao aproximar
      var antes = scale();
      zoom = parseFloat(range.value);
      var depois = scale();
      var r = depois / antes;
      ox = frameCenterX - (frameCenterX - ox) * r;
      oy = frameCenterY - (frameCenterY - oy) * r;
      pinta();
    });

    // ---- Arraste (dedo / mouse) ----
    var dragging = false, px = 0, py = 0;
    function start(x, y) { dragging = true; px = x; py = y; }
    function move(x, y, e) {
      if (!dragging) return;
      ox += x - px; oy += y - py;
      px = x; py = y;
      if (e && e.cancelable) e.preventDefault();
      pinta();
    }
    function end() { dragging = false; }

    frame.addEventListener("touchstart", function (e) { start(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
    frame.addEventListener("touchmove", function (e) { move(e.touches[0].clientX, e.touches[0].clientY, e); }, { passive: false });
    frame.addEventListener("touchend", end);
    frame.addEventListener("mousedown", function (e) { start(e.clientX, e.clientY); e.preventDefault(); });
    window.addEventListener("mousemove", _mm);
    window.addEventListener("mouseup", _mu);
    function _mm(e) { if (dragging) move(e.clientX, e.clientY, e); }
    function _mu() { end(); }

    // ---- Botões ----
    el.querySelector("#cropper-ok").addEventListener("click", function () {
      recorta(files[i]).then(function (f) {
        resultados.push(f);
        proxima();
      });
    });
    el.querySelector("#cropper-cancel").addEventListener("click", function () {
      cleanup();
      fecha();
      onCancel();
    });

    function cleanup() {
      window.removeEventListener("mousemove", _mm);
      window.removeEventListener("mouseup", _mu);
    }
    // Garante limpeza dos listeners globais ao concluir
    var _onDone = onDone;
    onDone = function (res) { cleanup(); _onDone(res); };

    carrega(files[0]);
  }

  window.KSCropper = { open: open };
})();
