
from image_to_pdf import post_img_to_pdf , get_img_to_pdf
from fastapi import FastAPI, UploadFile, File
from pdf_to_image import post_pdf_to_img,get_pdf_to_img
from docx_to_pdf import post_convert_docx_to_pdf,get_convert_docx_to_pdf
from pdf_to_docx import post_convert_pdf_to_docx,get_convert_pdf_to_docx
from pptx_to_pdf import post_convert_pptx_to_pdf, get_convert_pptx_to_pdf
from pdf_to_pptx import post_pdf_to_pptx , get_convert_pdf_to_pptx
from txt_to_pdf import  post_convert_txt_to_pdf, get_convert_txt_to_pdf
from register_user import (add_user,check_email_and_password_exists, delete_user_by_email_and_password,
                           get_user_id, change_password)
app = FastAPI()


@app.post("/register/client/{email}{password}")
async def register_user(email: str, password: str):
    if check_email_and_password_exists(email,password) == True:
        add_user(email,password)
        user_id = get_user_id(email,password)
        return {"message": "Успешно зарегистрирован" }, str(user_id)
    else:
        return {"message": "ползователь с такими даннымый существует"}
@app.get("/login/client/{email}{password}")
async def login_user(email: str, password: str):
    if check_email_and_password_exists(email,password) == True:
        return str(get_user_id(email,password))
@app.put("/register/user/{email}{new_password}")
async def update_user(email: str, new_password: str):
    if change_password(email,new_password) == True:
        return {"message": "Пароль успешно изменен"}


@app.post("/convert/jpg_to_pdf/{user_id}")
async def convert_jpg_to_pdf(user_id: str, file: UploadFile = File(...)):
   return await post_img_to_pdf(file, user_id)


@app.get("/convert/jpg_to_pdf/download/{filename}{user_id}")
async def get_convert_jpg_to_pdf(filename: str, user_id: str):
   return await get_img_to_pdf(filename, user_id)


@app.post("/convert/pdf_to_jpg/{user_id}")
async def convert_pdf_to_jpg(user_id: str, file: UploadFile = File(...)):
  return await post_pdf_to_img(file, user_id)

# Эндпоинт для скачивания архива с изображениями
@app.get("/download_images/{filename}{user_id}")
async def download_images(filename: str, user_id: str):
    return await get_pdf_to_img(filename, user_id)


@app.post("/convert/docx_to_pdf/{user_id}")
async def post_cnvert_docx_to_pdf(user_id: str, file: UploadFile = File(...)):
    return await post_convert_docx_to_pdf(file, user_id)


@app.get("/convert/docx_to_pdf/download/{filename}{user_id}")
async def get_cnvert_docx_to_pdf(filename: str, user_id: str):
    return await get_convert_docx_to_pdf(filename, user_id)


@app.post("/convert/pdf_to_docx/{user_id}")
async def post_conv_pdf_to_docx(user_id: str, file: UploadFile = File(...)):
    return await post_convert_pdf_to_docx(file, user_id)


@app.get("/convert/pdf_to_docx/download/{filename}{user_id}")
async def get_conv_pdf_to_docx(filename: str, user_id: str):
    return await get_convert_pdf_to_docx(filename, user_id)

@app.post("/convert/pptx_to_pdf/{user_id}")
async def post_cnvert_pptx_to_pdf(user_id: str, file: UploadFile = File(...)):
    return await post_convert_pptx_to_pdf(file, user_id)

@app.get("/convert/pptx_to_pdf/download/{filename}{user_id}")
async def get_conv_pptx_to_pdf(filename: str, user_id: str):
    return await get_convert_pptx_to_pdf(filename, user_id)

@app.post("/convert/pdf_to_pptx/{user_id}")
async def post_conv_pdf_to_pptx(user_id: str, file: UploadFile = File()):
    return await post_pdf_to_pptx(file, user_id)


@app.get("/convert/pdf_to_pptx/download/{filename}{user_id}")
async def post_conv_pdf_to_pptx(filename: str, user_id: str):
    return await get_convert_pdf_to_pptx(filename, user_id)


@app.post("/convert/txt_to_pdf/{user_id}")
async def post_txt_to_pdf(user_id: str, file: UploadFile = File()):
    return await post_convert_txt_to_pdf(file, user_id)


@app.get("/convert/txt_to_pdf/download/{filename}{user_id}")
async def post_txt_to_pdf(filename: str, user_id: str):
    return await get_convert_txt_to_pdf(filename,user_id)
@app.delete("/user/delete/{email}{password}")
async def delete_user(email: str, password: str):
    return await delete_user_by_email_and_password(email, password)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
