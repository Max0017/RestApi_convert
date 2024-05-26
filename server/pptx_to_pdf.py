import uuid

from h11._abnf import status_code
from pptx import Presentation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import tempfile
import urllib.parse
from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import FileResponse
import aspose.slides as slides
import aspose.pydrawing as drawing
from cheking_file_name import chek_file_name
from register_user import add_file_from_path, get_file
from cheking_file_name import refactor_name_file
from starlette.responses import FileResponse, StreamingResponse

async def post_convert_pptx_to_pdf(file, user_id):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
    # Создаем временную директорию для хранения pdf файлов
            temp_dir = tempfile.mkdtemp()
            global pdf_file_name
            pdf_file_name = temp_dir + file.filename + ".pdf"
        with slides.Presentation(temp_file_path) as presentation:
            presentation.save(pdf_file_name, slides.export.SaveFormat.PDF)
        add_file_from_path(user_id, pdf_file_name)
        return {"message": "Conversion successful", "pdf_filename": pdf_file_name, "user_id": user_id}
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))

async def get_convert_pptx_to_pdf(file_name, user_id):
    try:
        file_data = get_file(user_id, refactor_name_file(file_name))
        headers = {
            "Content-Disposition": f"attachment; filename={refactor_name_file(file_name)}"
        }
        if file_data:
            return StreamingResponse(iter([file_data]), media_type="application/pdf", headers=headers)
        else:
            raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        return {"error": str(e)}