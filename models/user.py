class User:
    @staticmethod
    def register(username, email, phone, password, confirm_password):
        print(f"Registering user: {username}, {email}, {phone}")
        if password != confirm_password:
            return False, "Passwords do not match"
        return True, "Registration successful"
