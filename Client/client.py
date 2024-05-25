import tkinter as tk
from tkinter import filedialog
import requests

# URL вашего сервера
SERVER_URL = 'http://localhost:8000'

name_button = "выбрать изображения"
def convert_image_to_pdf(image_path):
    # Создаем URL для конечной точки, которая конвертирует изображение в PDF
    endpoint_url = f'{SERVER_URL}/convert/jpg_to_pdf'

    # Открываем файл изображения
    with open(image_path, 'rb') as image_file:
        # Отправляем POST-запрос на сервер с файлом изображения в формате multipart/form-data
        response = requests.post(endpoint_url, files={'file': image_file})
        # Проверяем успешность запроса
        if response.status_code == 200:
            name_button = "скачать pdf файл"
            name_main(name_button,download_file())
            print('Изображение успешно сконвертировано в PDF')
        else:
            print('Ошибка при конвертации изображения в PDF:', response.text)

def download_file():
    endpoint_url = f'{SERVER_URL}/convert/jpg_to_pdf/download'
    response = requests.get(endpoint_url)
    if response.status_code == 200:
            # Сохраняем файл
        with open("pdf_file.pdf", 'wb') as file:
            file.write(response.content)
            print('Файл успешно сохранен')
    else:
        print('Скачивание отменено')

def browse_image():
    global filename
    # Открываем диалоговое окно выбора файла для выбора изображения
    filename = filedialog.askopenfilename()
    if filename:
        # Вызываем функцию конвертации изображения в PDF с выбранным файлом
        convert_image_to_pdf(filename)


def name_main(name_button , button_command):
    root = tk.Tk()
    root.title("Конвертер изображений в PDF")
    # Создаем кнопку для выбора изображения
    browse_button = tk.Button(root, text= name_button, command= button_command)
    browse_button.pack(pady=10)

    # Запускаем главный цикл обработки событий
    root.mainloop()
name_main(name_button,browse_image)
convert_image_to_pdf()
download_file()