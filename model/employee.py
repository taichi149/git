# 文件：model/employee.py
# Model 层：员工实体类，只存放属性，不写业务逻辑


class Employee:
    def __init__(self, id=None, employee_id=None, name=None, age=None,
                 position=None, salary=None, department=None, email=None,
                 contact_address=None, emergency_contact=None, is_archived=0):
        self.id = id
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary
        self.department = department
        self.email = email
        self.contact_address = contact_address
        self.emergency_contact = emergency_contact
        self.is_archived = is_archived