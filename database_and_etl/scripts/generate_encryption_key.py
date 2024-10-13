import base64
import os

def generate_fernet_key():
    # Generate 32 random bytes
    key = os.urandom(32)
    
    # Encode the bytes to base64
    encoded_key = base64.urlsafe_b64encode(key)
    
    # Decode to string for easy copying
    return encoded_key.decode()

if __name__ == "__main__":
    fernet_key = generate_fernet_key()
    print("Generated Fernet Key:")
    print(fernet_key)
    print("\nAdd this key to your .env file as:")
    print(f"ENCRYPTION_KEY={fernet_key}")
    