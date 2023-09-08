var icon = document.getElementById("icon");

const handleChangeTheme = async (event) => {
    event.preventDefault();

    const response = await fetch("/theme", {
        method: "PUT",
    });

    displayTheme();
};

icon.addEventListener("click", handleChangeTheme);

const displayTheme = async () => {
    const response = await fetch("/theme", {
        method: "GET",
    });
    const theme = await response.text();

    if (theme == "dark") {
        document.body.classList.toggle("dark-theme");
        icon.src = "static/images/sun.png"
    } else if (theme == "light") {
        document.body.classList.remove("dark-theme");
        icon.src = "static/images/moon.png"
    }
};

displayTheme();