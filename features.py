import time
import psutil
import os

def timetaken(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        start_time = time.time()
        func(*args,**kwargs)
        end_time = time.time()
        print(f"Time taken to run this program is {end_time-start_time:.10f} seconds")    
    return wrapper

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def track_memory(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))

        return result
    return wrapper