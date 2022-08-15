from pathlib import Path
import shutil
from time import time

import file_parser as parser
from normalize import normalize
import asyncio


async def handle_files(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


async def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
                      normalize(filename.name.replace(filename.suffix, ''))
    #  создаем папку для архива с именем файла

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


async def sort_files(folder: Path):
    list_tasks = []
    for k, v in parser.REGISTER_EXTENSIONS.items():
        for file in v:
            if k == 'JPEG' or k == 'JPG' or k == 'SVG' or k == 'PNG':
                list_tasks.append(asyncio.create_task(handle_files(file, folder / 'images' / k)))
            elif k == 'MP3' or k == 'OGG' or k == 'WAV' or k == 'AMR':
                list_tasks.append(asyncio.create_task(handle_files(file, folder / 'audio' / k)))
            elif k == 'AVI' or k == 'MP4' or k == 'MKV' or k == 'MOV':
                list_tasks.append(asyncio.create_task(handle_files(file, folder / 'video' / k)))
            elif k == 'DOC' or k == 'DOCX' or k == 'TXT' or k == 'PDF' or k == 'PPTX' or k == 'XLSX':
                list_tasks.append(asyncio.create_task(handle_files(file, folder / 'documents' / k)))
            elif k == 'ZIP' or k == 'GZ' or k == 'TAR':
                list_tasks.append(asyncio.create_task(handle_archive(file, folder / 'archives' / k)))
            else:
                list_tasks.append(asyncio.create_task(handle_files(file, folder / 'other' / 'OTHERS')))
    await asyncio.gather(*list_tasks)

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)
    return


async def main(folder: Path):
    parser.scan(folder)
    await sort_files(folder)


if __name__ == '__main__':
    user_input = input(">>>")
    start = time()
    if user_input:
        folder_for_scan = Path(user_input).resolve()
        print(f'Start in folder {folder_for_scan}')
        asyncio.run(main(folder_for_scan))
        print(time() - start)
