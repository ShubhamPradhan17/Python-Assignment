from features import timetaken, track_memory


@track_memory
@timetaken
def printStatement(name):
    new_name = name.lower()
    lst = [x for x in new_name]
    print(f"Hello, Good Morning. I am {new_name}.")
    return lst




lst = printStatement("Shubham")