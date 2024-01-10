// {% load static %}
self.addEventListener('install', e => {
    const cacheProm = caches.open('cache-1')
        .then(cache => {
            return cache.addAll([
                '/',
                '/regions',
                '{% static "img/tur4.jpg" %}',
                '{% static "img/svg/sprite.svg" %}',
                '{% static "css/styles.min.css" %}',
                '{% static "img/logot.png" %}',
                '{% static "js/script.js" %}'
                // '{% static "js/app.js"%}',
            ])
        }
    )

e.waitUntil(cacheProm);
});

self.addEventListener('fetch', e => {
    console.log(e.request);

    //   const requestUrl = new URL(e.request.url);
    //   if (requestUrl.origin === location.origin) {
    //       if (requestUrl.pathname === "/") {
    //           e.respondWith(caches.match("/"));
    //           console.log("matched")
    //           return;
    //       }
    //   }

    e.respondWith(caches.match(e.request).then(function (response) {
        return response ;
    }))
})