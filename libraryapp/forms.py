from django import forms
from .models import Studentreg, Staffreg, Department, Designation, Program, Book, Holiday, BorrowedBook, BorrowRequest, BookReservation, ReturnRequest
from .validators import validate_isbn, validate_year_of_published


class StudentRegistrationForm(forms.ModelForm):
    pwd = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Studentreg
        fields = ['student_name', 'email', 'pwd']
        # Add any other fields you want to include in the registration form

    def save(self, commit=True):
        student = super(StudentRegistrationForm, self).save(commit=False)
        student.email = self.cleaned_data['email']
        student.pwd = get_random_string(length=12)  # Generate a random password
        if commit:
            student.save()
        return student


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Studentreg
        fields = ['student_name', 'dob', 'address', 'phone_number', 'p_id', 'd_id', 'pwd', 'pic']


# class StudentEditForm(forms.ModelForm):
#     class Meta:
#         model = Studentreg
#         fields = ['student_name','dob', 'address', 'phone_number','p_id', 'd_id', 'pwd', 'pic']
#         # Add any other fields you want to include in the edit form


class StaffAdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staffreg
        fields = ['staff_name', 'email', 'pwd']
        widgets = {
            'pwd': forms.HiddenInput(),  # Hide the password field from the form
        }

    def save(self, commit=True):
        staff = super(StaffAdminRegistrationForm, self).save(commit=False)

        if commit:
            staff.save()

        return staff




class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staffreg
        fields = ['staff_name', 'dob', 'address', 'phone_number', 'd_id', 'des_id', 'pwd', 'pic']


class ProgramForm(forms.ModelForm):
    d_id = forms.ModelChoiceField(queryset=Department.objects.all(), label='Department')  # Assuming you want to choose from existing departments

    class Meta:
        model = Program
        fields = ['program', 'd_id']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department']

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['designation']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    pwd = forms.CharField(label='Password', widget=forms.PasswordInput)


# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = '__all__'
#         widgets = {
#             'year_of_published': forms.SelectDateWidget(years=range(1990, 2023)),
#         }
#
#     def clean_isbn(self):
#         isbn = self.cleaned_data['isbn']
#         validate_isbn(isbn)
#         return isbn
#
#     def clean_year_of_published(self):
#         year = self.cleaned_data['year_of_published']
#         validate_year_of_published(year)
#         return year


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = '__all__'



class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = '__all__'

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = '__all__'


class SearchForm(forms.Form):
    member_id = forms.CharField(label='Member ID', required=True)