$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = {
            username: $('#username').val(),
            password: $('#password').val()
        };

        // Send form data to backend API endpoint
        $.ajax({
            type: 'POST',
            url: '/api/login',
            data: formData,
            success: function(response) {
                // Handle successful login response
                if (response.status === "success" && response.access_token) {
                    // Set access token in cookie
                    setToken('Authorization', response.access_token, 3); // Cookie expires in 3 days

                    // Redirect to dashboard or any other secure page
                    window.location.href = '/chat.html';
                } else {
                    // Handle invalid login scenario
                    alert('Invalid credentials. Please try again.');
                }
            },
            error: function(xhr, status, error) {
                // Handle error responses from backend
                console.error('Login failed:', error);
                alert('Login failed. Please try again.');
            }
        });
    });

    // Function to set cookie
    function setToken(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }
});