# Алфавіт
alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ.,?!\"*:;%@_"

def substitution_cipher(text, shift):
    encrypted = ''.join(alphabet[(alphabet.index(c) + shift) % len(alphabet)] if c in alphabet else c for c in text)
    return encrypted

# Шифрування
message = "ПОХИБКА"
shift = 5
encrypted_message = substitution_cipher(message, shift)

# Дешифрування
decrypted_message = substitution_cipher(encrypted_message, -shift)

# Виведення результатів
print("Повідомлення:", message)
print("Зашифроване:", encrypted_message)
print("Розшифроване:", decrypted_message)

