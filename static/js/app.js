import { urlB64ToUint8Array, getCookie } from "./utils.js";

let isPushEnabled = false,
    registration,
    subBtn,
    btnText;


window.addEventListener("load", function () {
    subBtn = document.getElementById("webpush-subscribe-btn");
    btnText = document.querySelector(".btn-text");

    subBtn?.addEventListener("click", function () {
        subBtn.disabled = true;
        if (isPushEnabled) {
            return unsubscribe(registration);
        }
        return subscribe(registration);
    });

    // Do everything if the Browser Supports Service Worker
    if ("serviceWorker" in navigator) {
        const serviceWorker = document.querySelector('meta[name="sw"]').content;
        navigator.serviceWorker.register(serviceWorker).then(function (reg) {
            registration = reg;
            if (subBtn !== null) {
                initialiseState(reg);
            }
        });
    }
    // If service worker not supported, show warning to the message box
    else {
        showMessage(
            gettext("Service workers are not supported in your browser.")
        );
    }

    // Once the service worker is registered set the initial state
    function initialiseState(reg) {
        // Are Notifications supported in the service worker?
        if (!reg.showNotification) {
            subBtn.setAttribute("aria-pressed", false);
            showMessage(
                gettext(
                    "Showing notifications are not supported in your browser."
                )
            );
            return;
        }

        // Check the current Notification permission.
        // If its denied, it's a permanent block until the
        // user changes the permission
        if (Notification.permission === "denied") {
            subBtn.disabled = false;
            subBtn.setAttribute("aria-pressed", false);
            showMessage(
                gettext("Push notifications are blocked by your browser.")
            );
            return;
        }

        // Check if push messaging is supported
        if (!("PushManager" in window)) {
            subBtn.disabled = false;
            subBtn.setAttribute("aria-pressed", false);
            showMessage(
                gettext("Push notifications are not available in your browser.")
            );
            return;
        }

        // We need to get subscription state for push notifications and send the information to server
        reg.pushManager.getSubscription().then(function (subscription) {
            if (subscription) {
                checkSubscription(subscription, function (response) {
                    if (response.status === 200) {
                        btnText.textContent = "Wyłącz powiadomienia";
                        subBtn.setAttribute("aria-pressed", true);
                        subBtn.disabled = false;
                        isPushEnabled = true;
                    }
                });
            }
        });
    }
});

function showMessage(message) {
    const messageBox = document.getElementById("webpush-message");
    if (messageBox) {
        messageBox.textContent = message;
        messageBox.style.display = "block";
    }
}

function subscribe(reg) {
    reg.pushManager.getSubscription().then(function (subscription) {
        var metaObj, applicationServerKey, options;
        metaObj = document.querySelector('meta[name="vapid-key"]');
        applicationServerKey = metaObj.content;
        options = {
            userVisibleOnly: true,
        };
        if (applicationServerKey) {
            options.applicationServerKey =
                urlB64ToUint8Array(applicationServerKey);
        }

        reg.pushManager
            .subscribe(options)
            .then(function (subscription) {
                postSubscribeObj(
                    "subscribe",
                    subscription,
                    function (response) {
                        // Check the information is saved successfully into server
                        if (response.status === 201) {
                            btnText.textContent = "Wyłącz powiadomienia";
                            subBtn.setAttribute("aria-pressed", "true");
                            subBtn.disabled = false;
                            isPushEnabled = true;
                            showMessage(
                                gettext(
                                    "Successfully subscribed to push notifications."
                                )
                            );
                        }
                    }
                );
            })
            .catch(function () {
                console.log(
                    gettext("Error while subscribing to push notifications."),
                    arguments
                );
            });
    });
}

function unsubscribe(reg) {
    // Get the Subscription to unregister
    reg.pushManager.getSubscription().then(function (subscription) {
        // Check we have a subscription to unsubscribe
        if (!subscription) {
            // No subscription object, so set the state
            // to allow the user to subscribe to push
            subBtn.disabled = false;
            subBtn.setAttribute("aria-pressed", false);
            btnText.textContent = "Włącz powiadomienia";
            showMessage(gettext("Subscription is not available."));
            return;
        }
        postSubscribeObj("unsubscribe", subscription, function (response) {
            // Check if the information is deleted from server
            if (response.status === 202) {
                // Get the Subscription
                // Remove the subscription
                subscription
                    .unsubscribe()
                    .then(function (successful) {
                        showMessage(
                            gettext(
                                "Successfully unsubscribed from push notifications."
                            )
                        );
                        isPushEnabled = false;
                        subBtn.disabled = false;
                        subBtn.setAttribute("aria-pressed", false);
                        btnText.textContent = "Włącz powiadomienia";
                    })
                    .catch(function (error) {
                        showMessage(
                            gettext(
                                "Error while unsubscribing from push notifications."
                            )
                        );
                        subBtn.disabled = false;
                    });
            }
        });
    });
}

function checkSubscription(subscription, callback) {
    const data = {
        subscription: subscription.toJSON(),
        group: subBtn.dataset.group,
    };
    const headers = new Headers();
    const csrftoken = getCookie("csrftoken");
    headers.append("X-CSRFToken", csrftoken);
    headers.append("Content-Type", "application/json");

    fetch("/subscription-check", {
        method: "post",
        mode: "same-origin",
        headers: headers,
        body: JSON.stringify(data),
    }).then(callback);
}

function postSubscribeObj(statusType, subscription, callback) {
    const browser = navigator.userAgent
            .match(/(firefox|msie|chrome|safari|trident)/gi)[0]
            .toLowerCase(),
        user_agent = navigator.userAgent,
        data = {
            status_type: statusType,
            subscription: subscription.toJSON(),
            browser: browser,
            user_agent: user_agent,
            group: subBtn.dataset.group,
        };
    const headers = new Headers();
    const csrftoken = getCookie("csrftoken");
    headers.append("X-CSRFToken", csrftoken);
    headers.append("Content-Type", "application/json")
    fetch(subBtn.dataset.url, {
        method: "post",
        mode: "same-origin",
        headers: headers,
        body: JSON.stringify(data),
    }).then(callback);
}


