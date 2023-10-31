import psycopg2
from psycopg2 import sql

hostname = 'localhost'
user = 'postgres'
password = 'postgres'
db_name = 'test'
port_id = 5432

# Connect database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host = hostname,
            user = user,
            password = password,
            dbname = db_name,
            port = port_id)
        return connection
    except Exception as error:
        print(error)

# Create table
def create_task_table(connection):
    create_script = '''CREATE TABLE IF NOT EXISTS todolist(
                    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    task_name varchar(100) NOT NULL,
                    task_description varchar(250) NOT NULL,
                    task_written_by varchar(50) NOT NULL,
                    task_written_for varchar(50) NOT NULL,
                    task_done BOOLEAN);'''
    try:
        cursor = connection.cursor()
        cursor.execute(create_script)
        connection.commit()
        cursor.close()
    except Exception as error:
        print(error)


# Add a task
def add_task(connection, task_name, task_description, task_written_by, task_written_for):
    insert_task_script = sql.SQL('''INSERT INTO todolist (task_name, task_description, task_written_by, task_written_for, task_done)
                            VALUES ({}, {}, {}, {}, {});''').format(
                                sql.Literal(task_name),
                                sql.Literal(task_description),
                                sql.Literal(task_written_by),
                                sql.Literal(task_written_for),
                                sql.Literal(False)
                            )
    try:
        cursor = connection.cursor()
        cursor.execute(insert_task_script)
        connection.commit()
        cursor.close()
        print('The task has been added')
    except Exception as error:
        print(error)

# Select_all_tasks
def view_tasks(connection):
    select_all_tasks = '''SELECT * FROM todolist ORDER BY id;'''
    try:
        cursor = connection.cursor()
        cursor.execute(select_all_tasks)
        tasks = cursor.fetchall()
        if len(tasks) == 0:
            print('It is empty')
        else:
            print('Here is all your task table: ')
            for task in tasks:
                print(f'''ID: {task[0]}
                        Task name: {task[1]},
                        Task Description: {task[2]},
                        Issued by: {task[3]},
                        Task received: {task[4]},
                        Status: {task[5]}''')
        cursor.close()
    except Exception as error:
        print(error)

# Delete a task
def delete_task(connection, id):
    deletequery_task = '''DELETE FROM todolist WHERE id = %s'''
    try:
        cursor = connection.cursor()
        id = int(id)
        cursor.execute(deletequery_task, (id,))
        connection.commit()
        cursor.close()
        print('The task has been deleted')
    except Exception as error:
        print(error)

# Complete a task
def complete_task(connection, id):
    if id is not None:
        completequery_task = '''UPDATE todolist SET task_done = True WHERE id = %s'''
        try:
            cursor = connection.cursor()
            id = int(id)
            cursor.execute(completequery_task, (id,))
            connection.commit()
            cursor.close()
            print('The status has been changed')
        except Exception as error:
            print(error)


if __name__ == '__main__':
    connection = connect_to_db()
    create_task_table(connection)

    while True:
        print('===ToDo List===')
        print('\nChoose an action')
        print('1. Add a task')
        print('2. Delete a task')
        print('3. View tasks')
        print('4. Mark task as completed')
        print('5. Quit')

        choice = input('Input here: ')

        if choice == '1':
            task_name = input('Input a task name: ')
            task_description = input('Input a task description: ')
            task_written_by = input('Input who is writing a task: ')
            task_written_for = input('Input who is receiving a task: ')
            add_task(connection, task_name, task_description, task_written_by, task_written_for)

        elif choice == '2':
            task_id = input('Input ID which you want to delete: ')
            delete_task(connection, task_id)
        
        elif choice == '3':
            view_tasks(connection)

        elif choice == '4':
            task_id = input('Input ID which you want to mark as completed: ')
            complete_task(connection, task_id)

        elif choice == '5':
            connection.close()
            print('Table is closed')
            break
        else:
            print('It is not possible')