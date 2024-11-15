from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from app.api import APIClient


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    api = APIClient()

    data = api.get("/book/")
    if not data:
        return render(request, "index.html", {'error': "Gagal menghubungi API"})

    data_buku = data.get('data', [])
    return render(request, "index.html", {'data': data_buku})
