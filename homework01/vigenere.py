def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    az_min = 97
    az_max = 122
    AZ_min = 65
    AZ_max = 90

    keyword = keyword.upper()
    while len(keyword) < len(plaintext):
        keyword += keyword

    for index, letter in enumerate(plaintext):
        code = ord(letter)

        if not ((AZ_min <= code <= AZ_max) or (az_min <= code <= az_max)):
            ciphertext += letter
            continue

        shift_letter = keyword[index]
        shift = ord(shift_letter) - AZ_min

        if AZ_min <= code <= AZ_max:
            if code + shift - AZ_max > 0:
                next_letter = chr(AZ_min + (code + shift - AZ_max) - 1)
            else:
                next_letter = chr(code + shift)
        else:
            if code + shift - az_max > 0:
                next_letter = chr(az_min + (code + shift - az_max) - 1)
            else:
                next_letter = chr(code + shift)

        ciphertext += next_letter

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    az_min = 97
    az_max = 122
    AZ_min = 65
    AZ_max = 90

    keyword = keyword.upper()
    while len(keyword) < len(ciphertext):
        keyword += keyword

    for index, letter in enumerate(ciphertext):
        code = ord(letter)

        shift_letter = keyword[index]
        shift = ord(shift_letter) - AZ_min

        if not ((AZ_min - shift <= code - shift <= AZ_max - shift) or (az_min - shift <= code - shift <= az_max - shift)):
            plaintext += letter
            continue

        if AZ_min - shift <= code - shift <= AZ_max - shift:
            if AZ_min - (code - shift) > 0:
                next_letter = chr(AZ_max - (AZ_min - (code - shift)) + 1)
            else:
                next_letter = chr(code - shift)
        else:
            if az_min - (code - shift) > 0:
                next_letter = chr(az_max - (az_min - (code - shift)) + 1)
            else:
                next_letter = chr(code - shift)

        plaintext += next_letter

    return plaintext
