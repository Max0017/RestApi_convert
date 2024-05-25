
from image_to_pdf import post_img_to_pdf , get_img_to_pdf
from fastapi import FastAPI, UploadFile, File
from pdf_to_image import post_pdf_to_img,get_pdf_to_img
from docx_to_pdf import post_convert_docx_to_pdf,get_convert_docx_to_pdf
from pdf_to_docx import post_convert_pdf_to_docx,get_convert_pdf_to_docx
from pptx_to_pdf import post_convert_pptx_to_pdf, get_convert_pptx_to_pdf
app = FastAPI()

@app.post("/convert/jpg_to_pdf")
async def convert_jpg_to_pdf(file: UploadFile = File(...)):
   return await post_img_to_pdf(file)


@app.get("/convert/jpg_to_pdf/download/{filename}")
async def get_convert_jpg_to_pdf(filename : str):
   return await get_img_to_pdf(filename)


@app.post("/convert/pdf_to_jpg")
async def convert_pdf_to_jpg(file: UploadFile = File(...)):
  return await post_pdf_to_img(file)

# Эндпоинт для скачивания архива с изображениями
@app.get("/download_images/{filename}")
async def download_images(filename: str):
    return await get_pdf_to_img(filename)


@app.post("/convert/docx_to_pdf")
async def post_cnvert_docx_to_pdf(file: UploadFile = File(...)):
    return await post_convert_docx_to_pdf(file)


@app.get("/convert/docx_to_pdf/download/{filename}")
async def get_cnvert_docx_to_pdf(filename : str):
    return await get_convert_docx_to_pdf(filename)


@app.post("/convert/pdf_to_docx")
async def post_conv_pdf_to_docx(file: UploadFile = File(...)):
    return await post_convert_pdf_to_docx(file)


@app.get("/convert/pdf_to_docx/download/{filename}")
async def get_conv_pdf_to_docx(filename : str):
    return await get_convert_pdf_to_docx(filename)

@app.post("/convert/pptx_to_pdf")
async def post_cnvert_pptx_to_pdf(file: UploadFile = File(...)):
    return await post_convert_pptx_to_pdf(file)

@app.get("/convert/pptx_to_pdf/download/{filename}")
async def get_conv_pptx_to_pdf(filename : str):
    return await get_convert_pptx_to_pdf(filename)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
