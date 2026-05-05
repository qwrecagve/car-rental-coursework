import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import shutil
from pathlib import Path

from .models import RentRequest, ReturnRequest, CarCreate, CustomerCreate
from .system import (
    get_all_cars, 
    get_available_cars, 
    get_rented_cars,
    get_active_customers,
    get_all_registered_customers,
    rent_car, 
    return_car,
    add_car,
    delete_car,
    add_customer,
    get_earnings_report,
    get_rental_history
)

# .env faylini dasturga yuklash (o'qish)
load_dotenv()

# .env faylidagi o'zgaruvchilarni olamiz
ENVIRONMENT = os.getenv("ENVIRONMENT", "noma'lum holat")
PORT = os.getenv("PORT", "8000")

# FastAPI serverini .env dagi ma'lumotlarga asoslanib yaratish
app = FastAPI(title=f"Avtomobil Ijarasi API (Holat: {ENVIRONMENT})")

# Brauzerdan so'rovlarni qabul qilish uchun CORS middleware qo'shamiz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/api/cars")
def get_cars():
    return get_all_cars()

@app.get("/api/cars/available")
def get_av_cars():
    return get_available_cars()

@app.get("/api/cars/rented")
def get_rent_cars():
    return get_rented_cars()

@app.get("/api/customers")
def get_customers():
    return get_active_customers()

@app.get("/api/customers/all")
def get_all_cust():
    return get_all_registered_customers()

@app.post("/api/cars")
def create_car(car: CarCreate):
    success = add_car(car)
    if success:
        return {"message": "Mashina muvaffaqiyatli qo'shildi"}
    return {"error": "Xatolik! Raqam band bo'lishi mumkin."}

@app.delete("/api/cars/{car_id}")
def remove_car(car_id: str):
    success = delete_car(car_id)
    if success:
        return {"message": "Mashina o'chirildi"}
    return {"error": "Mashinani o'chirishda xatolik"}

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Rasmni frontend/images papkasiga saqlash
        images_dir = Path("frontend/images")
        images_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = images_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"filename": f"images/{file.filename}"}
    except Exception as e:
        return {"error": f"Rasm yuklashda xatolik: {str(e)}"}

@app.post("/api/customers")
def create_customer(customer: CustomerCreate):
    new_id = add_customer(customer)
    return {"customer_id": new_id, "message": "Mijoz ro'yxatdan o'tdi"}

@app.post("/api/rent")
def rent(request: RentRequest):
    return rent_car(request.customer_id, request.car_id, request.days)

@app.post("/api/return")
def return_c(request: ReturnRequest):
    return return_car(request.customer_id, request.car_id)

@app.get("/api/reports/earnings")
def get_earnings():
    return get_earnings_report()

@app.get("/api/reports/history")
def get_history():
    return get_rental_history()

@app.get("/api/debug")
def debug_info():
    from .system import db_init_error, get_available_cars
    import traceback
    cars_error = None
    cars_count = None
    try:
        cars = get_available_cars()
        cars_count = len(cars)
    except Exception:
        cars_error = traceback.format_exc()
        
    return {
        "db_init_error": db_init_error,
        "get_available_cars_error": cars_error,
        "cars_count": cars_count,
        "frontend_dir": FRONTEND_DIR,
        "frontend_exists": os.path.exists(FRONTEND_DIR),
        "index_html_exists": os.path.exists(os.path.join(FRONTEND_DIR, "index.html")),
        "cwd": os.getcwd(),
        "env_production": ENVIRONMENT == "production"
    }




# Frontend qismini ulash (BARCHA API ROUTELARDAN KEYIN BO'LISHI SHART)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

