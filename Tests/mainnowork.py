import psycopg2
from psycopg2 import sql

# Подключение к PostgreSQL базе данных
def connect_to_db():
    try:
        connection = psycopg2.connect(
            database="test",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return connection
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)

# Создание таблицы задачy
def create_task_table(connection):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_name TEXT NOT NULL,
            task_description TEXT,
            task_done BOOLEAN
        );
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Ошибка при создании таблицы задач:", e)

# Добавление задачи
def add_task(connection, task_name, task_description):
    insert_task_query = sql.SQL('INSERT INTO tasks (task_name, task_description, task_done) VALUES ({}, {}, {});').format(
        sql.Literal(task_name),
        sql.Literal(task_description),
        sql.Literal(False)
    )
    try:
        cursor = connection.cursor()
        cursor.execute(insert_task_query)
        connection.commit()
        cursor.close()
        print("Задача добавлена успешно.")
    except psycopg2.Error as e:
        print("Ошибка при добавлении задачи:", e)

# Просмотр списка задач
def view_tasks(connection):
    select_tasks_query = "SELECT * FROM tasks;"
    try:
        cursor = connection.cursor()
        cursor.execute(select_tasks_query)
        tasks = cursor.fetchall()
        if len(tasks) == 0:
            print("Список задач пуст.")
        else:
            for task in tasks:
                print(f"ID: {task[0]}, Название: {task[1]}, Описание: {task[2]}, Выполнено: {task[3]}")
        cursor.close()
    except psycopg2.Error as e:
        print("Ошибка при просмотре списка задач:", e)

if __name__ == "__main__":
    connection = connect_to_db()
    create_task_table(connection)

    while True:
        print("\nВыберите действие:")
        print("1. Добавить задачу")
        print("2. Просмотреть задачи")
        print("3. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            task_name = input("Введите название задачи: ")
            task_description = input("Введите описание задачи: ")
            add_task(connection, task_name, task_description)
        elif choice == "2":
            view_tasks(connection)
        elif choice == "3":
            connection.close()
            print("Выход из приложения.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите существующее действие.")
