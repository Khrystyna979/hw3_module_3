from pathlib import Path
from threading import Thread
import logging
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser(description="Сортування файлів за розширеннями з використанням багатопотоковості.")
parser.add_argument("source", help="Шлях до вихідної директорії.")
parser.add_argument('output', help="Шлях до цільової директорії (за замовчуванням: 'dist').")

args = parser.parse_args()

source_path = Path(args.source)
output_path = Path(args.output)

def sort_dir(source_path: Path):

    current_level_threads = []

    for el in source_path.iterdir():
        if el.is_dir():
            inner_process = Thread(target=sort_dir, args=(el,))
            inner_process.start()
            current_level_threads.append(inner_process)
        else:
            copy_process = Thread(target=copy_file, args=(el,))
            copy_process.start()
            current_level_threads.append(copy_process)

    for t in current_level_threads:
        t.join()
    
def copy_file(file: Path):

    suffix = file.suffix.lower()
    new_path = output_path / suffix[1:]
    new_path.mkdir(exist_ok=True, parents=True)
    final_path = new_path / file.name
    copyfile(file, final_path)
    logging.debug(f'Додано файл {file.name} до папки {new_path.name}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    if not source_path.is_dir():
        logging.error(f'Вихідна папка не знайдена: {source_path}')
    else:
        threads = []
        thread = Thread(target=sort_dir, args=(source_path,))
        thread.start()
        threads.append(thread)

        [el.join() for el in threads]

        logging.debug('Сортування завершено')


