import os
import tempfile
import zipfile

from fastapi import HTTPException
from pdf2image import convert_from_path
from starlette.responses import FileResponse
from register_user import add_file_from_path, get_file
from cheking_file_name import refactor_name_file
from starlette.responses import FileResponse, StreamingResponse

from cheking_file_name import chek_file_name

async def post_pdf_to_img(file, user_id):
    try:
        poppler_path = r'C:\Users\Serfar\Desktop\Release-24.02.0-0\poppler-24.02.0\Library\bin'
        # Создаем временный файл и записываем в него содержимое загруженного файла
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        # Создаем временную директорию для сохранения файлов
        temp_dir = tempfile.mkdtemp()
        # Конвертируем PDF в изображения
        pages = convert_from_path(temp_file_path, 300, poppler_path=poppler_path)
        jpg_filenames = file_enumerate(file,temp_dir,pages)
        return zip_file(temp_dir, jpg_filenames, user_id)
    except Exception as e:
        return {"error": str(e)}

def zip_file(temp_dir, jpg_filenames, user_id):
    # Создаем ZIP-архив с сохраненными изображениями
    zip_filename = os.path.join(temp_dir, "converted_images.zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for jpg_filename in jpg_filenames:
            zipf.write(jpg_filename, os.path.basename(jpg_filename))
    add_file_from_path(user_id, zip_filename)
    return {"message": "Conversion successful", "zip_filename": zip_filename,"user_id": user_id}


def file_enumerate(file,temp_dir,pages):
    jpg_filenames = []
    for i, page in enumerate(pages):
        jpg_filename = os.path.join(temp_dir, f"{os.path.splitext(file.filename)[0]}_{i + 1}.jpg")
        page.save(jpg_filename, "JPEG")
        jpg_filenames.append(jpg_filename)
    return jpg_filenames



async def get_pdf_to_img(file_name, user_id):
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