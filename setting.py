import configparser
from modules import *
from password_generator import PasswordGenerator


def reload_user():
    config_data = read_data_config()
    try:
        user_id = config_data.getint("user", "uid")
    except:
        user_id = None
    return int(user_id, 2)


is_internet = check_internet()
is_dir = main_directroy()

if is_dir:
    config_data = read_data_config()

# Данные по логгированию
loggin_lvl = config_data.get('general', 'log_level')

# Данные пользователя
try:
    user_id = config_data.getint("user", "uid")
except:
    user_id = None


pwo = PasswordGenerator()