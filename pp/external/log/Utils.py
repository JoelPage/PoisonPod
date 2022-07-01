import logging

logging.basicConfig(filename='pp.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def debug(txt):
    print(txt)
    logging.debug(txt)

def info(txt):
    print(txt)
    logging.info(txt)