# 文件：model/shift.py
# Model 层：排班实体类


class Shift:
    # employee_code / employee_name 不是排班表的字段，
    # 只在「全店排班视图」联查员工表时顺带带出来，方便页面显示，平时是 None。
    def __init__(self, id=None, employee_id=None, shift_date=None, shift_type=None,
                 employee_code=None, employee_name=None):
        self.id = id
        self.employee_id = employee_id
        self.shift_date = shift_date
        self.shift_type = shift_type
        self.employee_code = employee_code
        self.employee_name = employee_name
