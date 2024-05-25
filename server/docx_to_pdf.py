import os
import tempfile

from docx2pdf import convert
from starlette.responses import FileResponse


async def post_convert_docx_to_pdf(file_name):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            temp_file.write(await file_name.read())
            temp_file_path = temp_file.name
        temp_dir = tempfile.mkdtemp()
        # Преобразуем файл docx в pdf
        pdf_filename = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(file_name.filename))[0]}.pdf")
        convert(temp_file_path, pdf_filename)
        return {"message": "Conversion successful", "pdf_filename": pdf_filename}
    except Exception as e:
        return {"error": str(e)}

async def get_convert_docx_to_pdf(file_name):
    try:
        # Если file_name является строкой, кодируем ее в UTF-8
        if isinstance(file_name, str):
            file_name = file_name.encode("utf-8")
        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(file_name)}"
        }
        return FileResponse(path=file_name, media_type="application/pdf", headers=headers)
    except Exception as e:
        return {"error": str(e)}