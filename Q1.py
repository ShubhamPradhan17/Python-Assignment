def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally :
        print("This is the content of the file")



file_path = 'random.txt'
read_file(file_path)
