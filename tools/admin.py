from config import admins_list

def check(id):
    return True if id in admins_list else False