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

async def post_convert_pptx_to_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
    # Создаем временную директорию для хранения pdf файлов
            temp_dir = tempfile.mkdtemp()
            pdf_file_name = temp_dir + file.filename + ".pdf"
        with slides.Presentation(temp_file_path) as presentation:
            presentation.save(pdf_file_name, slides.export.SaveFormat.PDF)
        return {"message": "Conversion successful", "pdf_filename": pdf_file_name}
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))

async def get_convert_pptx_to_pdf(file_name):

        headers = {
            "Content-Disposition": f"inline; filename={file_name}"
        }
        return FileResponse(path = file_name, media_type="application/pdf", headers=headers)

