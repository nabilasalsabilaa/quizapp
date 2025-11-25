# Quiz App 

Situs kuis sederhana menggunakan Flask. Fitur:
- Pendaftaran & Login (username & nickname unik)
- Kuis acak tanpa batas (setiap soal 4 pilihan)
- Widget prakiraan cuaca 3 hari (OpenWeatherMap)
- Papan peringkat (leaderboard) yang diperbarui saat menyelesaikan kuis
- Navigasi dan footer dengan nama pengembang

## Persyaratan
- Python 3.9+ (direkomendasikan 3.10)
- Virtual environment (venv)
- API key OpenWeatherMap (gratis dari https://openweathermap.org/)

## Install dan jalankan (lokal)
1. Buat virtualenv dan aktifkan:
   - Windows PowerShell:
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Install dependency:
pip install -r requirements.txt

3. Buat folder `instance` (opsional; aplikasi akan membuatnya otomatis):
mkdir instance

4. Set environment variables (PowerShell contoh):
$env:FLASK_APP='app.py'
$env:FLASK_ENV='development'
$env:SECRET_KEY='isi_secret_anda'
$env:WEATHER_API_KEY='isi_openweather_api_key_anda'

5. Jalankan aplikasi:
python -m flask run

6. Buka browser ke `http://127.0.0.1:5000/`

## Deploy ke PythonAnywhere
- Upload kode (via GitHub atau upload file).
- Buat virtualenv di PythonAnywhere, install `pip install -r requirements.txt`.
- Atur Web app (Flask) di dashboard PA, set WSGI file ke `app.py` dan tambahkan env vars (`SECRET_KEY` & `WEATHER_API_KEY`).
- Pastikan mapping `/static/` ke folder static.

## Catatan
- Jangan commit API key ke repo publik.
- Ubah nama pengembang di `templates/base.html` footer sebelum submit.