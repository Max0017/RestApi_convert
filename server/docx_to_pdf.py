import os
import tempfile

from fastapi import HTTPException

from register_user import add_file_from_path, get_file, get_files_for_user
from docx2pdf import convert
from starlette.responses import FileResponse, StreamingResponse
from cheking_file_name import chek_file_name, remove_character_after_slash,refactor_name_file
file_mapping = []
async def post_convert_docx_to_pdf(file_name, user_id):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            temp_file.write(await file_name.read())
            temp_file_path = temp_file.name
        temp_dir = tempfile.mkdtemp()
        global pdf_filename
        pdf_filename = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(file_name.filename))[0]}.pdf")
        convert(temp_file_path, pdf_filename)
        file_mapping.append((pdf_filename))
        add_file_from_path(user_id, pdf_filename)
        return {"message": "Conversion successful", "pdf_filename": pdf_filename,"user_id": user_id}
    except Exception as e:
        return {"error": str(e)}

async def get_convert_docx_to_pdf(file_name, user_id):
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