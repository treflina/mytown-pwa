self.addEventListener("push", function (event) {
    let payload = event.data
            ? event.data.text()
            : { head: "No Content", body: "No Content", icon: "" },
        data = JSON.parse(payload),
        head = data.head,
        body = data.body,
        icon = data.icon;
    url = data.url ? data.url : self.location.origin;

    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: icon,
            data: { url: url },
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
