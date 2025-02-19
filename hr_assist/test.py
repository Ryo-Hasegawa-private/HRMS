from .models import Employee

emp_ages = []
for employee in Employee.objects.all():
    emp_age = employee.calculate_age()
    emp_ages.append(emp_age)
    
print(emp_ages)
    