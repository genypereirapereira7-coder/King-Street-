// King Street — Service Worker (PWA)
// v4: estáticos usam "network-first" e o painel (/painel/) nunca passa pelo
// service worker — sempre vai direto à rede, para o admin ver dados atuais.
const CACHE = "kingstreet-v4";
const OFFLINE_URL = "/offline/";

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.add(OFFLINE_URL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  // Painel administrativo: nunca intercepta — o navegador busca sempre do servidor
  if (new URL(req.url).pathname.startsWith("/painel/")) return;

  // Navegações: rede primeiro, cai para a página offline
  if (req.mode === "navigate") {
    event.respondWith(fetch(req).catch(() => caches.match(OFFLINE_URL)));
    return;
  }

  // Estáticos: rede primeiro (atualiza o cache), cai para o cache se offline
  if (req.url.includes("/static/")) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req))
    );
  }
});
