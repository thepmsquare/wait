const CACHE_NAME = 'my-pwa-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/favicon.ico', // You might want to cache favicon too
  // Add paths to your essential CSS and JS files here, e.g.,
  // '/static/css/style.css',
  // '/static/js/main.js',
  // Add Bootstrap CSS if served locally
  // '/static/bootstrap/css/bootstrap.min.css',
  // Add Bootstrap JS if served locally
  // '/static/bootstrap/js/bootstrap.bundle.min.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // No cache match - fetch from network
        return fetch(event.request);
      })
  );
});