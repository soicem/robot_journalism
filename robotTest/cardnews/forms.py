from django import forms

class NameForm(forms.Form):
    keyword = forms.CharField(label='keyword', max_length=100)
    tendency = forms.CharField(label='tendency', max_length=100)
    print("soicem")


class PostForm(forms.Form):
    content = forms.CharField(max_length=256)
    created_at = forms.DateTimeField()