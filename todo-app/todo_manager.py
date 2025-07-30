import json

class Todo:

    def __init__(self, username):
        self.file = f"data/{username}.json"
        self.username = username
        data = self.__load()
        self.__dump(data)
        self.current_id = self.__get_current_id()

    def __load(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f'Зарегистрирован пользователь {self.username}')
            data = {
                'current_id': 0,
                'tasks': []
            }
        return data

    def __dump(self, data):
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return

    def __get_current_id(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            current_id = data['current_id']
            return current_id

    def create_todo(self, text, priority, tags, deadline):
        new_task = {
            'id': self.current_id,
            'text': text,
            'done': False,
            'priority': priority,
            'tags': tags,
            'deadline': deadline,
        }

        data = self.__load()
        data['tasks'].append(new_task)

        self.current_id += 1
        data['current_id'] += 1

        self.__dump(data)
        print("Задача успешно добавлена!")

    def show_all_todo(self):
        data = self.__load()
        # tasks = [f'{i} | {task["text"]}' for i, task in enumerate(data['tasks'])]
        tasks = []
        for i, task in enumerate(data['tasks']):
            if task['done']:
                new_task = f'{i} | {task["text"]} - Выполнено'
            else:
                new_task = f'{i} | {task["text"]}'

            tasks.append(new_task)
        tasks.append('Выйти')

        return tasks

    def make_done(self, index):
        data = self.__load()
        data['tasks'][index]['done'] = not data['tasks'][index]['done']
        self.__dump(data)

    def delete_task(self, index):
        data = self.__load()
        data['tasks'].pop(index)
        self.__dump(data)

    def get_task(self, index):
        data = self.__load()
        task = data['tasks'][index]
        return task

    def redact_task(self, index, new_data):
        data = self.__load()
        for k, v in new_data.items():
            if v != '':
                data['tasks'][index][k] = v

        self.__dump(data)

