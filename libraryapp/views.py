from django.shortcuts import render, redirect, get_object_or_404
from .models import Studentreg, Staffreg, Department, Program, Designation, CustomUser, Book, BorrowRequest, BorrowedBook, ReturnRequest, BookReservation, Holiday,SearchBook
from .forms import StudentRegistrationForm, StaffAdminRegistrationForm, DepartmentForm, LoginForm, ProgramForm, DesignationForm, StudentProfileForm, StaffUpdateForm, BookForm, SearchForm, BorrowRequestForm, ReservationForm, BorrowedBookForm, ReturnRequestForm
# from django.contrib.auth import login as auth_login, authenticate

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.conf import settings
import secrets
import string
from django.db.models import Q


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('pwd')
#         user = authenticate(request, email=email, password=pwd)
#         if user is not None:
#             auth_login(request, user)
#             request.session['email'] = email
#             if user.is_admin:
#                 return redirect('adminhomepage')
#             elif user.is_staff:
#                 return redirect('staff_homepage')
#             elif user.is_student:
#                 return redirect('student_homepage')
#         else:
#             messages.error(request, "Invalid login credentials")
#
#     response = render(request, 'login.html')
#     response['Cache-Control'] = 'no-store, must-revalidate'
#     return response

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = email
            if user.is_admin:
                return redirect('adminhomepage')
            elif user.is_staff:
                return redirect('staff_homepage')
            elif user.is_student:
                return redirect('student_homepage')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')


def index(request):
    return render(request, "index.html")



def add_staff(request):
    if request.method == 'POST':
        # Get the email and username from the admin
        email = request.POST.get('email')
        name = request.POST.get('name')

        # Generate a random password
        password = get_random_string(length=12)

        # Create a new student with the generated password
        staff = Staffreg(staff_name=name, email=email, pwd=password)
        staff.save()

        # Send the password to the student's email address
        subject = 'Your New Password'
        message = f'Hello {name},\n\nYour new password is: {password}\n\n Login url: http://127.0.0.1:8000/login/\n\nPlease keep this information safe.'
        from_email = 'aleenaannshaji@gmail.com'  # Change this to your admin's email address
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        # Redirect to a success page or do something else
        return redirect('adminpage')

    return render(request, 'Staffreg.html')



def staff_update_profile(request, staff_id):
    staff = Staffreg.objects.get(staff_id=staff_id)
    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = StaffUpdateForm(instance=staff)

    return render(request, 'staffreg.html', {'form': form, 'staff': staff})



def add_student(request):
    if request.method == 'POST':
        # Get the email and username from the admin
        email = request.POST.get('email')
        name = request.POST.get('name')

        # Generate a random password
        password = get_random_string(length=12)

        # Create a new student with the generated password
        student = Studentreg(student_name=name, email=email, pwd=password)
        student.save()

        # Send the password to the student's email address
        subject = 'Your New Password'
        message = f'Hello {name},\n\nYour new password is: {password}\n\n Login url: http://127.0.0.1:8000/login/\n\nPlease keep this information safe.'
        from_email = 'aleenaannshaji@gmail.com'  # Change this to your admin's email address
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        # Redirect to a success page or do something else
        return redirect('adminpage')

    return render(request, 'Studentreg.html')




@login_required
def student_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully')
            except (ValidationError, IntegrityError):
                messages.error(request, 'Invalid data or email already exists')
    else:
        form = StudentProfileForm(instance=request.user)

    return render(request, 'student_profile.html', {'form': form})


# def student_profile(request):
#     return render(request, "student_profile.html")


