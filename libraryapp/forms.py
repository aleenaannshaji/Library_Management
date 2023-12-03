from django import forms
from .models import Department, Designation, Program, Book, Holiday, BorrowedBook, BorrowRequest, BookReservation, ReturnRequest

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