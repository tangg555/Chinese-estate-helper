import hashlib


class ParserTools(object):
    @classmethod
    def generate_md5(cls, string_: str):
        m = hashlib.md5()
        m.update(string_.encode('utf-8'))
        return m.hexdigest()
