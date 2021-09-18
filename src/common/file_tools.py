import os


class FileTools(object):
    @classmethod
    def info_to_file(cls, info, local_path: str):
        with open(local_path, 'w', encoding='utf-8') as fw:
            fw.write(f'{info}')

    @classmethod
    def info_append_to_file(cls, info, local_path: str):
        with open(local_path, 'a', encoding='utf-8') as fw:
            fw.write(f'{info}')
