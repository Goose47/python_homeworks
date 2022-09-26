import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    az_min = 97
    az_max = 122
    AZ_min = 65
    AZ_max = 90

    for letter in plaintext:
        code = ord(letter) + shift

        if not ((AZ_min + shift <= code <= AZ_max + shift) or (az_min + shift <= code <= az_max + shift)):
            ciphertext += letter
            continue

        if AZ_min + shift <= code <= AZ_max + shift:
            if code - AZ_max > 0:
                next_letter = chr(AZ_min + (code - AZ_max) - 1)
            else:
                next_letter = chr(code)
        else:
            if code - az_max > 0:
                next_letter = chr(az_min + (code - az_max) - 1)
            else:
                next_letter = chr(code)

        ciphertext += next_letter

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    az_min = 97
    az_max = 122
    AZ_min = 65
    AZ_max = 90

    for letter in ciphertext:
        code = ord(letter) - shift

        if not ((AZ_min - shift <= code <= AZ_max) or (az_min - shift <= code <= az_max)):
            plaintext += letter
            continue

        if AZ_min - shift <= code <= AZ_max - shift:
            if AZ_min - code > 0:
                next_letter = chr(AZ_max - (AZ_min - code) + 1)
            else:
                next_letter = chr(code)
        else:
            if az_min - code > 0:
                next_letter = chr(az_max - (az_min - code) + 1)
            else:
                next_letter = chr(code)

        plaintext += next_letter

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift

