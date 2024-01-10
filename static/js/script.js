document.addEventListener("DOMContentLoaded", function (event) {
    const garbageCol = () => {
        
        fetch("/api/garbagecollection/3")
            .then((res) => console.log(res))
            .catch(console.log("sth"));
    };
    garbageCol();
});
