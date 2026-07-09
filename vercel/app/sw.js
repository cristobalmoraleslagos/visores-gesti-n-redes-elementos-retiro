// Service Worker · Fiscalización Municipal · offline-first
const CACHE = 'fiscal-v1';
const SHELL = [
  '/app/',
  '/app/index.html',
  '/app/config.js',
  '/app/manifest.json',
  '/app/icon-192.png',
  '/app/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// App shell: cache-first. Supabase/API: siempre red (nunca cachear datos ni auth).
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.pathname.startsWith('/rest/') ||
      url.hostname.endsWith('supabase.co') || url.hostname.endsWith('supabase.in')) return;
  e.respondWith(
    caches.match(e.request).then(hit => hit ||
      fetch(e.request).then(res => {
        if (res.ok && url.origin === location.origin) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => caches.match('/app/index.html'))
    )
  );
});
