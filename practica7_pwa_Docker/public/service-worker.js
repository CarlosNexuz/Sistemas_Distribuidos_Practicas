/* eslint-disable no-restricted-globals */

// Este código se ejecuta en un hilo separado (el Service Worker).

const CACHE_NAME = 'insta-pwa-cache-v1';
// Lista de archivos esenciales para que la app funcione offline.
// 'index.html' y '/' se refieren a la página principal.
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/logo12.png',
  '/logo12.png',
];

// 1. Instalación del Service Worker
self.addEventListener('install', event => {
  console.log('Service Worker: Instalando...');
  // Espera hasta que la promesa se resuelva.
  event.waitUntil(
    // Abrimos la caché con nuestro nombre.
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Cache abierto, cacheando app shell.');
        // Agregamos todos los archivos importantes a la caché.
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        // Forzar al nuevo service worker a activarse inmediatamente.
        self.skipWaiting();
      })
  );
});

// 2. Activación del Service Worker
self.addEventListener('activate', event => {
  console.log('Service Worker: Activando...');
  event.waitUntil(
    // Obtenemos todos los nombres de las cachés existentes.
    caches.keys().then(cacheNames => {
      return Promise.all(
        // Mapeamos sobre ellas.
        cacheNames.map(cacheName => {
          // Si una caché no es la nuestra, la borramos.
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Borrando caché antigua:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  // Tomar control de las páginas abiertas inmediatamente.
  return self.clients.claim();
});

// 3. Interceptar peticiones (Fetch)
self.addEventListener('fetch', event => {
  // Solo aplicamos la estrategia para peticiones GET.
  if (event.request.method !== 'GET') {
      return;
  }
  
  // Estrategia: Network falling back to cache (Intenta la red primero, si falla, usa la caché)
  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // Si la petición a la red funciona, la clonamos y la guardamos en caché para el futuro.
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      })
      .catch(() => {
        // Si la red falla (estamos offline), intentamos servir desde la caché.
        return caches.match(event.request);
      })
  );
});
