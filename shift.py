# 文件：model/shift.py
# Model 层：排班实体类


class Shift:
    def __init__(self, id=None, employee_id=None, shift_date=None, shift_type=None):
        self.id = id
        self.employee_id = employee_id
        self.shift_date = shift_date
        self.shift_type = shift_type