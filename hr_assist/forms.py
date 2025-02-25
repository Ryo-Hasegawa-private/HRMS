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
            'email',
            'basic_salary',
            'joining_date',
            'status',
        ]
        labels = {
            'sei': '姓',
            'mei': '名',
            'birth_date': '生年月日',
            'gender': '性別',
            'email': 'メールアドレス',
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
            validators=[MinValueValidator(-1000000), MaxValueValidator(1000000)],
            label='手当額'
        )
        