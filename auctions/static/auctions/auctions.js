document.addEventListener('DOMContentLoaded', () => {
    let now = new Date().getTime();
    document.querySelectorAll(".class_post_time").forEach((post_time) => {
        let diff = now - new Date(post_time.innerHTML).getTime();
        let days = Math.floor(diff / 864e5);
        let hours = Math.floor(diff % 864e5 / 36e5);
        let minutes = Math.floor(diff % 36e5 / 6e4);
        let seconds = Math.floor(diff % 6e4 / 1e3);
        if (days > 0) {
            post_time.innerHTML = days + " days ago";
        } else if (hours > 0) {
            post_time.innerHTML = hours + " hours ago";
        } else if (minutes > 0) {
            post_time.innerHTML = minutes + " minutes ago";
        } else {
            post_time.innerHTML = "just now";
        }
    })
});

function bid_button() {
    if (document.querySelector("#id_value").value == "") {
        return false;
    } else {
        document.querySelector("#id_bid_watch_form").submit();
    }
}

function non_bid_button() {
    document.querySelector("#id_value").value = "";
    document.querySelector("#id_bid_watch_form").submit();
}