import sys
import string

class KeyLengthError(Exception):
    pass


alphabet = list(string.ascii_lowercase)

# Create dictionaries for letter-to-index and index-to-letter 
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def adjust_key_length(key):
    # Define a list of characters to remove from the key
    bad_chars = [';', ':', '*', " ", "\\", '"']
    cleaned_key = key
    # Remove "bad" characters from the key
    for char in bad_chars:
        cleaned_key = cleaned_key.replace(char, '')
    
    # Calculate the length of the cleaned key
    key_length = len(cleaned_key)
    print("Cleaned key:", cleaned_key)
    print("Key length:", key_length)
    # Check if the key length is allowed 
    if not 8 <= key_length <= 12:
        raise KeyLengthError("Key length must be between 8 and 12 characters.")
    return cleaned_key


def shift_key(key, offset):
    # Adjust the key length
    adjusted_key = adjust_key_length(key)
    shifted_key = ""
    # Iterate over each letter in the adjusted key
    for letter in adjusted_key:
        # Shift the letter by the specified offset
        if letter in alphabet:
            shifted_index = (letter_to_index[letter] + offset) % len(alphabet)
            shifted_key += index_to_letter[shifted_index]
    return shifted_key


def encrypt(message, key, offset):
    encrypted = ""
    # Shift the key by the offset
    shifted_key = shift_key(key.lower(), offset)
    # Split the message into parts based on the length of the shifted key
    split_message = [message[i:i + len(shifted_key)] for i in range(0, len(message), len(shifted_key))]
    for each_split in split_message:
        # Iterate over each letter in the part and corresponding letter in the shifted key
        for letter, k in zip(each_split, shifted_key):
            if letter in alphabet:
                number = (letter_to_index[letter] + letter_to_index[k]) % len(alphabet)
                encrypted += index_to_letter[number]
            else:
                encrypted += letter  
    return encrypted


def decrypt(cipher, key, offset):
    decrypted = ""
    # Shift the key by the offset
    shifted_key = shift_key(key.lower(), offset)
    # Split the encrypted message into parts based on the length of the shifted key
    split_encrypted = [cipher[i:i + len(shifted_key)] for i in range(0, len(cipher), len(shifted_key))]
    for each_split in split_encrypted:
        # Iterate over each letter in the part and corresponding letter in the shifted key
        for letter, k in zip(each_split, shifted_key):
            if letter in alphabet:
                number = (letter_to_index[letter] - letter_to_index[k]) % len(alphabet)
                decrypted += index_to_letter[number]
            else:
                decrypted += letter  
    return decrypted


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python main.py <-e/-d> <message> <key> <offset>")
        return

    # Parse command-line arguments
    action = sys.argv[1]
    message = sys.argv[2]
    key = sys.argv[3]
    offset = int(sys.argv[4])

    try:
        if action == "-e":
            encrypted_message = encrypt(message.lower(), key.lower(), offset)
            print("Original message:", message)
            print("Encrypted message:", encrypted_message)

        elif action == "-d":
            decrypted_message = decrypt(message.lower(), key.lower(), offset)
            print("Original message:", message)
            print("Decrypted message:", decrypted_message)

        else:
            print("Invalid action! Please use '-e' for encryption or '-d' for decryption.")
    except KeyLengthError as e:
        print("Key length error:", e)


if __name__ == "__main__":
    main()
