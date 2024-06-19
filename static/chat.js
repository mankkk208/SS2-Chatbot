window.onload = function () {
    const input = document.getElementById("submit-text");
    var submitButton = document.getElementById("submit");
    var chatzone = document.getElementById("chatzone");


    function appendUserMessage(text) {
        let div = document.createElement("div")
        div.innerHTML = `
        <div class="messages">
            <img class="user_avatar" src="avatar.jpg"></img>
            <div class="user_info">
                <div class="user_name">You</div>
                <div class="user_promt">${text.replace(/\n/g, "<br>")}</div>
            </div>
        </div>
        `
        chatzone.appendChild(div);
    };

    function appendAIMessage(text) {
        let div = document.createElement("div")
        div.innerHTML = `
        <div class="messages">
            <img class="user_avatar" src="logo.jpg"></img>
            <div class="user_info">
                <div class="user_name">SS2-Chatbot</div>
                <div class="user_promt">${text.replace(/\n/g, "<br>")}</div>
            </div>
        </div>
        `
        chatzone.appendChild(div);
    };

    function disableButton() {
        submitButton.classList.add("invalid");
        submitButton.disabled = true;
    }

    function enableButton() {
        submitButton.classList.remove("invalid");
        submitButton.disabled = false;
    }
    
    
    $('#textForm').submit(function(event) {
        event.preventDefault();
        disableButton();
        input.disabled = true;
        let text = input.value;
        appendUserMessage(text);
        $.ajax({
            type: 'POST',
            url: '/api/chat',
            contentType: 'application/json',
            data: JSON.stringify({ text: text }),
            success: function(response) {
                // Append the user's message to the chat box
                appendAIMessage(response.response);

                // Scroll to the bottom of the chat box
                $('#chatzone').scrollTop($('#chatzone')[0].scrollHeight);

                // Clear the input field
                input.value = '';

                // Restore button
                enableButton();
                input.disabled = false;
            },
            error: function(xhr, status, error) {
                // Restore button
                enableButton();
                input.disabled = false;
                // Handle error responses from backend
                console.error('Chat failed:', error);
                alert('Failed to send message. Please try again.');
            }
        });
    });
    input.addEventListener("input", function (event) {
        if (event.target.value === "") {
            disableButton();
        } else {
            enableButton();
        }
    });

    var sidebar = document.getElementsByClassName("sidebar")[0];

    document.getElementById("toggle-nav").addEventListener("click", function(event) {
        sidebar.hidden = !sidebar.hidden;
    })
};
