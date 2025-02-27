from django.shortcuts import render, redirect

from .models import Employee, Allowance
from .forms import EmployeeForm
from .forms import SalaryForm
from plotly.graph_objects import Histogram, Layout, Pie
from plotly import offline
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import statistics

def index(request):
    """人事労務くんのホームページ"""
    # 今月を取得
    today = datetime.today()
    this_month = today.strftime('%Y-%m')  # 例: '2025-02'

    # コンテキストに追加
    context = {
        'this_month': this_month,
    }
    return render(request, 'hr_assist/index.html', context)

@login_required
def register_employee(request):
    """従業員を追加する"""
    if request.method != 'POST':
        # データは送信されていないので空のフォームを生成する
        form = EmployeeForm()
    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EmployeeForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_assist:employees')
        
    # 空または無効のフォームを表示する
    context = {'form': form}
    return render(request, 'hr_assist/register_employee.html', context)

@login_required
def employees(request):
    """従業員一覧を表示する"""
    employees = Employee.objects.order_by('id')
    context = {'employees': employees}
    return render(request, 'hr_assist/employees.html', context)

@login_required
def employee(request, emp_id):
    """従業員の詳細情報を表示する"""
    # 先頭の0を削除してemp_idを比較する
    emp_id = str(emp_id).lstrip('0')
    
    # ログインしているユーザーの従業員番号も0を削除して比較
    user_id = str(request.user.username).lstrip('0')
    
    if emp_id == user_id or request.user.is_staff:
        employee = Employee.objects.get(id=emp_id)
    today = datetime.today()
    # `YYYY-MM`形式の文字列に変換
    this_month = today.strftime('%Y-%m')  # 例: '2025-02'
        
    context = {
        'employee': employee,
        'emp_id': emp_id,
        'this_month': this_month,
    }
    return render(request, 'hr_assist/employee.html', context)

@login_required
def confirm_salary(request, emp_id):
    # 従業員の情報を取得
    employee = get_object_or_404(Employee, id=emp_id)
    
    if request.method != 'POST':
        # データは送信されていないので空のフォームを生成する
        form = SalaryForm(initial={'employee': employee})  # 従業員を初期選択として設定
    else:
        # POSTでデータが送信されたのでこれを処理する
        form = SalaryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_assist:confirm_salary', emp_id=emp_id)
        
    # 空または無効のフォームを表示する
    context = {'form': form, 'employee': employee}
    return render(request, 'hr_assist/confirm_salary.html', context)

@login_required
def salary(request, emp_id, paymonth):
    
    # 先頭の0を削除してemp_idを比較する
    emp_id = str(emp_id).lstrip('0')
    
    # ログインしているユーザーの従業員番号も0を削除して比較
    user_id = str(request.user.username).lstrip('0')
    
    if emp_id == user_id or request.user.is_staff:
        # 従業員と支給年月を取得
        employee = Employee.objects.get(id=emp_id)
        
    today = datetime.today()
    # `YYYY-MM`形式の文字列に変換
    this_month = today.strftime('%Y-%m')  # 例: '2025-02'
    allowances = Allowance.objects.filter(employee=employee, paymonth=paymonth)
    paymonths = Allowance.objects.values('paymonth').distinct()  # 支給年月のリストを取得
    all_emp = Employee.objects.all()
    

    # 合計手当と合計控除を取得
    total_allowance = Allowance.total_allowance(emp_id, paymonth)  
    total_deduction = Allowance.total_deduction(emp_id, paymonth)  
    total_salary = employee.basic_salary + total_allowance + total_deduction
    context = {
        'employee': employee,
        'allowances': allowances,
        'paymonth': paymonth,
        'total_allowance': total_allowance,  
        'total_deduction': total_deduction,
        'total_salary': total_salary,
        'all_emp': all_emp,
        'paymonths': paymonths,

        'emp_id': emp_id,
        'this_month': this_month,
    }
    return render(request, 'hr_assist/salary.html', context)

