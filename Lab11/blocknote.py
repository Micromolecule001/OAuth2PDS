import random

# Перетворення символу в двійковий код
def text_to_binary(text):
    alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ.,?!\"*:;%@_"
    binary_text = ''.join(format(alphabet.index(c), '06b') for c in text.upper())
    return binary_text

# Генерація випадкового ключа
def generate_key(length):
    return ''.join(random.choice('01') for _ in range(length))

# XOR двох бінарних строк
def xor_strings(binary_text, binary_key):
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(binary_text, binary_key))

# Шифрування
message = "ХЛІБ"
binary_message = text_to_binary(message)
key = generate_key(len(binary_message))
ciphertext = xor_strings(binary_message, key)

# Виведення результатів
print("Повідомлення:", message)
print("Двійкове повідомлення:", binary_message)
print("Ключ:", key)
print("Криптотекст:", ciphertext)

