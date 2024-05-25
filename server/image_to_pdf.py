import os
import tempfile

from starlette.responses import FileResponse
from PIL import Image


async def post_img_to_pdf(file_name):
    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file_name.read())
            temp_file_path = temp_file.name
        temp_dir = tempfile.mkdtemp()
        image = Image.open(temp_file_path)
        #pdf_filename = os.path.join(file_name.filename)[0] + ".pdf"
        pdf_filename = os.path.join(temp_dir, f"{os.path.splitext(file_name.filename)[0]}.pdf")
        image.save(pdf_filename, "PDF", resolution=100.0)
        return {"message": "Conversion successful", "pdf_filename": pdf_filename}
    except Exception as e:
        return {"error": str(e)}


async def get_img_to_pdf(file_name):
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