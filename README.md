# 🌬️ SmogWatch

Monitor jakości powietrza w Polsce wykorzystujący dane z API GIOŚ.

## 🚀 Szybki start

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run serve
```

## 📱 Funkcjonalności

- ✅ Lista wszystkich stacji pomiarowych w Polsce
- ✅ Wyszukiwanie stacji po nazwie miasta
- ✅ Szczegółowe dane z każdej stacji
- ✅ Indeks jakości powietrza z kolorowym oznaczeniem
- ✅ Aktualne pomiary zanieczyszczeń (PM10, PM2.5, NO2, itd.)
- ✅ Responsywny design

## 🛠️ Technologie

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: Vue.js 3, Axios
- **API**: GIOŚ (Główny Inspektorat Ochrony Środowiska)

## 📊 Źródło danych

Aplikacja wykorzystuje oficjalne API GIOŚ:
`https://api.gios.gov.pl/pjp-api/rest`

## 🌐 Dostęp

- Backend: http://localhost:5000
- Frontend: http://localhost:8080

---
Made with ❤️ for cleaner air in Poland