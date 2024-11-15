from django.contrib.messages import success, error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from app.api import APIClient
from app.kategori.forms import KategoriForm


@require_http_methods(["GET"])
def list_kategori(request: HttpRequest) -> HttpResponse:
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 5))
    search = request.GET.get('search', "")
    ordering = request.GET.get('ordering', '-created_at')

    api = APIClient()
    data = api.get("/category/", {'search': search, 'ordering': ordering, 'page': page, "page_size": page_size})
    if not data:
        return render(request, "pages/kategori.html", {'error': "Gagal menghubungi API"})

    data_kategori = data.get('data', [])
    data_meta = data.get('meta', {})
    return render(
        request,
        "pages/kategori.html",
        {
            'data': data_kategori,
            'meta': {
                **data_meta,
                'sequence': data_meta.get('page_size', 5) * (data_meta.get('page', 1) - 1),
                'iterator': range(1, data_meta.get('page_total', 1) + 1)
            }
        }
    )


@require_http_methods(["GET", "POST"])
def tambah_kategori(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(
            request,
            "pages/kategori_form.html",
            {'header': "Tambah kategori baru", 'action': "tambah"}
        )

    form = KategoriForm(request.POST)
    if not form.is_valid():
        error(request, "Form tidak valid")
        return redirect("kategori:list")

    api = APIClient()
    res = api.post("/category/", form.cleaned_data)
    if not res:
        error(request, "API mengembalikan error")
        return redirect("kategori:list")

    success(request, "Sukses tambah kategori")
    return redirect("kategori:list")


@require_http_methods(["GET", "POST"])
def edit_kategori(request: HttpRequest, id: int) -> HttpResponse:
    api = APIClient()

    if request.method == "GET":
        data = api.get(f"/category/{id}") or {}
        return render(
            request,
            "pages/kategori_form.html",
            {
                'header': "Ubah kategori",
                'action': "edit",
                'kategori': data.get('data', {}),
            }
        )

    form = KategoriForm(request.POST)
    if not form.is_valid():
        error(request, "Form tidak valid")
        return redirect("kategori:list")

    res = api.put(f"/category/{id}", form.cleaned_data)
    if not res:
        error(request, "API mengembalikan error")
        return redirect("kategori:list")

    success(request, "Sukses ubah kategori")
    return redirect("kategori:list")


@require_http_methods(["GET", "POST"])
def hapus_kategori(request: HttpRequest, id: int) -> HttpResponse:
    api = APIClient()

    if request.method == "GET":
        kategori = api.get(f"/category/{id}") or {}
        data_kategori = kategori.get('data', {})

        buku = api.get(f"/book/?search={data_kategori.get('name', None)}") or {}
        data_buku = buku.get('data', None)

        if data_buku:
            return render(
                request,
                "pages/dialog.html",
                {'kategori': data_kategori, 'buku': data_buku, 'label': "kategori"}
            )

    res = api.delete(f"/category/{id}")
    if not res:
        error(request, "API mengembalikan error")
        return redirect("kategori:list")

    success(request, "Sukses hapus kategori")
    return redirect("kategori:list")
