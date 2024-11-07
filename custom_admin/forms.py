from django import forms
from quiz.models import Question
from user.models import CustomUser

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['topic', 'text', 'correct_answer', 'option_a', 'option_b', 'option_c', 'start_time', 'end_time', 'is_repeatable']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


def create_dynamic_form(model):
    class DynamicModelForm(forms.ModelForm):
        class Meta:
            model = model
            fields = '__all__'  # Include all fields

    return DynamicModelForm


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Select Excel file', help_text='Upload an Excel file containing questions.')