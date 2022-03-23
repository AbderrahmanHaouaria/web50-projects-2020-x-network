document.addEventListener("DOMContentLoaded", function(){

    const owner = document.getElementById("owner-username").value;
    // const visitor = document.getElementById("visitor-username").value;

    document.getElementById("follow-btn").addEventListener("click", () => {
        fetch(`${owner}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });

        let followers = 0;

        if (document.querySelector("#follow-btn").value === "Follow") {

            document.getElementById("follow-btn").value = "Unfollow";

            followers = parseInt(document.getElementById("followers-count").innerHTML) + 1;
        } else {

            document.getElementById("follow-btn").value = "Follow";

            followers = parseInt(document.getElementById("followers-count").innerHTML) - 1;
        }

        document.getElementById("followers-count").innerHTML = followers;
    });

});