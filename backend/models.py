from pydantic import BaseModel
from typing import List, Optional

class Car(BaseModel):
    car_id: str
    make: str
    model: str
    year: int
    price_per_day: float
    image_url: str
    is_rented: bool = False

class CarCreate(BaseModel):
    car_id: str
    make: str
    model: str
    year: int
    price_per_day: float
    image_url: str

class Customer(BaseModel):
    customer_id: Optional[int] = None
    name: str
    phone: str = "Noma'lum"
    rented_car_id: Optional[str] = None

class CustomerCreate(BaseModel):
    name: str
    phone: str

class RentRequest(BaseModel):
    customer_id: int
    car_id: str
    days: int

class ReturnRequest(BaseModel):
    customer_id: int
    car_id: str
