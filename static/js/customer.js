// ==========================================
// BREWPOINT CUSTOMER.JS
// Dùng chung cho Login & Register
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // ==========================================
    // SHOW / HIDE PASSWORD
    // ==========================================
    const passwordToggles = document.querySelectorAll(
        ".toggle-password, .toggle-confirm"
    );
    passwordToggles.forEach(toggle => {
        toggle.addEventListener("click", () => {
            const input =
                toggle.parentElement.querySelector("input");
            if (input.type === "password") {
                input.type = "text";
                toggle.classList.replace("bx-hide", "bx-show");
            } else {
                input.type = "password";
                toggle.classList.replace("bx-show", "bx-hide");
            }
        });
    });
    // ==========================================
    // INPUT EFFECT
    // ==========================================
    document.querySelectorAll("input").forEach(input => {
        input.addEventListener("focus", () => {
            input.parentElement.classList.add("active");
        });
        input.addEventListener("blur", () => {
            input.parentElement.classList.remove("active");
        });
    });
    // ==========================================
    // LOGIN
    // ==========================================
    const loginForm =
        document.getElementById("customerLogin");
    if (loginForm) {
        loginForm.addEventListener("submit", e => {
            e.preventDefault();
            const email =
                document.getElementById("email").value.trim();
            const password =
                document.getElementById("password").value.trim();
            if (email === "") {
                alert("Vui lòng nhập email.");
                return;
            }
            const emailRegex =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert("Email không đúng định dạng.");
                return;
            }
            if (password.length < 6) {
                alert("Mật khẩu phải có ít nhất 6 ký tự.");
                return;
            }
            alert("Đăng nhập thành công! (Demo)");
            // loginForm.submit();
        });
    }
    // ==========================================
    // REGISTER
    // ==========================================
    const registerForm =
        document.getElementById("customerRegister");
    if (registerForm) {
        registerForm.addEventListener("submit", e => {
            e.preventDefault();
            const fullname =
                document.getElementById("fullname").value.trim();
            const email =
                document.getElementById("email").value.trim();
            const phone =
                document.getElementById("phone").value.trim();
            const password =
                document.getElementById("password").value;
            const confirmPassword =
                document.getElementById("confirmPassword").value;
            const agree =
                document.getElementById("agree").checked;
            if (fullname === "") {
                alert("Vui lòng nhập họ tên.");
                return;
            }
            if (fullname.length < 2) {
                alert("Họ tên không hợp lệ.");
                return;
            }
            const emailRegex =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert("Email không hợp lệ.");
                return;
            }
            const phoneRegex =
                /^(0|\+84)[0-9]{9}$/;
            if (!phoneRegex.test(phone)) {
                alert("Số điện thoại không hợp lệ.");
                return;
            }
            if (password.length < 6) {
                alert("Mật khẩu phải từ 6 ký tự.");
                return;
            }
            if (password !== confirmPassword) {
                alert("Mật khẩu xác nhận không khớp.");
                return;
            }
            if (!agree) {
                alert("Bạn cần đồng ý điều khoản.");
                return;
            }
            alert("Đăng ký thành công! (Demo)");
            // registerForm.submit();
        });
    }
    // ==========================================
    // GOOGLE LOGIN
    // ==========================================
    const googleBtn =
        document.querySelector(".google-btn");
    if (googleBtn) {
        googleBtn.addEventListener("click", () => {
            alert("Tính năng sẽ được phát triển sau.");
        });
    }
    // ==========================================
    // ENTER SUBMIT
    // ==========================================
    document.addEventListener("keydown", e => {
        if (e.key !== "Enter") return;
        if (loginForm) {
            loginForm.requestSubmit();
        }
        if (registerForm) {
            registerForm.requestSubmit();
        }
    });
});