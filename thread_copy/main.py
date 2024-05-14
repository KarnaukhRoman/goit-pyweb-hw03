import shutil
from threading import Thread
import argparse
from pathlib import Path
import logging
import time


def create_list_dir(src_dir: Path) -> list:
    """
    Повертає список всіх директорій у вказаній цільовій директорії,
    включаючи саму цільову директорію.
    """
    all_directories = []
    all_directories.append(src_dir)
    for el in src_dir.iterdir():
        if el.is_dir():
            all_directories.extend(create_list_dir(el))
    return all_directories


def copy_file(src_dir: Path, dest_dir: Path):
    """
    Копіює файл з вихідної директорії до піддиректорії з назвою, що відповідає розширенню файлу,
    у вказаній цільовій директорії.
    """
    for el in src_dir.iterdir():
        if el.is_file():
            ext = el.suffix[1::]
            dst_subdir = dest_dir.joinpath(ext)
            try:
                dst_subdir.mkdir(parents=True, exist_ok=True)
                logging.debug(f'Start copy file in thread: {el.name}')
                shutil.copy2(el, dst_subdir)
            except OSError as err:
                logging.debug(f'Error {err} copy file in thread: {el.name}')


def create_thread(list_dir: list, dest_dir: Path):
    """
     Створюємо потоки для копіювання файлів до кожної директорії
    """
    threads = []
    for directory in list_dir:
        thread = Thread(target=copy_file, args=(directory, dest_dir))
        thread.start()
        threads.append(thread)
        print(f'thread = {thread}')

    for thread in threads:
        thread.join()


def main():
    # Парсер аргументів командного рядка
    parser = argparse.ArgumentParser(description='Program for copying and sorting files')
    parser.add_argument('src_dir', help='Шлях до вихідної директорії')
    parser.add_argument('dst_dir', nargs='?', default='dist', help='Шлях до цільової директорії')
    args = parser.parse_args()

    src_dir = Path(args.src_dir)
    dst_dir = Path(args.dst_dir)

    # Створюємо список усіх директорій
    directories = create_list_dir(src_dir)

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    start_time = time.time()
    create_thread(directories, dst_dir)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
