from pydantic import BaseModel
from typing import List, Optional

class Car(BaseModel):
    car_id: str
    make: str
    model: str
    year: int
    price_per_day: float
    image_url: str  # Yangi maydon
    is_rented: bool = False

class Customer(BaseModel):
    customer_id: int
    name: str
    rented_cars: List[Car] = []

class RentRequest(BaseModel):
    customer_id: int
    car_id: str
    days: int

class ReturnRequest(BaseModel):
    customer_id: int
    car_id: str
