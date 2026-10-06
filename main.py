
import os
import sys
from pathlib import Path

try:
    from pillow_heif import register_heif_opener
    from PIL import Image
except ImportError:
    print("Ошибка: Необходимые библиотеки не установлены.")
    print("Установите их командой:")
    print("pip install pillow-heif pillow")
    sys.exit(1)


def convert_heic_to_jpg(input_folder: str, output_folder: str = None, quality: int = 90):
    """
    Конвертирует все HEIC файлы в папке в формат JPG
    
    Args:
        input_folder: Путь к папке с HEIC файлами
        output_folder: Путь к папке для сохранения JPG (по умолчанию та же папка)
        quality: Качество JPG от 1 до 100 (по умолчанию 90)
    """
    
    # Регистрируем поддержку HEIF/HEIC
    register_heif_opener()
    
    # Создаем объект Path для входной папки
    input_path = Path(input_folder)
    
    # Проверяем существование папки
    if not input_path.exists():
        print(f"Ошибка: Папка '{input_folder}' не найдена!")
        return
    
    if not input_path.is_dir():
        print(f"Ошибка: '{input_folder}' не является папкой!")
        return
    
    # Определяем выходную папку
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    # Находим все HEIC файлы
    heic_files = list(input_path.glob('*.heic')) + list(input_path.glob('*.HEIC'))
    
    if not heic_files:
        print(f"В папке '{input_folder}' не найдено HEIC файлов.")
        return
    
    print(f"Найдено {len(heic_files)} HEIC файл(ов)")
    print(f"Начинаю конвертацию...\\n")
    
    success_count = 0
    error_count = 0
    
    for heic_file in heic_files:
        try:
            # Открываем HEIC файл
            with Image.open(heic_file) as img:
                # Формируем имя выходного файла
                jpg_filename = heic_file.stem + '.jpg'
                jpg_path = output_path / jpg_filename
                
                # Конвертируем и сохраняем
                # Конвертируем в RGB если нужно (для совместимости)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(jpg_path, 'JPEG', quality=quality)
                
                print(f"✓ {heic_file.name} -> {jpg_filename}")
                success_count += 1
                
        except Exception as e:
            print(f"✗ Ошибка при конвертации {heic_file.name}: {str(e)}")
            error_count += 1
    
    print(f"\\n{'='*50}")
    print(f"Конвертация завершена!")
    print(f"Успешно: {success_count}")
    print(f"Ошибок: {error_count}")
    print(f"Результаты сохранены в: {output_path}")


def main():
    """Главная функция с обработкой аргументов командной строки"""
    
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python convert_heic.py <папка_с_heic> [папка_для_jpg] [качество]")
        print("\\nПримеры:")
        print("  python convert_heic.py C:\\Photos")
        print("  python convert_heic.py C:\\Photos C:\\Photos_JPG 95")
        print("\\nЕсли папка для JPG не указана, файлы сохранятся в ту же папку")
        print("Качество по умолчанию: 90 (от 1 до 100)")
        
        # Интерактивный режим
        print("\\n" + "="*50)
        input_folder = input("Введите путь к папке с HEIC файлами: ").strip().strip('"')
        
        if not input_folder:
            print("Путь не указан. Завершаю работу.")
            return
        
        output_folder = input("Введите путь для сохранения JPG (Enter - та же папка): ").strip().strip('"')
        if not output_folder:
            output_folder = None
        
        quality_input = input("Качество JPG (1-100, Enter - 90): ").strip()
        quality = int(quality_input) if quality_input else 90
        
        convert_heic_to_jpg(input_folder, output_folder, quality)
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else None
        quality = int(sys.argv[3]) if len(sys.argv) > 3 else 90
        
        convert_heic_to_jpg(input_folder, output_folder, quality)


if __name__ == "__main__":
    main()