def add_program(request):
    error_message = None
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program_name = form.cleaned_data['program']
            d_id = form.cleaned_data['d_id']  # Update to 'd_id'

            # Check if a program with the same name and department already exists
            if Program.objects.filter(program=program_name, d_id=d_id).exists():
                error_message = 'A program with this name in the selected department already exists.'
            else:
                form.save()
            return redirect('program_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form, 'error_message': error_message})


def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department_name = form.cleaned_data['department']
            if Department.objects.filter(department=department_name).exists():
                error_message = 'Department with this name already exists.'
            else:
                form.save()
                return redirect('department_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = DepartmentForm()
        error_message = None

    return render(request, 'add_department.html', {'form': form, 'error_message': error_message})


def add_designation(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            designation_name = form.cleaned_data['designation']
            if Designation.objects.filter(designation=designation_name).exists():
                error_message = 'Designation with this name already exists.'
            else:
                form.save()
                return redirect('designation_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = DesignationForm()
        error_message= None
    return render(request, 'add_designation.html', {'form': form, 'error_message': error_message})


def student_list(request):
    students = Studentreg.objects.all()
    return render(request, 'student_list.html', {'students': students})

def staff_list(request):
    staffs = Staffreg.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})


def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def designation_list(request):
    designations = Designation.objects.all()
    return render(request, 'designation_list.html', {'designations': designations})




def adminhomepage(request):
    return render(request, 'adminhome.html')

def student_homepage(request):
    some_value = "Welcome to studentpage!"
    return render(request, 'studenthome.html', {'some_context_data': some_value})

def staff_homepage(request):
    return render(request, 'staffhome.html')




def search_members(request):
    search_performed = False
    students = []
    staff = []

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        if member_id:
            student = Studentreg.objects.filter(student_id=member_id).first()
            staff_member = Staffreg.objects.filter(staff_id=member_id).first()

            if student:
                students.append(student)
            if staff_member:
                staff.append(staff_member)

        search_performed = True

    return render(request, 'member_list.html', {'search_performed': search_performed, 'students': students, 'staff': staff})



# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             book = form.save()
#             return redirect('book_list')  # Redirect to a page displaying the list of books
#
#     else:
#         form = BookForm()
#
#     return render(request, 'add_book.html', {'form': form})



def add_book(request):
    if request.method == 'POST':
        # Handle form submission to create a new book
        # Extract form data and save it to the Book model
        accno = request.POST.get('accno')
        callno = request.POST.get('callno')
        title = request.POST.get('title')
        author = request.POST.get('author')
        year_of_published = request.POST.get('year_of_published')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        pages = request.POST.get('pages')
        type_of_book = request.POST.get('type_of_book')
        available_copies = request.POST.get('available_copies')
        total_copies = request.POST.get('total_copies')
        active = request.POST.get('active')

        book = Book(
            accno=accno,
            callno=callno,
            title=title,
            author=author,
            year_of_published=year_of_published,
            isbn=isbn,
            publisher=publisher,
            pages=pages,
            type_of_book=type_of_book,
            available_copies=available_copies,
            total_copies=total_copies,
            active=active
        )
        book.save()

        return redirect('book_list')  # Replace 'book_list' with the URL pattern for listing books
    else:
        # Render the form to add a new book
        return render(request, 'add_book.html')


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def set_book_status(request, accno):
    if request.method == 'POST':
        book = get_object_or_404(Book, accno=accno)
        book_status = request.POST.get('book_status')

        if book_status == 'active':
            if book.active and book.can_be_borrowed():
                # If the book is active and has available copies, redirect to borrow view
                return redirect('borrow_book', accno=accno)
            elif book.active and book.can_be_reserved():
                # If the book is active but doesn't have available copies, redirect to reserve view
                return redirect('reserve_book', accno=accno)
            else:
                # If the book is inactive, activate it
                book.activate()
        elif book_status == 'inactive':
            # If the book is active, deactivate it
            if book.active:
                book.deactivate()

    # Redirect back to the book list page with the updated status
    return redirect('book_list')


def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Get the search query from the URL parameter
        books = Book.objects.filter(Q(accno__icontains=query) | Q(title__icontains=query))

        context = {
            'books': books,
        }
        return render(request, 'search_book.html', context)




# def book_details(request, accno):
#     book = Book.objects.get(accno=accno)
#     penalty = book.calculate_penalty()
#
#     if request.method == 'POST':
#         # Handle actions related to the book, e.g., marking as returned, approval, etc.
#         # You can implement these actions based on your requirements.
#         pass
#
#     return render(request, 'book_details.html', {'book': book, 'penalty': penalty})


def student_staff_search_books(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        # Perform a query to search for books
        books = Book.objects.filter(Q(accno__icontains=search_term) | Q(title__icontains=search_term))
        return render(request, 'student_staff_search_books.html', {'books': books})
    else:
        return render(request, 'user_search_book.html')


# def set_book_status(request, accno):
#     if request.method == 'POST':
#         book = get_object_or_404(Book, accno=accno)
#         book_status = request.POST.get('book_status')
#
#         if book_status == 'active':
#             book.active = True
#         elif book_status == 'inactive':
#             book.active = False
#         book.save()
#
#     # Redirect back to the search page with the updated status
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def request_book(request, accno):
    book = get_object_or_404(Book, accno=accno)

    if request.method == 'POST':
        user = request.user  # Replace with the actual way to get the user
        staff_id = user.staff_id
        student_id = user.student_id

        if book.can_be_borrowed() and 'borrow' in request.POST:
            # Handle the borrow request
            BorrowRequest.objects.create(
                accno=book,
                student_id=student_id,
                staff_id=staff_id,
                book_title=book.title,
                book_author=book.author
            )
            return redirect('borrow_requests')  # Create a view for listing borrow requests

        elif 'reserve' in request.POST:
            # Handle the reservation request
            BookReservation.objects.create(
                accno=book,
                student_id=student_id,
                staff_id=staff_id,
                book_title=book.title,
                book_author=book.author
            )
            return redirect('reservation_requests')  # Create a view for listing reservation requests

    return render(request, 'request_book.html', {'book': book})


def borrow_book(request, accno):
    # Get the book object by accession number (accno)
    book = get_object_or_404(Book, accno=accno)

    if request.method == 'POST':
        # Handle the book borrowing request
        if book.can_be_borrowed():
            # Check if the book can be borrowed (is active and not already borrowed)

            # Create a BorrowedBook entry
            borrowed_book = BorrowedBook(
                accno=book,
                student_id=request.user.student_id,  # Replace with the actual way to get student_id
                staff_id=request.user.staff_id,  # Replace with the actual way to get staff_id
                borrowed_date=timezone.now(),
                due_date=timezone.now() + timezone.timedelta(days=14),  # Set the due date to 14 days from now
            )
            borrowed_book.save()

            # Update the book's available copies
            book.available_copies -= 1
            book.save()

            # Check if there are pending reservations for this book and approve if possible
            reservations = BookReservation.objects.filter(accno=book, approved=False)
            if reservations.exists():
                # Approve the first reservation (FIFO)
                reservation = reservations.first()
                reservation.approved = True
                reservation.save()
                # Update the book's available copies
                book.available_copies -= 1
                book.save()

            return redirect('borrowed_books')  # Replace with the URL pattern for listing borrowed books
        else:
            # Book cannot be borrowed, handle accordingly (e.g., show a message)
            return render(request, 'cannot_borrow.html', {'book': book})  # Create an HTML template for this message

    # Render the book borrowing form
    return render(request, 'borrow_book.html', {'book': book})

#-------
def borrow_requests(request):
    pending_requests = BorrowRequest.objects.filter(
        book__active=True,
        approved=False
    )
    return render(request, 'borrow_requests.html', {'pending_requests': pending_requests})

@login_required
def approve_borrow_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    borrow_request.approved = True
    borrow_request.save()
    # Create a corresponding BorrowedBook entry
    borrowed_book = BorrowedBook(
        book=borrow_request.book,
        borrower=borrow_request.borrower,
        borrowed_date=timezone.now(),
        due_date=timezone.now() + timezone.timedelta(days=14)  # 14 days due date
    )
    borrowed_book.save()
    return redirect('borrow_requests')

@login_required
def return_book(request, accno):
    book = get_object_or_404(Book, accno=accno)
    borrowed_book = BorrowedBook.objects.filter(
        book=book,
        borrower=request.user,
        returned=False
    ).first()
    if borrowed_book:
        # Create a ReturnRequest for the borrowed book
        return_request = ReturnRequest(borrowed_book=borrowed_book, return_date=timezone.now())
        return_request.save()
        return redirect('return_requests')
    else:
        # Handle the case when the book hasn't been borrowed
        pass

@login_required
def return_requests(request):
    pending_return_requests = ReturnRequest.objects.filter(
        borrowed_book__book__active=True,
        approved=False
    )
    return render(request, 'return_requests.html', {'pending_return_requests': pending_return_requests})

@login_required
def approve_return_request(request, request_id):
    return_request = get_object_or_404(ReturnRequest, id=request_id)
    return_request.approved = True
    return_request.save()
    borrowed_book = return_request.borrowed_book
    borrowed_book.returned = True
    borrowed_book.save()
    return redirect('return_requests')
