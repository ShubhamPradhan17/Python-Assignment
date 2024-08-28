# Build a retry decorator with retry time and retry interval to run a function 3 time with interval of 3 sec
import datetime
import time

def retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            start = datetime.datetime.now()
            result = func()
            print(start)
            time.sleep(3)
        return result
    return wrapper


@retry
def hello():
    print("Hello")


hello()