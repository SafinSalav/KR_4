import json


class JsonSaver:
    def __init__(self, path):
        self.path = path

    def load_json(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            pass

    def dump_json(self, data):
        if self.load_json() is not None:
            question = ''
            while question.lower() not in ['да', 'нет']:
                question = input(f'Файл {self.path} существует. Перезаписать файл? (да/нет)')
            if 'нет' == question.lower():
                return False
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
