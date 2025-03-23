import configparser


def remove_data_config(new_data) -> bool:
    """Функция обновления данных файла config
    """

    # Write the configuration to a file
    with open('C:\\vision\\setting.ini', 'w') as configfile:
        new_data.write(configfile)

    return True


def update_data_config(new_data) -> bool:
    """Функция обновления данных файла config
    """

    # Write the configuration to a file
    with open('C:\\vision\\setting.ini', 'a') as configfile:
        new_data.write(configfile)

    return True


def read_data_config() -> configparser.ConfigParser:
    """Функция чтения данных из файла .config"""

    config = configparser.ConfigParser()
    try:
        config.read("C:\\vision\\setting.ini")
        print(config.sections())
    except Exception as e:
        print(e)
        return {}
    else:
        return config