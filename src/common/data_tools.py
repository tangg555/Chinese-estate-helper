from .string_tools import StringTools


class DataTools(object):


    '''
    ============================ filters ============================
    '''

    @classmethod
    def containing_filter(cls, class_type: type, obj_list: list, attr: str, keyword: str):
        filtered = []
        for obj in obj_list:
            if StringTools.contain(eval(f'{obj}.{attr}'), keyword):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def or_containing_filter(cls, class_type: type, obj_list: list, attr: str, keywords: list):
        filtered = []
        for obj in obj_list:
            if StringTools.multi_or_contain(eval(f'{obj}.{attr}'), keywords):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def and_containing_filter(cls, class_type: type, obj_list: list, attr: str, keywords: list):
        filtered = []
        for obj in obj_list:
            if StringTools.multi_and_contain(eval(f'{obj}.{attr}'), keywords):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def group(cls, class_type: type, obj_list: list, attr: str) -> dict:
        group_dict = {}
        for obj in obj_list:
            key = eval(f'paper.{attr}')
            if key not in group_dict:
                group_dict[key] = class_type()
            group_dict[key].houses.append(obj)
        return group_dict
