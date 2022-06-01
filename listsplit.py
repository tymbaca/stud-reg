def listsplit(list: list, key: str = "", cleanempty=True) -> list:
    """
    
    Делит исходный список на несколько вложенных списоков по ключу.
    Возвращает получившийся список аналогично методу str.split()

    Аргументы:
        key        [str]    - Ключ, относительно которого происходит деление. 
                            На выходе элемент списка, содержащий ключ, не остается.
        cleanempty [bool]   - Когда True, удаляет пустые вложенные списки

    """
    grouped_list = [[]]
    inner_list_index = 0

    for item in list:
        inner_list = grouped_list[inner_list_index]
        if item != key:
            inner_list.append(item)
        else:
            grouped_list.append([])
            inner_list_index += 1
    
    if cleanempty is True:
        grouped_list = clean_empty_inner_lists(grouped_list)
        
    return grouped_list

def clean_empty_inner_lists(lists: list[list]) -> list[list]:
    """Удаляет пустые вложенные списки и возвращает получившийся список"""
    clean_lists = []
    for inner_list in lists:
        if len(inner_list) > 0:
            clean_lists.append(inner_list)
    return clean_lists



if __name__ == "__main__":
    list = ["", 11, 12, 13, "", "", 14, 15, "", 16, ""]
    grouped_list = listsplit(list)
    print(grouped_list)
