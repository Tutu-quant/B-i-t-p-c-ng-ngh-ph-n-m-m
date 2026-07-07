class Attendance:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def check_in(self, time=None):
        return {
            "employee_id": self.employee_id,
            "status": "checked_in",
            "time": time,
        }
