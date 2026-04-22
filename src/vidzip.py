import subprocess
import os
import sys

def compress_webm(input_path: str, output_path: str = None, 
                  crf: int = 30, speed: int = 4, 
                  audio_bitrate: str = "64k", scale: str = None, fps: int = None):
    """
    Сжимает .webm файл с помощью ffmpeg (кодек VP9 + Opus).
    
    :param input_path: Путь к исходному файлу
    :param output_path: Путь к результату (по умолчанию: имя_compressed.webm)
    :param crf: Качество видео (15-60). Чем МЕНЬШЕ, тем лучше качество, но БОЛЬШЕ размер.
                Рекомендуемо: 25-35 для баланса.
    :param speed: Скорость кодирования CPU (0-8). 0 = медленнее/качественнее, 8 = быстрее/хуже.
                  Рекомендуемо: 3-5
    :param audio_bitrate: Битрейт аудио (например, "48k", "64k", "96k")
    :param scale: Масштабирование, например "1280:-2" (высота 1280, ширина кратная 2)
    :param fps: Ограничение кадров/сек, например 30
    """
    if not os.path.exists(input_path):
        print(f"❌ Ошибка: Файл '{input_path}' не найден.")
        sys.exit(1)

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_compressed.webm"

    # Проверка ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print("❌ FFmpeg не найден в PATH. Установите его перед запуском скрипта.")
        print("🔗 Инструкция: https://ffmpeg.org/download.html")
        sys.exit(1)

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libvpx-vp9",
        "-crf", str(crf),
        "-b:v", "0",          # Обязательно для работы CRF в VP9
        "-cpu-used", str(speed),
        "-row-mt", "1",       # Включение многопоточности (ускоряет на современных CPU)
        "-c:a", "libopus",
        "-b:a", audio_bitrate,
        "-y",                 # Перезаписывать выходной файл без вопросов
    ]

    if scale:
        cmd.extend(["-vf", f"scale={scale}"])
    if fps:
        cmd.extend(["-r", str(fps)])

    cmd.append(output_path)

    orig_size = os.path.getsize(input_path) / (1024**2)
    print(f"🎬 Исходный файл: {input_path} ({orig_size:.1f} МБ)")
    print(f"📦 Выходной файл: {output_path}")
    print(f"⚙️  Параметры: CRF={crf} | CPU Speed={speed} | Аудио={audio_bitrate} | Scale={scale or 'нет'} | FPS={fps or 'оригинал'}")
    print("💡 CRF 30 обычно даёт ~3-4 Мбит/с. Для 15 мин это ~300-450 МБ.")
    print("-" * 60)

    try:
        # Запускаем ffmpeg и передаём вывод в консоль (чтобы видеть прогресс)
        subprocess.run(cmd, check=True)
        
        comp_size = os.path.getsize(output_path) / (1024**2)
        saved_pct = (1 - comp_size / orig_size) * 100
        print("-" * 60)
        print(f"✅ Готово! Размер: {orig_size:.1f} МБ → {comp_size:.1f} МБ (сжато на {saved_pct:.1f}%)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка кодирования: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # === ПРИМЕР ИСПОЛЬЗОВАНИЯ ===
    # Укажите путь к вашему файлу
    INPUT_FILE = "/home/romand/Видео/Записи экрана/1.mkv"  # <-- ЗАМЕНИТЕ НА СВОЙ ФАЙЛ
    
    compress_webm(
        input_path=INPUT_FILE,
        crf=32,              # Качество (попробуйте 28-35)
        speed=4,             # Баланс скорость/качество
        audio_bitrate="48k", # Достаточно для речи, 64k-96k для музыки/шумов
        # scale="1280:-2",   # Раскомментируйте для уменьшения разрешения
        # fps=30             # Раскомментируйте для ограничения FPS
    )
