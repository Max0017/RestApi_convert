from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import os
import tempfile
import uvicorn
from cheking_file_name import chek_file_name
file_mapping = []


def conv_txt_to_pdf(txt_path, pdf_path):
    with open(txt_path, 'r', encoding='utf-8') as txt_file:  # Указываем кодировку UTF-8
        text = txt_file.read()

    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 40

    lines = text.split('\n')
    y_position = height - margin

    for line in lines:
        if y_position <= margin:
            pdf.showPage()
            y_position = height - margin
        pdf.drawString(margin, y_position, line)
        y_position -= 14

    pdf.save()



async def post_convert_txt_to_pdf(file, user_id):
    try:
        # Создаем временный TXT файл
        temp_txt_path = ''
        temp_pdf_path = ''
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt_file:
                temp_txt_file.write(await file.read())
                temp_txt_path = temp_txt_file.name

            # Создаем временный PDF файл
            temp_pdf_path = os.path.splitext(temp_txt_path)[0] + ".pdf"

            # Конвертируем TXT в PDF
            conv_txt_to_pdf(temp_txt_path, temp_pdf_path)
        finally:
            # Удаляем временный TXT файл после завершения всех операций
            if temp_txt_path and os.path.exists(temp_txt_path):
                os.remove(temp_txt_path)
        file_mapping.append(str(temp_pdf_path))
        # Возвращаем путь к PDF файлу
        file_mapping.clear()
        return {"message": "Conversion successful", "pdf_filename": temp_pdf_path, "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def get_convert_txt_to_pdf(file_name, user_id):
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="File not found")

        # Возвращаем PDF файл
        if chek_file_name(file_name, file_mapping) == True:
            headers = {
                "Content-Disposition": f"attachment; filename={os.path.basename(file_name)}"
            }
            return FileResponse(path=file_name, media_type="application/pdf", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

