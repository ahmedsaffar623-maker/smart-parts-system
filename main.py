from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.vin_search import router as vin_router
from app.routes.parts import router as parts_router
from app.routes.inventory import router as inventory_router
from app.routes.customers import router as customers_router

app = FastAPI(
    title="Ruwaiei Smart Parts ERP",
    version="1.0.0"
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# الصفحة الرئيسية

@app.get("/")
def home():

    return {
        "system": "Ruwaiei Smart Parts ERP",
        "status": "running"
    }

# ROUTES

app.include_router(vin_router)
app.include_router(parts_router)
app.include_router(inventory_router)
app.include_router(customers_router)