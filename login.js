document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the normal way

    var account = document.getElementById('account').value;
    var password = document.getElementById('password').value;

    if (account === 'test_cloud_infra' && password === 'cloud@infra12') {
        window.location.href = 'dash.html'; // Redirect to dash.html
    } else {
        alert('Incorrect account name or password');
    }
});

// Show/Hide Password functionality
document.getElementById('showPassword').addEventListener('change', function() {
    var passwordInput = document.getElementById('password');
    if (this.checked) {
        passwordInput.type = 'text'; // Show password
    } else {
        passwordInput.type = 'password'; // Hide password
    }
});

