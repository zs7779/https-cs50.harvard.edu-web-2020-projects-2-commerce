document.addEventListener('DOMContentLoaded', () => {
    let diff = new Date().getTime() - new Date(document.querySelector("#id_post_time").innerHTML).getTime();
    let days = Math.floor(diff / 864e5);
    let hours = Math.floor(diff % 864e5 / 36e5);
    let minutes = Math.floor(diff % 36e5 / 6e4);
    let seconds = Math.floor(diff % 6e4 / 1e3);
    console.log(days, hours, minutes, seconds);
    let diff_str = "";
    if (days > 0) {
        diff_str = days + " days ago";
    } else if (hours > 0) {
        diff_str = hours + " hours ago";
    } else if (minutes > 0) {
        diff_str = minutes + " minutes ago";
    } else {
        diff_str = "just now";
    }
    document.querySelector("#id_post_time_diff").innerHTML = diff_str;
});