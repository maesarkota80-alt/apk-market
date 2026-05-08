import os
import json
import requests
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Konfigurasi
FDROID_JSON = "https://f-droid.org/repo/index-v2.json"
OUT_DIR = "dist"
TEMPLATES_DIR = "templates"
BASE_URL = "https://mini-apk.pages.dev"

def get_text(data_field, default=""):
    if isinstance(data_field, dict):
        return data_field.get('en-US') or next(iter(data_field.values()), default)
    return data_field if data_field else default

def build_site():
    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
    
    # Pastikan folder templates ada
    if not os.path.exists(TEMPLATES_DIR):
        print("Folder templates tidak ditemukan!")
        return

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template_home = env.get_template('home.html')
    template_detail = env.get_template('detail.html')

    print("Mengunduh data dari F-Droid...")
    data = requests.get(FDROID_JSON).json()
    
    apps_list = []
    sitemap_urls = [BASE_URL]

    print("Memproses aplikasi...")
    for pkg, info in data['packages'].items():
        meta = info.get('metadata', {})
        nama = get_text(meta.get('name'), pkg)
        summary = get_text(meta.get('summary'), "No summary")

        app_context = {
            "nama": nama,
            "summary": summary,
            "deskripsi": get_text(meta.get('description'), "No description"),
            "pkg_name": pkg,
            "icon": f"https://f-droid.org/repo/{pkg}/en-US/icon.png"
        }
        apps_list.append(app_context)
        sitemap_urls.append(f"{BASE_URL}/app/{pkg}/")

        app_folder = os.path.join(OUT_DIR, "app", pkg)
        os.makedirs(app_folder, exist_ok=True)
        with open(os.path.join(app_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(template_detail.render(app=app_context))

    # Buat Halaman Utama
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(template_home.render(apps=apps_list))

    # Buat Sitemap
    now = datetime.now().strftime("%Y-%m-%d")
    sitemap_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_content += f'  <url><loc>{url}</loc><lastmod>{now}</lastmod></url>\n'
    sitemap_content += '</urlset>'
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print(f"Sukses! {len(apps_list)} halaman dibuat.")

if __name__ == "__main__":
    build_site()