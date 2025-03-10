import time

import time
class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = round(time.time() - self.start_time, 2)
        print(f"Elapsed time: {elapsed_time} seconds")


# Пример использования контекстного менеджера
with Timer() as timer:
    # Ваш блок кода
    time.sleep(3)




