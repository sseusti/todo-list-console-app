from operator import index

from todo_manager import Todo
import inquirer
from inquirer import prompt

def add_task():
    text = input('Введите текст задачи: ')

    priority = input('Укажите приоритет задачи (низкий, высокий, средний): ').capitalize()
    priority = priority if priority else 'Средний'

    tags = input('Введите, если необходимо, теги через пробел: ')
    tags = list(tags.split(' '))

    deadline = input('Введите дедлайн если необходимо: ')

    todo.create_todo(text, priority, tags, deadline)

def leave():
    global is_active
    is_active = False

def nothing(task):
    pass

def make_done(task):
    index = int(task[:2])
    todo.make_done(index)

def delete_task(task):
    index = int(task[:2])
    todo.delete_task(index)

def redact_task(task):
    index = int(task[:2])
    task = todo.get_task(index)

    text = input('Введите новый текст задачи: ')

    priority = input('Укажите новый приоритет задачи (низкий, высокий, средний): ').capitalize()

    tags = input(f'Введите новые теги через пробел (предыдущие: {' '.join(task['tags'])}): ')
    tags = list(tags.split(' '))

    deadline = input('Введите новый дедлайн если необходимо: ')

    new_data = {
        'text': text,
        'priority': priority,
        'tags': tags,
        'deadline': deadline
    }
    todo.redact_task(index, new_data)


def show_tasks():
    tasks_list = todo.show_all_todo()

    tasks = [
            inquirer.List(
                'tasks',
                message='Выберите задачу',
                choices=tasks_list
            )
        ]

    task = prompt(tasks)['tasks']

    if task != 'Выйти':
        tasks_actions_choice = [
            inquirer.List(
                'tasks_actions_choice',
                message='Что сделать с задачей',
                choices=task_actions
            )
        ]

        task_action_choice = prompt(tasks_actions_choice)['tasks_actions_choice']
        task_action = task_actions.get(task_action_choice)

        if task_action:
            task_action(task)

menu_actions = {
    'Добавить задачу': add_task,
    'Показать все задачи': show_tasks,
    'Выйти': leave,
}

task_actions = {
    'Отметить выполненной': make_done,
    'Удалить задачу': delete_task,
    'Редактировать задачу': redact_task,
    'Выйти': nothing
}

if __name__ == '__main__':
    username = input('Введите имя пользователя: ')
    todo = Todo(username)

    is_active = True

    while is_active:
        questions = [
            inquirer.List(
                'choice',
                message='Выберите пункт меню',
                choices=[k for k in menu_actions]
            )
        ]

        choice = prompt(questions)['choice']
        menu_action = menu_actions.get(choice)

        if menu_action:
            menu_action()
