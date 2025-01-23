def file_name_check(file_name):
    if not isinstance(file_name, str):
        return 'No'
    if file_name.count('.')!= 1:
        return 'No'
    name, extension = file_name.split('.')
    if not name or not name[0].isalpha():
        return 'No'
    if sum(c.isdigit() for c in name) > 3:
        return 'No'
    if extension not in ['txt', 'exe', 'dll']:
        return 'No'
    return 'Yes'