from werkzeug.security import generate_password_hash


class User:
    def __init__(self, username, email, phone, password_hash=None):
        self.username = username
        self.email = email
        self.phone = phone
        self.password_hash = password_hash

    @staticmethod
    def register(username, email, phone, password, confirm_password):
        if not username or not email or not phone or not password:
            raise ValueError("Vui lòng điền đầy đủ thông tin")
        if password != confirm_password:
            raise ValueError("Mật khẩu xác nhận không khớp")

        password_hash = generate_password_hash(password)
        return User(
            username=username,
            email=email,
            phone=phone,
            password_hash=password_hash,
        )
