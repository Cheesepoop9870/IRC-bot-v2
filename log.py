#this is deprecated, is now built into main.py
import logging


logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file named 'app.log'
    filemode='w'         # Append to the file (default is 'a', 'w' for overwrite)
)

logging.debug('This is a debug message')  
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')