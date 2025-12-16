from time import time
from multiprocessing import cpu_count, Pool
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize_worker(number):

    new_numbers = []

    for i in range(1, number + 1):
        if number % i == 0:
            new_numbers.append(i)

    return new_numbers

def factorize_sync(*numbers):

    numb_to_fact = list(numbers)
    start_time_sync = time()
    result = [factorize_worker(i) for i in numb_to_fact]

    logging.debug(f'Час виконання синхронної версії: {round(time()-start_time_sync, 6)} сек')
    return result

def factorize_parallel(*numbers):
    numb_to_factorize = list(numbers)
    start_time = time()

    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_worker, numb_to_factorize)

    end_time = time()
    logging.debug(f'Кількість ядер: {cpu_count()}')
    logging.debug(f'Час виконання паралельної версії: {round(end_time - start_time, 6)} сек')

    return results

if __name__ == '__main__':
    numbers = (128, 255, 99999, 10651060)
    
    logging.debug('\nСинхронне виконання:')
    a_sync, b_sync, c_sync, d_sync = factorize_sync(*numbers)

    logging.debug('\nПаралельне виконання:')
    a_par, b_par, c_par, d_par = factorize_parallel(*numbers) 

    logging.debug('\nТестування результатів для паралельної версії:')
    assert a_par == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b_par == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c_par == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d_par == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    logging.debug('Тести пройшли успішно')

    logging.debug(f'\nДільники {numbers[3]} - {d_par}')
