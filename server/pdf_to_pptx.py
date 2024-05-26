from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os
import shutil
import tempfile
import urllib
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pdf2pptx import convert_pdf2pptx
from cheking_file_name import chek_file_name
from register_user import add_file_from_path, get_file
from cheking_file_name import refactor_name_file
from starlette.responses import FileResponse, StreamingResponse


async def post_pdf_to_pptx(file, user_id):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
            # Создаем временную директорию для хранения DOCX файлов
        temp_dir = tempfile.mkdtemp()
        pptx_filename = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(file.filename))[0]}.pptx")
        resolution = 300  # Разрешение в dpi
        start_page = 0  # Номер начальной страницы
        page_count = None  # Количество страниц (None для всех страниц)
        convert_pdf2pptx(temp_file_path, pptx_filename, resolution, start_page, page_count)
        try:
            add_file_from_path(user_id, pptx_filename)
            return {"message": "Conversion successful", "zip_filename": pptx_filename, "user_id": user_id }

        finally:
            # Удаляем временный PDF файл
            os.remove(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




async def get_convert_pdf_to_pptx(file_name, user_id):
    try:
        file_data = get_file(user_id, refactor_name_file(file_name))
        headers = {
            "Content-Disposition": f"attachment; filename={refactor_name_file(file_name)}"
        }
        if file_data:
            return StreamingResponse(iter([file_data]), media_type="application/zip", headers=headers)
        else:
            raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        return {"error": str(e)}