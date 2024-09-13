import bcrypt

# Function to hash a password
def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to check if a password matches the hashed password
def check_password(stored_password: str, provided_password: str) -> bool:
    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Example usage
plain_password = 'Password123'
hashed = hash_password(plain_password)
print(f'Hashed Password: {hashed}')

# Verify password
is_correct = check_password(hashed, plain_password)
print(f'Password match: {is_correct}')
