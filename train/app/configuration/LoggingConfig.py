import logging

#logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - L:%(lineno)d - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename="app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)