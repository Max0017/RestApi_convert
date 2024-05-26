import os
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT
    )
''')

# Создание таблицы файлов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        filename TEXT NOT NULL,
        file_data BLOB NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

def add_user(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    conn.commit()


def add_file_from_path(user_id, file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO files (user_id, filename, file_data) VALUES (?, ?, ?)',
                       (user_id, os.path.basename(file_path), file_data))
        conn.commit()

        # Проверяем успешность добавления файла
        cursor.execute('SELECT COUNT(*) FROM files WHERE user_id = ? AND filename = ?',
                       (user_id, os.path.basename(file_path)))
        count = cursor.fetchone()[0]

        conn.close()

        if count > 0:
            print("Файл успешно добавлен в базу данных")
        else:
            print("Ошибка при добавлении файла в базу данных")
    except Exception as e:
        print("Ошибка:", e)


def get_file(user_id, file_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_data FROM files WHERE user_id = ? AND filename = ?', (user_id, file_name))
    file = cursor.fetchone()
    conn.close()
    if file:
        return file[0]  # file_data is stored in the first column of the result
    else:
        return False


def get_files_for_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files WHERE user_id = ?', (user_id,))
    files = cursor.fetchall()
    conn.close()
    return files

def get_user_id(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()

    if user:
        return user[0]
    else:
        return None
    conn.close()
def check_email_and_password_exists(email,password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ? AND password = ?', (email, password))
    existing_user = cursor.fetchone()
    if existing_user:
        return True
    else:
        return False
    conn.close()


def delete_user_by_email_and_password(email,password):
    try:
        # Устанавливаем соединение с базой данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Получаем ID пользователя по его email
        cursor.execute('SELECT id FROM users WHERE email = ? AND password = ?', (email, password))
        user_id = cursor.fetchone()

        if user_id:
            user_id = user_id[0]  # Получаем ID из кортежа
            # Удаляем пользователя из таблицы "users" по его ID
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

            # Удаляем все связанные записи из других таблиц, если они есть

            # Применяем изменения к базе данных
            conn.commit()
            print(f"Пользователь с email '{email}' успешно удален из базы данных.")
        else:
            print(f"Пользователь с email '{email}' не найден в базе данных.")
            conn.close()

    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)

def change_password(email, new_password):
    try:
        # Устанавливаем соединение с базой данных
        conn = sqlite3.connect('database.db.db')
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь с указанным email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            # Обновляем пароль пользователя
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, email))
            conn.commit()
            return True
        else:
            return False

    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)

    finally:
        # Закрываем соединение с базой данных
        if conn:
            conn.close()





# Завершение работы с базой данных
conn.commit()
conn.close()
