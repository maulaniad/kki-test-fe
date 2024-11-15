from django.urls import path

from app.buku.views import list_buku, tambah_buku, edit_buku, hapus_buku


app_name = "buku"

urlpatterns = [
    path("", list_buku, name="list"),
    path("tambah", tambah_buku, name="tambah"),
    path("edit/<int:id>", edit_buku, name="edit"),
    path("hapus/<int:id>", hapus_buku, name="hapus")
]
