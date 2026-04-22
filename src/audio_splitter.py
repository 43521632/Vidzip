#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydub import AudioSegment
import os

def split_audio_into_parts(audio_path, output_dir, num_parts=3):
    """
    Разбивает аудио на указанное количество равных частей
    """
    try:
        # Проверяем, существует ли аудио файл
        if not os.path.exists(audio_path):
            print(f"❌ Ошибка: Аудио файл не найден: {audio_path}")
            return False
        
        # Создаем папку для результатов если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Загружаем аудио
        print(f"🎵 Загрузка аудио: {audio_path}")
        audio = AudioSegment.from_file(audio_path)
        
        # Получаем общую длительность в миллисекундах
        total_duration = len(audio)
        
        # Вычисляем длительность каждой части
        part_duration = total_duration // num_parts
        
        # Получаем имя файла без расширения
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        print(f"📊 Общая длительность: {total_duration/1000:.1f} сек")
        print(f"✂️ Разбиваем на {num_parts} частей по {part_duration/1000:.1f} сек каждая")
        print("-" * 40)
        
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
            output_path = os.path.join(output_dir, f"{base_name}_part_{i+1}.mp3")
            
            # Сохраняем
            part.export(output_path, format="mp3")
            
            # Получаем размер файла
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Часть {i+1}: {output_path}")
            print(f"   Длительность: {(end-start)/1000:.1f} сек, Размер: {file_size:.2f} MB")
        
        print("-" * 40)
        print(f"✨ Готово! {num_parts} файлов сохранено в: {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    # ============================================
    # ЗДЕСЬ ПРОПИСЫВАЕШЬ СВОИ ПУТИ
    # ============================================
    
    # Путь к исходному аудио файлу (которое ты извлек из видео)
    AUDIO_PATH = "/home/romand/Видео/1.mp3"
    
    # Папка для сохранения разбитых файлов
    OUTPUT_DIR = "/home/romand/Видео/split_audio"
    
    # Количество частей (можно изменить на любое число)
    PARTS_COUNT = 3
    
    # ============================================
    
    print("=" * 50)
    print("РАЗБИВКА АУДИО НА ЧАСТИ")
    print("=" * 50)
    
    split_audio_into_parts(AUDIO_PATH, OUTPUT_DIR, PARTS_COUNT)
