import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .models import RentRequest, ReturnRequest
from .system import (
    get_all_cars, 
    get_available_cars, 
    get_all_customers, 
    rent_car, 
    return_car
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

@app.get("/api/customers")
def get_customers():
    return get_all_customers()

@app.post("/api/rent")
def rent(request: RentRequest):
    return rent_car(request.customer_id, request.car_id, request.days)

@app.post("/api/return")
def return_c(request: ReturnRequest):
    return return_car(request.customer_id, request.car_id)
