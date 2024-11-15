from django.contrib.messages import success, error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from app.api import APIClient
from app.buku.forms import BukuForm


@require_http_methods(["GET"])
def list_buku(request: HttpRequest) -> HttpResponse:
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 5))
    search = request.GET.get('search', "")
    ordering = request.GET.get('ordering', "-created_at")

    api = APIClient()
    data = api.get("/book/", {'search': search, 'ordering': ordering, 'page': page, "page_size": page_size})
    if not data:
        return render(request, "pages/buku.html", {'error': "Gagal menghubungi API"})

    data_buku = data.get('data', [])
    data_meta = data.get('meta', {})
    return render(
        request,
        "pages/buku.html",
        {
            'data': data_buku,
            'meta': {
                **data_meta,
                'sequence': data_meta.get('page_size', 5) * (data_meta.get('page', 1) - 1),
                'iterator': range(1, data_meta.get('page_total', 1) + 1)
            }
        }
    )


@require_http_methods(["GET", "POST"])
def tambah_buku(request: HttpRequest) -> HttpResponse:
    api = APIClient()

    if request.method == "GET":
        kategori = api.get("/category/") or {}
        return render(
            request,
            "pages/buku_form.html",
            {
                'header': "Tambah buku baru",
                'action': "tambah",
                'kategori': kategori.get('data', {})
            }
        )

    form = BukuForm(request.POST)
    if not form.is_valid():
        error(request, "Form tidak valid")
        return redirect("buku:list")

    res = api.post("/book/", form.cleaned_data)
    if not res:
        error(request, "API mengembalikan error")
        return redirect("buku:list")

    success(request, "Sukses tambah buku")
    return redirect("buku:list")


@require_http_methods(["GET", "POST"])
def edit_buku(request: HttpRequest, id: int) -> HttpResponse:
    api = APIClient()

    if request.method == "GET":
        data = api.get(f"/book/{id}") or {}
        kategori = api.get("/category/") or {}

        return render(
            request,
            "pages/buku_form.html",
            {
                'header': "Ubah buku",
                'action': "edit",
                'buku': data.get('data', {}),
                'kategori': kategori.get('data', {})
            }
        )

    form = BukuForm(request.POST)
    if not form.is_valid():
        error(request, "Form tidak valid")
        return redirect("buku:list")

    res = api.put(f"/book/{id}", form.cleaned_data)
    if not res:
        error(request, "API mengembalikan error")
        return redirect("buku:list")

    success(request, "Sukses ubah buku")
    return redirect("buku:list")


@require_http_methods(["GET", "POST"])
def hapus_buku(request: HttpRequest, id: int) -> HttpResponse:
    api = APIClient()
    if request.method == "GET":
        buku = api.get(f"/book/{id}") or {}
        data_buku = buku.get('data', {})
        return render(request, "pages/dialog.html", {'buku': data_buku, 'label': "buku"})

    res = api.delete(f"/book/{id}")
    if not res:
        error(request, "API mengembalikan error")
        return redirect("buku:list")

    success(request, "Sukses hapus buku")
    return redirect("buku:list")
