from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    #path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', views.login_view, name='login_view'),
    path('adminpage/addstudent/', views.add_student, name="add_student"),
    path('adminpage/', views.adminhomepage, name="adminpage"),
    path('student/', views.student_homepage, name="student"),
    path('staff/', views.staff_homepage, name="staff"),
    path('logout/', views.logout, name='logout'),
    path('adminpage/add_staff/', views.add_staff, name='add_staff'),
    path('staff/update_profile/<int:staff_id>/', views.staff_update_profile, name='staff_update_profile'),
    path('adminpage/add_prgm/', views.add_program, name='add_program'),
    path('adminpage/add_dept/', views.add_department, name='add_department'),
    path('adminpage/add_des/', views.add_designation, name='add_designation'),
    path('program/', views.program_list, name='program_list'),
    path('department/', views.department_list, name='department_list'),
    path('designation/', views.designation_list, name='designation_list'),
    path('student/student_profile/', views.student_profile, name='student_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_email/', auth_views., name='password_reset_email'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('adminpage/add_book/', views.add_book, name='add_book'),
    path('adminpage/book_list/', views.book_list, name='book_list'),
    path('book/<str:accno>/', views.book_details, name='book_details'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),

    path('adminpage/search_book/', views.search_books, name='search_books'),

    path('adminpage/search_members/', views.search_members, name='search_members'),
    path('borrow/<str:accno>/', views.borrow_book, name='borrow_book'),
    path('borrow-requests/', views.borrow_requests, name='borrow_requests'),
    path('approve-borrow-request/<int:request_id>/', views.approve_borrow_request, name='approve_borrow_request'),
    path('return/<str:accno>/', views.return_book, name='return_book'),
    path('return_requests/', views.return_requests, name='return_requests'),
    path('approve-return-request/<int:request_id>/', views.approve_return_request, name='approve_return_request'),
    path('set_book_status/<str:accno>/', views.set_book_status, name='set_book_status'),
    path('student_staff_search_books/', views.student_staff_search_books, name='student_staff_search_books'),
]