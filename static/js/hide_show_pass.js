function togglePasswordVisibility(iconId, inputId) {
    var passwordInput = document.getElementById(inputId);
    var passwordIcon = document.getElementById(iconId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.classList.remove('bi', 'bi-eye-fill');
        passwordIcon.classList.add('bi', 'bi-eye-slash');

    } else {
        passwordInput.type = 'password';
        passwordIcon.classList.remove('bi', 'bi-eye-slash');
        passwordIcon.classList.add('bi', 'bi-eye-fill');
        console.log("hide password")
    }
}
