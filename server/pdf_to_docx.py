import os
import shutil
import tempfile
import urllib
import zipfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pdf2docx import Converter



async def post_convert_pdf_to_docx(file):
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
            return {"message": "Conversion successful", "zip_filename": zip_filename}

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



async def get_convert_pdf_to_docx(file_name):
    try:

        print(file_name)
        # Декодируем URL-кодированный путь к файлу
        decoded_file_name = urllib.parse.unquote(file_name)

        # Проверяем, существует ли файл
        if not os.path.exists(decoded_file_name):
            raise HTTPException(status_code=404, detail="File not found")

        # Получаем имя файла из полного пути
        base_filename = os.path.basename(decoded_file_name)
        print(base_filename)

        headers = {
            "Content-Disposition": f"attachment; filename={base_filename}"
        }
        return FileResponse(path=decoded_file_name, media_type="application/zip", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
