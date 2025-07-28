from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.extractor import extract_data_from_pdf

router = APIRouter()

@router.post("/extract/")
async def extract_pdf_data(file: UploadFile = File(...)):
    try:
        data = await extract_data_from_pdf(file)
        return JSONResponse(content={"data": data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)