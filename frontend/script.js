
var origin_url = document.getElementById("original-url");
var short_btn = document.getElementById("shorten-btn");

var result_card = document.getElementById("result-card");
var short_url_input = document.getElementById("short-url");
var copy_btn = document.getElementById("copy-btn");
var copy_message = document.getElementById("copy-message");

const API_BASE_URL = "https://url-shortner-2pdj.onrender.com";
short_btn.addEventListener("click", async function() {

    var url = origin_url.value.trim();

    if (url === "") {
        alert("Please enter a URL");
        return;
    }

    result_card.style.display = "none";
    copy_btn.style.display = "none";
    copy_message.textContent = "";

    try {

        const response = await fetch(`${API_BASE_URL}/url`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                original_url: url
            })

        });

        const data = await response.json();

        if (!response.ok) {

            short_url_input.value = data.detail;
            result_card.style.display = "block";
            return;
        }

        short_url_input.value = `${API_BASE_URL}/url/${data.short_url}`;

        result_card.style.display = "block";
        copy_btn.style.display = "block";

    }

    catch(error) {

        alert("Something went wrong!");

    }

});


copy_btn.addEventListener("click", async function() {

    try {

        await navigator.clipboard.writeText(short_url_input.value);

        copy_message.textContent = "Link copied successfully!";

    }

    catch(error) {

        copy_message.textContent = "Unable to copy link!";

    }

});
