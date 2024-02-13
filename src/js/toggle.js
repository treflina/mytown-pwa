Array.from(document.querySelectorAll("button.Toggle")).forEach((button) => {
    button.addEventListener("click", (event) => {
        if (button.getAttribute("aria-pressed") === "true") {
            button.removeAttribute("aria-pressed");
            // button.innerText = "Wyłącz powiadomienia";
        } else {
            button.setAttribute("aria-pressed", "true");
            // button.innerText="Włącz powiadomienia"
        }
    });
});
