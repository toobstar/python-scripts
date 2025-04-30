

# Implementation of a naive cypher (https://en.wikipedia.org/wiki/Caesar_cipher)

DICTIONARY = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
              'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', ' ', '.', ',', '!', '?', '@', '#', '$',
              '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
              '{', '}', '[', ']', '|', ':', ';', '"', "'", '<',
              '>', '/', '\\', '`', '~']

DICT_LENGTH = len(DICTIONARY)


def encrypt(cypher, text, reverse=False):
    """
    Encrypts or decrypts a given text using a substitution cipher.

    This function shifts the characters in the input text based on the provided
    cipher key (`cypher`) and the direction specified by the `reverse` flag.
    Characters not present in the `DICTIONARY` are left unchanged.

    Args:
      cypher (int): The number of positions to shift characters in the `DICTIONARY`.
      text (str): The input text to be encrypted or decrypted.
      reverse (bool, optional): If True, decrypts the text by reversing the shift.
                    Defaults to False (encryption mode).

    Returns:
      str: The resulting encrypted or decrypted text.
    """
    result = ""

    for char in text:
        if char in DICTIONARY:
            index = DICTIONARY.index(char)

            if (reverse):
                new_index = index + cypher
            else:
                new_index = index - cypher

            while new_index >= DICT_LENGTH:
                new_index -= DICT_LENGTH

            while new_index < 0:
                new_index += DICT_LENGTH

            result += DICTIONARY[new_index]
        else:
            result += char

    return result


def eval_from_input():
    """
    Prompts the user to input a cypher code (number) and choose between encryption or decryption.

    The function performs the following steps:
    1. Asks the user to input a cypher code and validates that it is a number.
    2. Prompts the user to choose between encryption ('E') or decryption ('D').
    3. Depending on the choice:
       - For encryption, it asks for the text to encrypt and prints the encrypted result.
       - For decryption, it asks for the text to decrypt and prints the decrypted result.
    4. Handles invalid inputs for both the cypher code and the operation choice.

    Note:
    - The `encrypt` function is assumed to handle both encryption and decryption based on the provided parameters.
    - If the cypher code is invalid (not a number), the program exits with an error message.
    - If the operation choice is invalid, an error message is displayed.

    Raises:
      SystemExit: If the cypher code is not a valid number.
    """

    print('Input cypher code (number) for encryption:')
    try:
        cypher = int(input())
    except ValueError:
        print("That's not a validcypher.  Needs to be a number")
        exit(1)

    print('Do you want to encrypt (E) or decrypt (D)?')
    direction = input().lower().strip()

    if direction == 'e':
        print('Input text to encrypt:')
        encrypted = encrypt(cypher, input())
        print('Encrypted:', encrypted)

    elif direction == 'd':
        print('Input text to decrypt:')
        decrypted = encrypt(cypher, input(), True)
        print('Decrypted:', decrypted)

    else:
        print('Invalid option', direction)


if __name__ == "__main__":
    eval_from_input()
