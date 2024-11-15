from django.urls import path

from app.kategori.views import list_kategori, edit_kategori, tambah_kategori, hapus_kategori


app_name = "kategori"

urlpatterns = [
    path("", list_kategori, name="list"),
    path("tambah", tambah_kategori, name="tambah"),
    path("edit/<int:id>", edit_kategori, name="edit"),
    path("hapus/<int:id>", hapus_kategori, name="hapus"),
]
