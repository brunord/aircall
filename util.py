import os

data_dir = os.path.join(os.path.dirname(__file__), 'resources', 'data')


def data_file():
    return [i for i in os.listdir(data_dir) if i.endswith(".json")][0]


def data_file_abs():
    return f"{data_dir}/{data_file()}"