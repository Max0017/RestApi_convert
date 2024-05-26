import os
import sqlite3
def chek_file_name(file_name, file_mapping):
    for file in file_mapping:
        path_file_name = file_name
        last_slash_index = path_file_name.rfind('\\')  # Находим индекс последнего вхождения символа '\'
        if last_slash_index != -1:  # Проверяем, что символ был найден
            new_path_file_name = path_file_name[last_slash_index:]  # Обрезаем строку до этого индекса
        path_file = file
        last_slash_index_file = path_file.rfind('\\')
        if last_slash_index_file != -1:
            new_path_file = path_file[last_slash_index_file:]
        if new_path_file == new_path_file_name:
            return True


def remove_character_after_slash(path):
    result = []
    skip_next = False

    for i in range(len(path)):
        if skip_next:
            skip_next = False
            continue

        if path[i] == "\\":
            result.append("\\")
            skip_next = True  # Установить флаг для пропуска следующего символа
        else:
            result.append(path[i])

    return "".join(result)

def refactor_name_file(file_name):
    for file in file_name:
        path_file_name = file_name
        last_slash_index = path_file_name.rfind('\\')  # Находим индекс последнего вхождения символа '\'
        if last_slash_index != -1:  # Проверяем, что символ был найден
            new_path_file_name = path_file_name[last_slash_index+1:]  # Обрезаем строку до этого индекса
            return new_path_file_name


