import os
import shutil
import tempfile
import urllib
import zipfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pdf2docx import Converter
from cheking_file_name import chek_file_name
from cheking_file_name import chek_file_name
from register_user import add_file_from_path, get_file
from cheking_file_name import refactor_name_file
from starlette.responses import FileResponse, StreamingResponse

async def post_convert_pdf_to_docx(file, user_id):
    try:
        # Создаем временный PDF файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Создаем временную директорию для хранения DOCX файлов
        temp_dir = tempfile.mkdtemp()

        try:
            docx_filename = converter(temp_dir, temp_file_path, file)
            zip_filename = zip_file(temp_dir, docx_filename)
            add_file_from_path(user_id, zip_filename)
            return {"message": "Conversion successful", "zip_filename": zip_filename,"user_id": user_id}

        finally:
            # Удаляем временный PDF файл
            os.remove(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def zip_file(temp_dir, doxc_filename):
    zip_filename = os.path.join(temp_dir, "converted_doxc.zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(doxc_filename, os.path.basename(doxc_filename))
    return zip_filename



def converter(temp_dir, file_path, file):
    with open(file_path, 'rb') as pdf_file:
        cv = Converter(pdf_file)
        docx_filename = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(file.filename))[0]}.docx")
        cv.convert(docx_filename, start=0, end=None)
        cv.close()
        return docx_filename



async def get_convert_pdf_to_docx(file_name, user_id):
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
