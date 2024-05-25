import os
import tempfile
import zipfile
from pdf2image import convert_from_path
from starlette.responses import FileResponse


async def post_pdf_to_img(file):
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
        return zip_file(temp_dir, jpg_filenames)
    except Exception as e:
        return {"error": str(e)}

def zip_file(temp_dir, jpg_filenames):
    # Создаем ZIP-архив с сохраненными изображениями
    zip_filename = os.path.join(temp_dir, "converted_images.zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for jpg_filename in jpg_filenames:
            zipf.write(jpg_filename, os.path.basename(jpg_filename))
    return {"message": "Conversion successful", "zip_filename": zip_filename}


def file_enumerate(file,temp_dir,pages):
    jpg_filenames = []
    for i, page in enumerate(pages):
        jpg_filename = os.path.join(temp_dir, f"{os.path.splitext(file.filename)[0]}_{i + 1}.jpg")
        page.save(jpg_filename, "JPEG")
        jpg_filenames.append(jpg_filename)
    return jpg_filenames



async def get_pdf_to_img(file_name):
    try:
        if isinstance(file_name, str):
            file_name = file_name.encode("utf-8")
        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(file_name)}"
        }
        return FileResponse(path=file_name, media_type="application/zip", headers=headers)
    except Exception as e:
        return {"error": str(e)}