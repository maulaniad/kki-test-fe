from django.forms import Form, CharField, IntegerField


class BukuForm(Form):
    title = CharField(max_length=50, required=True)
    author = CharField(max_length=50)
    category = IntegerField(required=True)
