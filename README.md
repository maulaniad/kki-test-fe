Smolib (Small Library) Digital

# How to setup for Development
## Requirements
- Python 3.13
- Django 5+
- Tailwind CSS
- Poetry or Pip

## Steps
1. Download Taiwind CSS binary [di sini](https://github.com/tailwindlabs/tailwindcss/releases/latest) (tersedia untuk berbagai platform) hanya untuk development.
2. Pindahkan binary Tailwind CSS ke directory project, ubah nama menjadi `tailwind.exe` atau menjadi `tailwind` untuk linux.
3. Install dependency project
    - Menggunakan Poetry
        - Masuk environment `poetry shell`
        - Install packages `poetry install`
    - Menggunakan Pip
        - Buat environment `python -m venv venv`
        - Masuk environment (Windows) `source venv/Scripts/activate`
        - atau (Linux) `source venv/bin/active`
        - Install packages `pip install -r requirements.txt`
4. Jalankan project setelah masuk virtual environment `python manage.py runserver`
5. Untuk development, jalankan juga listener Tailwind CSS agar stylesheets selalu terupdate. `./tailwind.exe --watch -i static/src/input.css -o static/src/output.css`

Catatan:

Jika menjalankan aplikasi backend bersamaan, ganti port ini dengan yang lain.

Contohnya:

`python manage.py runserver 127.0.0.1:3000`
