from django.core.exceptions import ValidationError
from datetime import date

def YourAgeValidator(value):
    def validate_age(date_of_birth):
        age = (date.today() - date_of_birth).days // 365
        if not 18 <= age <= 26:
            raise ValidationError("Age must be between 18 and 26 years.")

    return validate_age(value)

def validate_isbn(value):
    if len(value) != 12 or not value.isdigit():
        raise ValidationError("ISBN must be a 12-digit number.")

def validate_year_of_published(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError("Year of publication cannot be in the future.")
