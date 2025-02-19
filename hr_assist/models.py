from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Employee(models.Model):
    """従業員情報を表すモデル"""
    sei = models.CharField(max_length=20)
    mei = models.CharField(max_length=20)
    birth_date = models.DateField()
    MALE = '男性'
    FEMALE = '女性'

    GENDER_CHOICES = [
        (MALE, '男性'),
        (FEMALE, '女性'),
    ]
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE
    )
    email = models.EmailField()
    basic_salary = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000000)])
    joining_date = models.DateField()
    
    # ステータスの選択肢
    STAYED = 'STAYED'  # 在職中
    ABSENCE = 'ABSENCE'  # 休職中
    GOING_TO_LEAVE = 'GOING TO LEAVE'  # 退職予定
    LEAVED = 'LEAVED'  # 退職済み

    STATUS_CHOICES = [
        (STAYED, '在職中'),
        (ABSENCE, '休職中'),
        (GOING_TO_LEAVE, '退職予定'),
        (LEAVED, '退職済み'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STAYED
    )
    
    def calculate_age(self):
        """年齢を計算して返す"""
        today = date.today()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or ((today.month == self.birth_date.month) and (today.day < self.birth_date.day)):
            age -= 1
        return age
    
    def get_status_display(self):
        if self.status == 'STAYED':
            return '在職中'
        elif self.status == 'ABSENCE':
            return '休職中'
        elif self.status == 'GOING TO LEAVE':
            return '退職予定'
        elif self.status == 'LEAVED':
            return '退職済み'
        return '不明'
    
    # `User` モデルとの関連
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    
    def __str__(self):
        """モデルの文字列表現を返す"""
        return f'{self.sei} {self.mei}'

class Allowance(models.Model):
    """手当を表すモデル"""
    name = models.CharField(max_length=100)  # 手当名
    amount = models.IntegerField()  # 支給額
    paymonth = models.CharField(max_length=7) # 例) 2025-02
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # 従業員ID（FK）
    
    def __str__(self):
        return self.name

    @staticmethod
    def total_allowance(emp_id, paymonth):
        """手当の合計"""
        allowances = Allowance.objects.filter(employee_id=emp_id, paymonth=paymonth)
        total_allowance = 0
        for allowance in allowances:
            if allowance.amount > 0:
                total_allowance += allowance.amount
        return total_allowance
    
    @staticmethod
    def total_deduction(emp_id, paymonth):
        """控除の合計"""
        deductions = Allowance.objects.filter(employee_id=emp_id, paymonth=paymonth)
        total_deduction = 0
        for deduction in deductions:
            if deduction.amount < 0:
                total_deduction += deduction.amount
        return total_deduction     
                
        


    
        

class AllowanceList(models.Model):
    """手当リストを表すモデル"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # 従業員ID（FK）
    allowance = models.ForeignKey(Allowance, on_delete=models.CASCADE)  # 手当ID（FK）

    class Meta:
        # 'employee' と 'allowance' の組み合わせがユニークであることを指定
        constraints = [
            models.UniqueConstraint(fields=['employee', 'allowance'], name='unique_employee_allowance')
        ]
        
    def __str__(self):
        return f'{self.employee.sei} {self.employee.mei}-{self.allowance.name}({self.allowance.paymonth})'
        
class Salary:
    """給与のクラス"""
    
    def __init__(self, employee, paymonth):
        self.employee = employee
        self.paymonth = paymonth
    
    def calculate(self):
        """給料計算をして返す"""
        basic_salary = self.employee.basic_salary
        total_allowance = Allowance.total_allowance(self.employee, self.paymonth)
        total_salary = basic_salary + total_allowance
        return total_salary
