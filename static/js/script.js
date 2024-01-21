const mainImg = document.querySelector('.home__image-img');

const onResize = () => {
    if (mainImg && window.screen.width > 1000) {
        mainImg.src = "static/img/tur4.jpg";
    }
}
window.addEventListener("load", onResize);
window.addEventListener("resize", onResize);
