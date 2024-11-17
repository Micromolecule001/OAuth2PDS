# Таблиця Віженера
alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"

def vigenere_encrypt(text, key):
    encrypted = ''
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    for t, k in zip(text, key):
        encrypted += alphabet[(alphabet.index(t) + alphabet.index(k)) % len(alphabet)]
    return encrypted

def vigenere_decrypt(ciphertext, key):
    decrypted = ''
    key = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    for c, k in zip(ciphertext, key):
        decrypted += alphabet[(alphabet.index(c) - alphabet.index(k)) % len(alphabet)]
    return decrypted

# Шифрування
message = "ПРИКЛАД"
key = "КЛЮЧ"
encrypted_message = vigenere_encrypt(message, key)

# Дешифрування
decrypted_message = vigenere_decrypt(encrypted_message, key)

# Виведення результатів
print("Повідомлення:", message)
print("Ключ:", key)
print("Зашифроване:", encrypted_message)
print("Розшифроване:", decrypted_message)

