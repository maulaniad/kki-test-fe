from django.forms import Form, CharField


class KategoriForm(Form):
    name = CharField(max_length=50, required=True)
