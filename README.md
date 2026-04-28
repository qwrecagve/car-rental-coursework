# 🚗 Avtomobil Ijarasi (Car Rental) Servisi

Python va FastAPI asosida yaratilgan Avtomobil Ijarasi veb-tizimi. OOP (Obyektga Yo'naltirilgan Dasturlash) tamoyillariga asoslangan.

## 📂 Loyiha Tuzilmasi

```
car_rental_coursework/
├── .env                  # Muhit sozlamalari
├── .gitignore            # Git uchun e'tiborsiz fayllar
├── README.md             # Loyiha haqida ma'lumot
│
├── backend/              # Server qismi (Python + FastAPI)
│   ├── models.py         # Mashina va Mijoz modellari
│   ├── system.py         # Biznes mantiq (ijaraga berish, qaytarish)
│   └── main.py           # FastAPI server va API endpointlar
│
└── frontend/             # Veb-sayt qismi (HTML, CSS, JS)
    ├── index.html         # Asosiy sahifa
    ├── style.css          # Glassmorphism dizayn
    ├── app.js             # Frontend mantiq
    └── images/            # Avtomobil rasmlari
```

## 🛠 Texnologiyalar

- **Backend:** Python 3.13, FastAPI, Uvicorn, Pydantic
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Dizayn:** Glassmorphism, Dark Mode

## 🚀 Ishga Tushirish

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

## 📋 Funksiyalar

- ✅ Bo'sh avtomobillarni ko'rish (rasmli kartochkalar)
- ✅ Mijozlar ro'yxatini ko'rish
- ✅ Avtomobilni ijaraga olish (narx avtomatik hisoblanadi)
- ✅ Avtomobilni qaytarish
- ✅ Zamonaviy va responsive dizayn

## 👨‍💻 Muallif

Kurs ishi loyihasi
