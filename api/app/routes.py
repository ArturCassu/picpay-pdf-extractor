from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse, StreamingResponse
from app.services.extractor import PDFExtractor
import pandas as pd
import io

router = APIRouter()

# Simple in-memory cache: {username: data}
user_cache = {}

@router.post("/extract/")
async def extract_pdf_data(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        contents = await file.read()
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)
        extractor = PDFExtractor(temp_path)
        data = extractor.extract_data()
        # Cache by username
        user_cache[data["usuario"]] = data
        return JSONResponse(content={"data": data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.get("/download_excel/")
def download_excel(usuario: str = Query(...)):
    data = user_cache.get(usuario)
    if not data:
        return JSONResponse(content={"error": "No data for this user"}, status_code=404)
    df = pd.DataFrame(data["transacoes"], columns=[
        "Data", "Hora", "Descrição", "Valor", "Saldo", "Saldo Sacável",
        "ValorNum", "SaldoNum", "SaldoSacavelNum"
    ])
    df["Tipo"] = df["ValorNum"].apply(lambda x: "Recebido" if x > 0 else "Gasto" if x < 0 else "Nulo")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename=movimentacoes_{usuario}.xlsx"})

@router.delete("/clear/")
def clear_user_data(usuario: str = Query(...)):
    if usuario in user_cache:
        del user_cache[usuario]
        return JSONResponse(content={"message": "User data cleared"}, status_code=200)
    return JSONResponse(content={"error": "No data for this user"}, status_code=404)