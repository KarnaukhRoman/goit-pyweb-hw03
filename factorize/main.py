from multiprocessing import Pool, cpu_count
import time


def factorize(*args: list) -> list:
    factors = []
    for num in args:
        num_factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                num_factors.append(i)
        factors.append(num_factors)
    return factors


def factor(*args: list) -> list:
    num_factors = []
    for num in args:
        for i in range(1, num + 1):
            if num % i == 0:
                num_factors.append(i)
    return num_factors


def factorize_parallel(*args):
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(factor, args)
        pool.close()
        pool.join()
        return results


if __name__ == '__main__':
    nums = [12810654,
            255651060,
            99999106,
            10651060,
            ]
    start_time = time.time()
    # Start factorize single
    factorize(*nums)
    print(f'end of factorize single   {time.time() - start_time}')
    start_time = time.time()
    # Start factorize parallel
    factorize_parallel(*nums)
    print(f'end of factorize parallel {time.time() - start_time}')
