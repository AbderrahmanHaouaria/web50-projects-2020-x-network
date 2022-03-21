document.querySelectorAll(".editBtn").forEach( (element) => {

    element.addEventListener("click", (event) => {

        if (event.target.value === "Edit"){

            const oldContent = event.target.parentElement.children[1].innerText;

            event.target.parentElement.children[1].outerHTML = `<textarea id='edited-content' class='form-control' rows='2'>${oldContent}</textarea>`;
            event.target.value = "Save";
        } else {

            const postId = event.target.parentElement.querySelector(".post-id").value;

            const newContent = event.target.parentElement.children[1].value;

            event.target.parentElement.children[1].outerHTML = `<p>${newContent}</p>`;
            event.target.value = "Edit";

            fetch(`/update-post/${postId}/${newContent}`, {
                method: 'POST'
            })
            .then(respone => respone.json())
            .then(result => {
                console.log(result);
            });
        }

    });

});

document.querySelectorAll(".likeBtn").forEach( (element) => {

    element.addEventListener("click", (event) => {

        const postId = event.target.parentElement.querySelector(".post-id").value;

        if (event.target.value === "Unlike"){

            event.target.parentElement.querySelector(".post-likes").innerHTML--;
            event.target.value = "Like";

            fetch(`update-like/${postId}/Unlike`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
        } else {

            event.target.parentElement.querySelector(".post-likes").innerHTML++;
            event.target.value = "Unlike";

            fetch(`update-like/${postId}/Like`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
        }

    });

});