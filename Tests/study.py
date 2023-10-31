todo_list = []

while True:
    print('===ToDo List===')
    print('1. Добавить задачу')
    print('2. Удалить задачу')
    print('3. Список задач')
    print('4. Выйти')

    choice = input('Выберите действие: ')

    if choice == '1':
        newtask = input('Введите новую задачу: ')
        todo_list.append(newtask)
        print('Задача добавлена.')

    elif choice == '2':
        print('Какую из задач нужно удалить?')
        if todo_list:
            for i, task in enumerate(todo_list, start=1):
                print(f'{i}. {task}')
            taskdel = int(input('Введите номер задачи: '))
            if 1 <= taskdel <= len(todo_list):
                todo_list.pop(taskdel - 1)
                print(f'Задача "{taskdel}" удалена.')
            else:
                print('Неверный номер задачи.')
        else:
            print('Список задач пуст.')
    
    elif choice == '3':
        if todo_list:
            print('Список задач: ')
            for i, task in enumerate(todo_list, start=1):
                    print(f'{i}. {task}')
        else:
            print('Список задач пуст.')
    
    elif choice == '4':
        break
    else:
        print('Неверный выбор, выберите действие из меню.')
