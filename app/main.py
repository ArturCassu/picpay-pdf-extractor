from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.transaction_routes import router as transaction_router
from app.routes.user_routes import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Extractor API!"}