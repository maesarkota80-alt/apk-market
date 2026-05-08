import os
import json
import requests
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import xml.etree.ElementTree as ET

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
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template_home = env.get_template('home.html')
    template_detail = env.get_template('detail.html')

    print("Mengunduh data F-Droid...")
    data = requests.get(FDROID_JSON).json()
    
    packages = data.get('packages', {})
    versions = data.get('versions', {})
    apps_list = []
    sitemap_entries = [BASE_URL + "/"]

    print("Memproses data aplikasi...")
    for pkg, info in packages.items():
        meta = info.get('metadata', {})
        current_vcode = meta.get('currentVersionCode')
        
        # Logika link download yang akurat
        apk_file = ""
        pkg_versions = versions.get(pkg, [])
        if current_vcode:
            for v in pkg_versions:
                if v.get('versionCode') == current_vcode:
                    apk_file = v.get('file', {}).get('name')
                    break
        
        if not apk_file and pkg_versions:
            apk_file = pkg_versions[0].get('file', {}).get('name')

        download_url = f"https://f-droid.org/repo/{apk_file}" if apk_file else "#"

        app_context = {
            "nama": get_text(meta.get('name'), pkg),
            "summary": get_text(meta.get('summary'), "No summary available"),
            "deskripsi": get_text(meta.get('description'), "No description"),
            "pkg_name": pkg,
            "icon": f"https://f-droid.org/repo/{pkg}/en-US/icon.png",
            "download_link": download_url,
            "version_name": meta.get('currentVersionName', 'Latest')
        }
        
        apps_list.append(app_context)
        sitemap_entries.append(f"{BASE_URL}/app/{pkg}/")

        # Generate Page Detail
        app_folder = os.path.join(OUT_DIR, "app", pkg)
        os.makedirs(app_folder, exist_ok=True)
        with open(os.path.join(app_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(template_detail.render(app=app_context))

    # Generate Home Page
    print("Membuat index.html...")
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(template_home.render(apps=apps_list))

    # GENERATE SITEMAP XML (Proper Format)
    print("Membuat sitemap.xml yang valid...")
    now = datetime.now().strftime("%Y-%m-%d")
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in sitemap_entries:
        url_tag = ET.SubElement(root, "url")
        ET.SubElement(url_tag, "loc").text = url
        ET.SubElement(url_tag, "lastmod").text = now
        ET.SubElement(url_tag, "changefreq").text = "daily"
        ET.SubElement(url_tag, "priority").text = "0.8" if "/app/" in url else "1.0"

    # Simpan sitemap dengan deklarasi XML yang benar
    tree = ET.ElementTree(root)
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

    print(f"Sukses! Selesai memproses {len(apps_list)} aplikasi.")

if __name__ == "__main__":
    build_site()