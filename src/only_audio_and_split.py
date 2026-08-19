#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ffmpeg
import os
from pydub import AudioSegment
import math

def extract_and_split_audio(video_path, output_dir, max_minutes_per_part=30):
    """
    Извлекает аудио из видео и разбивает на части не более указанного количества минут
    """
    try:
        # Проверяем, существует ли видео файл
        if not os.path.exists(video_path):
            print(f"❌ Ошибка: Видео файл не найден: {video_path}")
            return False
        
        # Создаем папку для результатов если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Получаем имя файла без расширения
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # Временный файл для аудио
        temp_audio_path = os.path.join(output_dir, f"{base_name}_temp_audio.mp3")
        
        # ШАГ 1: Извлекаем аудио из видео
        print("=" * 60)
        print("ШАГ 1: ИЗВЛЕЧЕНИЕ АУДИО ИЗ ВИДЕО")
        print("=" * 60)
        print(f"🎬 Видео: {video_path}")
        print(f"🎵 Временное аудио: {temp_audio_path}")
        
        try:
            ffmpeg.input(video_path).output(temp_audio_path).run(overwrite_output=True, quiet=True)
            print(f"✅ Аудио успешно извлечено!")
        except ffmpeg.Error as e:
            print(f"❌ Ошибка FFmpeg: {e.stderr.decode()}")
            return False
        
        # Получаем размер аудио файла
        audio_size = os.path.getsize(temp_audio_path) / (1024 * 1024)
        print(f"📊 Размер аудио: {audio_size:.2f} MB")
        
        # ШАГ 2: Разбиваем аудио на части
        print("\n" + "=" * 60)
        print("ШАГ 2: РАЗБИВКА АУДИО НА ЧАСТИ")
        print("=" * 60)
        
        # Загружаем аудио
        print(f"🎵 Загрузка аудио...")
        audio = AudioSegment.from_file(temp_audio_path)
        
        # Получаем общую длительность в миллисекундах
        total_duration = len(audio)
        total_seconds = total_duration / 1000
        total_minutes = total_seconds / 60
        
        print(f"📊 Общая длительность: {total_minutes:.1f} мин ({total_seconds:.1f} сек)")
        
        # Вычисляем количество частей
        max_duration_ms = max_minutes_per_part * 60 * 1000
        num_parts = math.ceil(total_duration / max_duration_ms)
        
        print(f"✂️ Максимальная длительность части: {max_minutes_per_part} мин")
        print(f"📦 Будет создано частей: {num_parts}")
        print("-" * 60)
        
        # Вычисляем длительность каждой части
        part_duration = total_duration // num_parts
        
        # Разбиваем и сохраняем
        for i in range(num_parts):
            start = i * part_duration
            # Для последней части берем всё до конца
            if i == num_parts - 1:
                end = total_duration
            else:
                end = start + part_duration
            
            # Вырезаем часть
            part = audio[start:end]
            
            # Формируем имя файла
            part_minutes = (end - start) / 1000 / 60
            output_path = os.path.join(output_dir, f"{base_name}_part_{i+1}.mp3")
            
            # Сохраняем
            print(f"✂️ Создание части {i+1}...")
            part.export(output_path, format="mp3")
            
            # Получаем размер файла
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Часть {i+1}: {os.path.basename(output_path)}")
            print(f"   Длительность: {part_minutes:.1f} мин, Размер: {file_size:.2f} MB")
            print("-" * 60)
        
        # Удаляем временный аудио файл
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"🗑️ Временный файл удален: {temp_audio_path}")
        
        print(f"\n✨ ГОТОВО! {num_parts} файлов сохранено в: {output_dir}")
        print(f"📁 Путь: {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    # ============================================
    # ЗДЕСЬ ПРОПИСЫВАЕШЬ СВОИ ПУТИ
    # ============================================
    
    # Путь к исходному видео файлу
    VIDEO_PATH = "/home/romand/Videos/Записи экрана/1.mp4"
    
    # Папка для сохранения разбитых аудио файлов
    OUTPUT_DIR = "/home/romand/Videos/split_audio"
    
    # Максимальная длительность одной части в минутах
    MAX_MINUTES_PER_PART = 30  # можно изменить на любое значение
    
    # ============================================
    
    print("=" * 60)
    print("ИЗВЛЕЧЕНИЕ И РАЗБИВКА АУДИО ИЗ ВИДЕО")
    print("=" * 60)
    print(f"Видео: {VIDEO_PATH}")
    print(f"Папка: {OUTPUT_DIR}")
    print(f"Макс. часть: {MAX_MINUTES_PER_PART} минут")
    print("=" * 60)
    print()
    
    extract_and_split_audio(VIDEO_PATH, OUTPUT_DIR, MAX_MINUTES_PER_PART)
