from pathlib import Path
import shutil

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


async def main(folder: Path):
    list_tasks = []
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        t1 = asyncio.create_task(handle_files(file, folder / 'images' / 'JPEG'))
        list_tasks.append(t1)
    for file in parser.JPG_IMAGES:
        t2 = asyncio.create_task(handle_files(file, folder / 'images' / 'JPG'))
        list_tasks.append(t2)
    for file in parser.PNG_IMAGES:
        t3 = asyncio.create_task(handle_files(file, folder / 'images' / 'PNG'))
        list_tasks.append(t3)
    for file in parser.SVG_IMAGES:
        t4 = asyncio.create_task(handle_files(file, folder / 'images' / 'SVG'))
        list_tasks.append(t4)
    for file in parser.MP3_AUDIO:
        t5 = asyncio.create_task(handle_files(file, folder / 'audio' / 'MP3'))
        list_tasks.append(t5)
    for file in parser.OGG_AUDIO:
        t6 = asyncio.create_task(handle_files(file, folder / 'audio' / 'OGG'))
        list_tasks.append(t6)
    for file in parser.WAV_AUDIO:
        t7 = asyncio.create_task(handle_files(file, folder / 'audio' / 'WAV'))
        list_tasks.append(t7)
    for file in parser.AMR_AUDIO:
        t8 = asyncio.create_task(handle_files(file, folder / 'audio' / 'AMR'))
        list_tasks.append(t8)
    for file in parser.AVI_VIDEO:
        t9 = asyncio.create_task(handle_files(file, folder / 'video' / 'AVI'))
        list_tasks.append(t9)
    for file in parser.MP4_VIDEO:
        t10 = asyncio.create_task(handle_files(file, folder / 'video' / 'MP4'))
        list_tasks.append(t10)
    for file in parser.MOV_VIDEO:
        t11 = asyncio.create_task(handle_files(file, folder / 'video' / 'MOV'))
        list_tasks.append(t11)
    for file in parser.MKV_VIDEO:
        t12 = asyncio.create_task(handle_files(file, folder / 'video' / 'MKV'))
        list_tasks.append(t12)
    for file in parser.DOC_DOCUMENTS:
        t13 = asyncio.create_task(handle_files(file, folder / 'documents' / 'DOC'))
        list_tasks.append(t13)
    for file in parser.DOCX_DOCUMENTS:
        t14 = asyncio.create_task(handle_files(file, folder / 'documents' / 'DOCX'))
        list_tasks.append(t14)
    for file in parser.TXT_DOCUMENTS:
        t15 = asyncio.create_task(handle_files(file, folder / 'documents' / 'TXT'))
        list_tasks.append(t15)
    for file in parser.PDF_DOCUMENTS:
        t16 = asyncio.create_task(handle_files(file, folder / 'documents' / 'PDF'))
        list_tasks.append(t16)
    for file in parser.XLSX_DOCUMENTS:
        t17 = asyncio.create_task(handle_files(file, folder / 'documents' / 'XLSX'))
        list_tasks.append(t17)
    for file in parser.PPTX_DOCUMENTS:
        t18 = asyncio.create_task(handle_files(file, folder / 'documents' / 'PPTX'))
        list_tasks.append(t18)

    for file in parser.OTHER:
        t19 = asyncio.create_task(handle_files(file, folder / 'other' / 'OTHER'))
        list_tasks.append(t19)
    for file in parser.ARCHIVES:
        t20 = asyncio.create_task(handle_archive(file, folder / 'archives' / 'ARCHIVES'))
        list_tasks.append(t20)

    await asyncio.gather(*list_tasks)

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)
    return

if __name__ == '__main__':
    user_input = input(">>>")
    if user_input:
        folder_for_scan = Path(user_input).resolve()
        print(f'Start in folder {folder_for_scan}')
        asyncio.run(main(folder_for_scan))
