from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
import re
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import YourAgeValidator, validate_isbn, validate_year_of_published
from django.utils import timezone


# Custom User Manager for Admin
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        # Normalize the email
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Manager for Staff
class StaffUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        # Normalize the email
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

# Custom User Manager for Student
class StudentUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_student', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


# ... Other imports and model definitions ...

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # Add other custom fields for email format
    d_id = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
    p_id = models.ForeignKey('Program', on_delete=models.SET_NULL, blank=True, null=True)
    des_id = models.ForeignKey('Designation', on_delete=models.SET_NULL, blank=True, null=True)

    objects = CustomUserManager()  # Corrected this line

    # Add other methods as needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Custom User')
        verbose_name_plural = _('Custom Users')


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.department

class Program(models.Model):
    p_id = models.AutoField(primary_key=True)
    program = models.CharField(max_length=50, unique=True)
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

class Designation(models.Model):
    des_id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=50, unique=True)

def validate_phone_number(value):
    if re.match(r'^\+91([2-8]\d{9}|9{9}|1\d{8}|1[0-8]\d{7}1)$', value):
        raise ValidationError(
            _("Invalid phone number format. Please check and try again.")
        )

def validate_password(value):
    if not re.match(r'^(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/\-])(?=.*\d)(?=.*[A-Z]).*$', value):
        raise ValidationError(
            _("Password must contain at least one special character, one digit, and one capital letter.")
        )

def validate_image_extension(value):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = value.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(_("File type is not supported. Please upload a valid image file (jpg, jpeg, png, gif)."))

def validate_age(self):
    today = date.today()
    age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    if not (18 <= age <= 26):
        raise ValidationError(_("Age must be between 18 and 26 years."))

def validate_age_staff(self):
    today = date.today()
    age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    if not (26 <= age <= 56):
        raise ValidationError(_("Age must be between 26 and 56 years."))


class Studentreg(models.Model):
    student_id = models.AutoField(primary_key=True, editable=False)
    student_name = models.CharField(max_length=25, validators=[
        RegexValidator(r'^[A-Z][a-zA-Z\s]*$', message="Name should start with a capital letter")])
    dob = models.DateField("Date Of Birth",validators=[YourAgeValidator], blank=True, null=True)
    address = models.CharField(max_length=50, validators=[
        RegexValidator(r'^[A-Z][a-zA-Z\s]*$', message="Address should start with a capital letter")])
    phone_number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\+91\d{10}$',
                message="Phone number must start with '+91' followed by 10 digits.",
            ),
            validate_phone_number,
        ],
        default="+91", blank=True,
        null=True
    )
    p_id = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[
        EmailValidator(message="Invalid email format."),
        RegexValidator(
            regex=r'@(?:mca\.ajce\.in|intmca\.ajce\.in|cs\.ajce\.in)$',
            message="Invalid email domain. Use '@mca.ajce.in', '@intmca.ajce.in', or '@cs.ajce.in'."
        )
    ])
    pwd = models.CharField("Password", max_length=25, default=get_random_string(length=12))
    pic = models.ImageField(
        "Profile Picture",
        upload_to='images/',
        validators=[validate_image_extension],
    )

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Studentreg.objects.order_by('-student_id').first()
            if last_student:
                self.student_id = last_student.student_id + 1
            else:
                self.student_id = 1001
        super().save(*args, **kwargs)


class Staffreg(models.Model):
    staff_id = models.AutoField("Staff Id",primary_key=True, editable=False)
    staff_name = models.CharField("Staff Name",max_length=25)
    dob = models.DateField("Date Of Birth",validators=[validate_age_staff], blank=True, null=True)
    address = models.CharField("Address",max_length=50, validators=[
        RegexValidator(r'^[A-Z][a-zA-Z\s]*$', message="Address should start with a capital letter")])
    phone_number = models.CharField("Phone Number",
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\+91\d{10}$',
                message="Phone number must start with '+91' followed by 10 digits.",
            ),
            validate_phone_number,
        ],
        default="+91",
        blank=True,
        null=True
    )
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    des_id = models.ForeignKey(Designation, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[
        EmailValidator(message="Invalid Email Format"),
        RegexValidator(
            regex=r'@amaljyothi\.ac\.in$',
            message="Invalid email domain. Use '@amaljyothi.ac.in'."
        )
    ])
    pwd = models.CharField("Password", max_length=25, default=get_random_string(length=12))
    pic = models.ImageField("Profile Picture", upload_to='staff_images/', validators=[validate_image_extension],)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            last_staff = Staffreg.objects.order_by('-staff_id').first()
            if last_staff:
                last_staff_id = int(last_staff.staff_id[3:])  # Extract the numeric part
                self.staff_id = f'FAC{last_staff_id + 1:03d}'  # Format as "FACXXX"
            else:
                self.staff_id = 'FAC001'
        super().save(*args, **kwargs)



def validate_year_of_published(value):
    current_year = date.today().year
    if not (1990 <= value <= current_year):
        raise ValidationError("Year of publication must be between 1990 and the current year.")


def validate_isbn(value):
    if len(value) != 12 or not value.isdigit():
        raise ValidationError("ISBN must be a 12-digit number.")


class Holiday(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.date)

from django.db.models import F