@login_required
def insight(request):
    """インサイト情報を表示する"""
    # 退職済み以外の従業員をフィルタリング
    active_employees = Employee.objects.exclude(status='LEAVED')  # 退職済み（LEAVED）を除外
    
    # 年齢リストを取得
    ages = [employee.calculate_age() for employee in active_employees]
    # 性別リストを取得
    genders = [employee.gender for employee in active_employees]
    # 基本給リストを取得
    basic_salaries = [employee.basic_salary for employee in active_employees]
    
    # 男女の数を計算
    male_count = genders.count('男性')
    female_count = genders.count('女性')
    total_count = len(genders)
    
    # 男女比を計算
    if total_count > 0:
        male_persentage = male_count / len(genders) * 100
    else:
        male_persentage = 0
        
    if total_count > 0:
        female_persentage = female_count / len(genders) * 100
    else:
        female_persentage = 0    
    
    # ヒストグラムのデータを作成
    data_age = Histogram(x=ages, xbins=dict(start=0, end=100, size=10))
    data_gender = [
        Pie(
            labels = ['男性', '女性'],
            values = [male_persentage, female_persentage],
            name = '性別比',
        )
    ]
    data_basic_salary = Histogram(x=basic_salaries, 
                                  xbins=dict(start=100000, end=1000000, size=100000))
    
    # グラフのレイアウトを設定
    x_axis_config_age = {'title': '年齢', 'dtick': 10}
    y_axis_config_age = {'title': '人数'}
    my_layout_age= Layout(title='年齢の分布', xaxis=x_axis_config_age, 
                       yaxis=y_axis_config_age, bargap=0.1)
    
    my_layout_gender = Layout(
        title='男女比',
        legend=dict(  # legend属性をdict型で追加
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
    )
    
    
    x_axis_config_basic_salary = {'title': '基本給', 'dtick': 100000}
    y_axis_config_basic_salary = {'title': '人数'}
    my_layout_basic_salary = Layout(title='基本給の分布', xaxis=x_axis_config_basic_salary,
                                    yaxis=y_axis_config_basic_salary, barmode="stack")
    
    # HTMLを生成してテンプレートに渡す
    graph_age = offline.plot({'data': data_age, 'layout': my_layout_age}, auto_open=False,  output_type='div')
    graph_gender = offline.plot({'data': data_gender, 'layout': my_layout_gender}, auto_open=False, output_type='div')
    graph_basic_salary = offline.plot({'data': data_basic_salary, 'layout': my_layout_basic_salary}, 
                                      auto_open=False, output_type='div')
    
    # その他計算
    # 従業員数
    total_employee = len(ages)
    
    # 平均年齢
    ans = 0
    if total_employee > 0:
        for age in ages:
            ans += age
        average_age = round(ans / total_employee, 1)
    else:
        average_age = 0
    
    # 最低年齢
    min_age = min(ages)
    
    # 最高年齢
    max_age = max(ages)
    
    # 男性数
    #male_count
    
    # 女性数
    #female_count
    
    # 平均基本給
    ans_salary = 0
    if total_employee > 0:
        for basic_salary in basic_salaries:
            ans_salary += basic_salary
        average_basic_salary = round(ans_salary / total_employee)
    else:
        average_basic_salary = 0
    
    # 基本給の中央値
    median_baisc_salary = statistics.median(basic_salaries)
    mode_basic_salary = statistics.mode(basic_salaries)
    
    dic = {
        'total_employee': total_employee,
        'average_age': average_age,
        'min_age': min_age,
        'max_age': max_age,
        'male_count': male_count,
        'female_count': female_count,
        'average_basic_salary': average_basic_salary,
        'active_employees': active_employees,
        'median_baisc_salary': median_baisc_salary,
        'mode_basic_salary': mode_basic_salary,
    }
    
    # テンプレートに渡す
    return render(request, 'hr_assist/insight.html', {'graph_age': graph_age, 'graph_gender': graph_gender, 
                                                      'graph_basic_salary': graph_basic_salary, 'dic': dic})



    
    
