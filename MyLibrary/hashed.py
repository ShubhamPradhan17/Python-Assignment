import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

plain_password = 'Password123'
hashed = hash_password(plain_password)
print(f'Hashed Password: {hashed}')

is_correct = check_password(hashed, plain_password)
print(f'Password match: {is_correct}')
