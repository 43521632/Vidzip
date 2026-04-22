#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ffmpeg
import os

def extract_audio_ffmpeg(video_path, audio_path):
    """
    Извлечение аудио из видео с помощью ffmpeg-python
    """
    try:
        # Проверяем, существует ли видео файл
        if not os.path.exists(video_path):
            print(f"❌ Ошибка: Видео файл не найден: {video_path}")
            return False
        
        # Проверяем, существует ли папка для сохранения аудио
        audio_dir = os.path.dirname(audio_path)
        if audio_dir and not os.path.exists(audio_dir):
            print(f"📁 Создаю папку: {audio_dir}")
            os.makedirs(audio_dir)
        
        # Извлекаем аудио
        print(f"🎬 Извлечение аудио из: {video_path}")
        print(f"🎵 Сохранение в: {audio_path}")
        
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)
        
        # Получаем размер файла
        file_size = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"✅ Аудио успешно сохранено! Размер: {file_size:.2f} MB")
        return True
        
    except ffmpeg.Error as e:
        print(f"❌ Ошибка FFmpeg: {e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при извлечении аудио: {e}")
        return False

if __name__ == "__main__":
    # ============================================
    # ЗДЕСЬ ПРОПИСЫВАЕШЬ СВОИ ПУТИ
    # ============================================
    
    # Путь к исходному видео файлу
    VIDEO_PATH = "/home/romand/Видео/ЗаписиЭкранаOBS/1.mp4"
    
    # Путь для сохранения аудио файла
    AUDIO_PATH = "/home/romand/Видео/my_audio.mp3"
    
    # ============================================
    # ЗАПУСК ИЗВЛЕЧЕНИЯ
    # ============================================
    
    print("=" * 60)
    print("ИЗВЛЕЧЕНИЕ АУДИО ИЗ ВИДЕО")
    print("=" * 60)
    print(f"Видео: {VIDEO_PATH}")
    print(f"Аудио: {AUDIO_PATH}")
    print("=" * 60)
    
    extract_audio_ffmpeg(VIDEO_PATH, AUDIO_PATH)
