{% load static %}
self.addEventListener("push", function (event) {
    let payload = event.data
            ? event.data.text()
            : { head: "No Content", body: "No Content", icon: "" },
        data = JSON.parse(payload),
        head = data.head,
        body = data.body,
        {% comment %} icon = data.icon, {% endcomment %}
        badge = data.badge,
    url = data.url ? data.url : self.location.origin;
    console.log(`${"{% static 'img/icos/android-chrome96x96.png' %}"}`)

    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: 'https://i.imgur.com/MZM3K5w.png',
            badge: '{% static "img/trash.ico" %}',
            image: 'https://i.imgur.com/MZM3K5w.png',
            data: { url: url }
        })
    );
});

self.addEventListener("notificationclick", function (event) {
    event.waitUntil(
        event.preventDefault(),
        event.notification.close(),
        self.clients.openWindow(event.notification.data.url)
    );
});