class Book(models.Model):
    accno = models.CharField(max_length=6, primary_key=True, unique=True, editable=False)
    callno = models.CharField(max_length=20,unique=True, validators=[RegexValidator(r'^[A-Za-z0-9\-\s]+$')])
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year_of_published = models.PositiveIntegerField(validators=[validate_year_of_published])
    isbn = models.CharField(max_length=12, validators=[validate_isbn],unique=True)
    publisher = models.CharField(max_length=50)
    pages = models.PositiveIntegerField()

    BOOK_TYPES = (
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Biography', 'Biography'),
        ('Computer Science', 'Computer Science'),
        # Add more types as needed
    )

    type_of_book = models.CharField(max_length=20, choices=BOOK_TYPES)
    available_copies = models.PositiveIntegerField(default=0)
    total_copies = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.accno:
            last_book = Book.objects.order_by('-accno').first()
            if last_book:
                last_accno = last_book.accno
                accno_int = int(last_accno[3:]) + 1
                self.accno = f'Acc{accno_int:03d}'
            else:
                self.accno = 'Acc001'
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def is_borrowed(self):
        return BorrowedBook.objects.filter(accno=self, returned=False).exists()

    def is_reserved(self):
        return BookReservation.objects.filter(accno=self, approved=False).exists()

    def can_be_borrowed(self):
        return self.active and not self.is_borrowed() and self.available_copies > 0

    def can_be_reserved(self):
        return not self.is_borrowed() and not self.is_reserved() and self.available_copies > 0

    def borrow_book(self):
        if self.can_be_borrowed():
            self.available_copies = F('available_copies') - 1
            self.save()
            return True
        return False

    def return_book(self):
        if self.is_borrowed():
            self.available_copies = F('available_copies') + 1
            self.save()
            return True
        return False


# class Book(models.Model):
#     accno = models.CharField(max_length=6, primary_key=True, unique=True, editable=False)
#     callno = models.CharField(max_length=15, unique=True, validators=[
#         RegexValidator(r'^[A-Za-z0-9\-,\s]+$', message="Call number should contain letters, digits, '-', and ','.")
#     ])
#     title = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     year_of_published = models.PositiveIntegerField(
#         validators=[MinValueValidator(1995), MaxValueValidator(2023)]
#     )
#     isbn = models.CharField(max_length=12, unique=True, validators=[validate_isbn])
#     publisher = models.CharField(max_length=50)
#     pages = models.PositiveIntegerField()
#
#     BOOK_TYPES = (
#         ('Fiction', 'Fiction'),
#         ('Non-Fiction', 'Non-Fiction'),
#         ('Science', 'Science'),
#         ('Biography', 'Biography'),
#         ('Computer Science', 'Computer Science'),
#         # Add more types as needed
#     )
#
#     type_of_book = models.CharField(max_length=20, choices=BOOK_TYPES)
#     available_copies = models.PositiveIntegerField(default=0)
#     total_copies = models.PositiveIntegerField(default=0)
#     active = models.BooleanField(default=True)
#
#     def activate(self):
#         self.active = True
#         self.save()
#
#     def deactivate(self):
#         self.active = False
#         self.save()
#
#     def save(self, *args, **kwargs):
#         if not self.accno:
#             last_book = Book.objects.order_by('-accno').first()
#             if last_book:
#                 last_accno = int(last_book.accno[3:])
#                 self.accno = f'acc{last_accno + 1:03d}'
#             else:
#                 self.accno = 'acc001'
#         super(Book, self).save(*args, **kwargs)
#
#     def is_borrowed(self):
#         return BorrowedBook.objects.filter(accno=self, returned=False).exists()
#
#     def is_reserved(self):
#         return BookReservation.objects.filter(accno=self, approved=False).exists()
#
#     def can_be_borrowed(self):
#         return self.active and not self.is_borrowed() and self.available_copies > 0
#
#     def can_be_reserved(self):
#         return not self.is_borrowed() and not self.is_reserved() and self.available_copies > 0
#
#     def borrow_book(self):
#         if self.can_be_borrowed():
#             self.available_copies = F('available_copies') - 1
#             self.save()
#             return True
#         return False
#
#     def return_book(self):
#         if self.is_borrowed():
#             self.available_copies = F('available_copies') + 1
#             self.save()
#             return True
#         return False
#

class BorrowRequest(models.Model):
    accno = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    student_id = models.ForeignKey(Studentreg, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Staffreg, on_delete=models.CASCADE, null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class BorrowedBook(models.Model):
    accno = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.ForeignKey(Studentreg, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Staffreg, on_delete=models.CASCADE, null=True, blank=True)
    borrowed_date = models.DateField()
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    fine_details = models.TextField(blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Add other fields as needed

    def __str__(self):
        return f"Borrowed {self.accno} by {self.student_id} or {self.staff_id}"


class BookReservation(models.Model):
    accno = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.ForeignKey(Studentreg, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Staffreg, on_delete=models.CASCADE, null=True, blank=True)
    # Add other fields like reservation date, status, etc.
    reservation_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.accno} by {self.student_id} or {self.staff_id}"



class SearchBook(models.Model):
    search_id = models.AutoField(primary_key=True)
    accno = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.ForeignKey(Studentreg, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Staffreg, on_delete=models.CASCADE, null=True, blank=True)
    # Add other fields as needed.


class ReturnRequest(models.Model):
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE, blank=True, null=True)
    accno = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.ForeignKey(Studentreg, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Staffreg, on_delete=models.CASCADE, null=True, blank=True)
    return_date = models.DateField()
    approved = models.BooleanField(default=False)
