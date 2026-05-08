<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Native APK Market - High Performance</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; margin: 0; padding: 20px; }
        .container { max-width: 1100px; margin: auto; }
        .search-box { position: sticky; top: 10px; z-index: 100; text-align: center; margin-bottom: 30px; }
        #searchInput { width: 100%; max-width: 500px; padding: 15px 25px; border-radius: 30px; border: none; shadow: 0 4px 6px rgba(0,0,0,0.1); outline: none; font-size: 16px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }
        .card { background: #fff; padding: 15px; border-radius: 12px; text-align: center; text-decoration: none; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .card img { width: 64px; height: 64px; margin-bottom: 10px; }
        .card h3 { font-size: 14px; margin: 5px 0; height: 35px; overflow: hidden; color: #007bff; }
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Cari dari 4.000+ aplikasi...">
        </div>

        <div class="grid" id="appGrid">
            {% for app in apps %}
            <a href="./app/{{ app.pkg_name }}/" class="card" data-name="{{ app.nama | lower }}">
                <!-- Lazy load gambar agar cepat -->
                <img src="{{ app.icon }}" loading="lazy" alt="{{ app.nama }}" onerror="this.src='https://f-droid.org/repo/categories/Connectivity.png'">
                <h3>{{ app.nama }}</h3>
            </a>
            {% endfor %}
        </div>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const cards = document.querySelectorAll('.card');

        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            cards.forEach(card => {
                const name = card.getAttribute('data-name');
                if (name.includes(term)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    </script>
</body>
</html>