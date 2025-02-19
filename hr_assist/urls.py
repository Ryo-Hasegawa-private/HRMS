"""hr_assistのURLパターンの定義"""

from django.urls import path

from . import views

app_name = 'hr_assist'
urlpatterns = [
    # ホームページ(P001)
    path('', views.index, name='index'),
    # 従業員登録ページ(A002)
    path('register_employee/', views.register_employee, name='register_employee'),
    # 従業員一覧ページ(A003)
    path('employees/', views.employees, name='employees'),
    # 個別従業員詳細ページ(A004)
    path('employee/<int:emp_id>/', views.employee, name='employee'),
    # インサイトページ(A005)
    path('insight/', views.insight, name='insight'),
    # 給与情報登録ページ(A006)
    path('confirm_salary/<int:emp_id>/', views.confirm_salary, name='confirm_salary'),
    # 給与明細ページ(A007)
    path('salary/<int:emp_id>/<str:paymonth>/', views.salary, name='salary'),
]