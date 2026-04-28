# 🚗 Avtomobil Ijarasi (Car Rental) Tizimi

Python (FastAPI) va HTML/CSS/JS da yozilgan avtomobil ijarasi veb-dasturi. OOP (Obyektga Yo'naltirilgan Dasturlash) tamoyillariga asoslangan kurs ishi loyihasi.

## Loyiha Tuzilmasi

```
car_rental_coursework/
├── .env                  # Muhit o'zgaruvchilari
├── .gitignore            # Git tomonidan e'tiborga olinmaydigan fayllar
├── backend/              # Server qismi (Python + FastAPI)
│   ├── models.py         # Mashina va Mijoz ma'lumot modellari
│   ├── system.py         # Biznes logikasi
│   └── main.py           # API server
└── frontend/             # Veb-sayt qismi
    ├── index.html         # Asosiy sahifa
    ├── style.css          # Zamonaviy dizayn
    ├── app.js             # Frontend logikasi
    └── images/            # Avtomobil rasmlari
```

## Ishga tushirish

### 1. Kutubxonalarni o'rnatish
```bash
py -m pip install fastapi uvicorn python-dotenv
```

### 2. Serverni ishga tushirish
```bash
py -m uvicorn backend.main:app --reload
```

### 3. Saytni ochish
`frontend/index.html` faylini brauzerda oching.

## Texnologiyalar
- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** HTML, CSS (Glassmorphism), JavaScript
- **API:** RESTful API
