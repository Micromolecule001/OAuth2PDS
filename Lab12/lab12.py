import cv2
import numpy as np
from tkinter import Tk, filedialog
import os


def video_to_bit_array(video_path):
    """Конвертація відеофайлу у бітовий масив безпосередньо з файлу."""
    # Читаємо файл безпосередньо у біти
    with open(video_path, 'rb') as file:
        video_bytes = file.read()

    # Конвертуємо байти у біти
    bits = np.unpackbits(np.frombuffer(video_bytes, dtype=np.uint8))
    return bits.tolist()


def hide_video_in_image(image_path, video_path, output_path):
    """Оптимізоване вбудовування відео у зображення."""
    # Завантажуємо біти відео
    bit_array = video_to_bit_array(video_path)
    video_size = len(bit_array)

    # Завантажуємо зображення
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Не вдалося завантажити зображення")

    # Перевіряємо розмір
    available_bits = img.size  # Кількість байтів * 8
    print(f"Розмір відео у бітах: {video_size}")
    print(f"Доступно бітів у зображенні: {available_bits}")

    if video_size > available_bits:
        raise ValueError(f"Недостатньо місця у зображенні: потрібно {video_size} біт, доступно {available_bits} біт")

    # Ефективне вбудовування
    flattened_img = img.ravel()
    for i in range(video_size):
        # Змінюємо тільки найменш значущий біт
        flattened_img[i] = (flattened_img[i] & 0xFE) | bit_array[i]

    # Відновлюємо форму зображення
    modified_img = flattened_img.reshape(img.shape)

    # Зберігаємо результат
    cv2.imwrite(output_path, modified_img)
    print(f"Відео успішно вбудовано у зображення")
    print(f"Використано {video_size} біт із {available_bits} доступних")


def main():
    """Головна функція з покращеною діагностикою."""
    try:
        base_dir = r"C:\Users\Admin\Desktop\Student\ProgramAndDataSecurity\Lab12"

        # Вибір файлів
        image_path = filedialog.askopenfilename(
            title="Оберіть PNG-зображення",
            filetypes=[("PNG зображення", "*.png")],
            initialdir=os.path.join(base_dir, "Original Files")
        )
        if not image_path:
            raise ValueError("Зображення не обрано")

        video_path = filedialog.askopenfilename(
            title="Оберіть відеофайл",
            filetypes=[("Відео", "*.mp4 *.avi")],
            initialdir=os.path.join(base_dir, "Original Files")
        )
        if not video_path:
            raise ValueError("Відео не обрано")

        # Виведення інформації про файли
        print(f"Розмір зображення: {os.path.getsize(image_path)} байт")
        print(f"Розмір відео: {os.path.getsize(video_path)} байт")

        # Формування вихідного шляху
        output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_with_{os.path.splitext(os.path.basename(image_path))[0]}"
        output_path = filedialog.asksaveasfilename(
            title="Зберегти результат",
            initialfile=output_filename,
            defaultextension=".png",
            filetypes=[("PNG зображення", "*.png")],
            initialdir=os.path.join(base_dir, "Changed files")
        )
        if not output_path:
            raise ValueError("Не обрано шлях для збереження")

        # Виконання стеганографії
        hide_video_in_image(image_path, video_path, output_path)
        print(f"Файл збережено за адресою: {output_path}")


    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
