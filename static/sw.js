const CACHE_NAME = "wait-cache-v3";

// Only same-origin static assets are cached. Authenticated pages are never
// stored so that private weight data cannot be served from a shared device's
// cache.
const STATIC_ASSETS = [
  "/static/css/style.css",
  "/static/favicon.ico",
  "/static/manifest.json",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
];

// install event - cache static assets (best effort)
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      Promise.allSettled(STATIC_ASSETS.map((asset) => cache.add(asset))),
    ),
  );
  self.skipWaiting();
});

// activate event - cleanup old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("[service worker] clearing old cache:", cache);
            return caches.delete(cache);
          }
          return Promise.resolve();
        }),
      ),
    ),
  );
  self.clients.claim();
});

// fetch event - stale-while-revalidate for same-origin static assets only
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  if (event.request.method !== "GET" || url.origin !== self.location.origin) {
    return;
  }

  // Never intercept navigations: they contain private, authenticated data.
  if (event.request.mode === "navigate") {
    return;
  }

  if (!url.pathname.startsWith("/static/")) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (networkResponse.ok) {
          const copy = networkResponse.clone();
          caches
            .open(CACHE_NAME)
            .then((cache) => cache.put(event.request, copy));
        }
        return networkResponse;
      });
      return cachedResponse || fetchPromise;
    }),
  );
});
