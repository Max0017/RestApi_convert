import os
import tempfile

from fastapi import HTTPException
from starlette.responses import FileResponse
from PIL import Image
from cheking_file_name import chek_file_name
from register_user import add_file_from_path, get_file
from cheking_file_name import refactor_name_file
from starlette.responses import FileResponse, StreamingResponse

async def post_img_to_pdf(file_name,user_id):
    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file_name.read())
            temp_file_path = temp_file.name
        temp_dir = tempfile.mkdtemp()
        image = Image.open(temp_file_path)
        #pdf_filename = os.path.join(file_name.filename)[0] + ".pdf"
        global pdf_filename
        pdf_filename = os.path.join(temp_dir, f"{os.path.splitext(file_name.filename)[0]}.pdf")
        image.save(pdf_filename, "PDF", resolution=100.0)
        add_file_from_path(user_id, pdf_filename)
        return {"message": "Conversion successful", "pdf_filename": pdf_filename, "user_id": user_id}
    except Exception as e:
        return {"error": str(e)}


async def get_img_to_pdf(file_name, user_id):
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