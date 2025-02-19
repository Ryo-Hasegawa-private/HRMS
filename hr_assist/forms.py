from django import forms

from .models import Employee
from .models import Allowance
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'sei',
            'mei',
            'birth_date',
            'gender',
            'basic_salary',
            'joining_date',
            'status',
        ]
        labels = {
            'sei': '姓',
            'mei': '名',
            'birth_date': '生年月日',
            'gender': '性別',
            'basic_salary': '基本給',
            'joining_date': '入社日',
            'status': 'ステータス',
        }
    
    # genderフィールドをラジオボタンで表示
    gender = forms.ChoiceField(
        choices = Employee.GENDER_CHOICES,
        widget = forms.RadioSelect,
        label = '性別',
    )
    
class SalaryForm(forms.ModelForm):
    class Meta:
        model = Allowance  # Allowance モデルを指定
        fields = ['employee', 'paymonth', 'name', 'amount']  # 使用するフィールドを指定
        
        employee = forms.ModelChoiceField(
            queryset=Employee.objects.all(),
            label='従業員',
            required=True
        )
    
        paymonth = forms.CharField(
            max_length=7, 
            label='支給年月（例: 2025-02）', 
            required=True
        )
        
        # nameフィールドを修正
        name = forms.ModelMultipleChoiceField(
            queryset=Allowance.objects.all(),  # Allowanceモデルのインスタンスを渡す
            widget=forms.CheckboxSelectMultiple,
            label='手当を選択',
            required=True
        )
    
        amount = forms.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(10000000)],
            label='手当額'
        )
        
    
    
    
"""class SalaryForm(forms.Form):
    employee = forms.ChoiceField(
        choices = [
            (employee.id, f"{employee.sei} {employee.mei}") for employee in Employee.objects.all()
        ],
        label='従業員',
    )
    # 年を選択できるフィールド
    current_year = datetime.now().year
    year_choices = [(str(year), str(year)) for year in range(current_year, current_year + 30)]
    
    year = forms.ChoiceField(
        choices=year_choices,
        label='支給年'
    )
    month = forms.ChoiceField(
        choices=[
            ('01', '1月'),
            ('02', '2月'),
            ('03', '3月'),
            ('04', '4月'),
            ('05', '5月'),
            ('06', '6月'),
            ('07', '7月'),
            ('08', '8月'),
            ('09', '9月'),
            ('10', '10月'),
            ('11', '11月'),
            ('12', '12月'),
        ], 
        label='支給月'
    )
    name = forms.ChoiceField(
        choices=[
            ('交通費', '交通費'),
            ('インセンティブ', 'インセンティブ'),
            ('役職手当', '役職手当'),
        ], 
        label='手当名'
    )
    amount = forms.IntegerField(validators=[MinValueValidator(0), 
                                            MaxValueValidator(10000000)], label='手当額')
"""
