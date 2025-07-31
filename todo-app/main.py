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
    i = int(task[:2])
    todo.make_done(i)


def delete_task(task):
    i = int(task[:2])
    todo.delete_task(i)


def redact_task(task):
    i = int(task[:2])
    task = todo.get_task(i)

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
    todo.redact_task(i, new_data)


def add_deadline(task):
    i = int(task[:2])
    task = todo.get_task(i)
    deadline = input(f'Укажите дедлайн в формате дд-мм-гг (старый - {task['deadline']}): ')
    todo.add_deadline(i, deadline)


def show(tasks_list):
    tasks = [
        inquirer.List(
            'tasks',
            message='Выберите задачу',
            choices=tasks_list
        )
    ]

    task = prompt(tasks)['tasks']

    if task == 'Очистить выполненные':
        todo.clear_done()

    elif task != 'Выйти':
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

def show_tasks():
    tasks_list = todo.show_all_todo()
    show(tasks_list)


def show_overdue():
    tasks_list = todo.show_overdue()
    show(tasks_list)

def show_by_tag():
    all_tags = todo.get_tags()
    tag = input(f'Выберите тег ({' '.join(all_tags)} ): ')
    task_list = todo.show_tasks_by_tag(tag)
    show(task_list)


menu_actions = {
    'Добавить задачу': add_task,
    'Показать все задачи': show_tasks,
    'Показать просроченные задачи': show_overdue,
    'Показать задачи по тегу': show_by_tag,
    'Выйти': leave,
}

task_actions = {
    'Отметить выполненной': make_done,
    'Удалить задачу': delete_task,
    'Редактировать задачу': redact_task,
    'Добавить дедлайн': add_deadline,
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
