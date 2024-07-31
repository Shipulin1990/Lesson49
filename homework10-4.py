from threading import Thread
import time
from queue import Queue


class Table:

    def __init__(self, number):
        self.number = int(number)
        self.is_busy = False


class Cafe:

    def __init__(self, tables):
        self.tables = tables
        self.queue = Queue()
        self.caller_thr = []

    def customer_arrival(self):
        for i in range(1, 21):
            time.sleep(1)
            print(f"Посетитель номер {i} прибыл.")
            caller = Thread(target=self.serve_customer, args=(i,))
            self.caller_thr.append(caller)
            caller.start()
        for caller in self.caller_thr:
            caller.join()

    def serve_customer(self, caller):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {caller} сел за стол {table.number}.(начало обслуживания)')
                time.sleep(5)
                table.is_busy = False
                print(f'Посетитель номер {caller} покушал и ушёл.(конец обслуживания)')
                table.is_busy = False
                if not self.queue.empty():
                    caller = Thread(target=self.serve_customer, args=(self.queue.get(),))
                    self.caller_thr.append(caller)
                    caller.start()
                exit()
        print(f'{caller} ожидает свободный стол')
        self.queue.put(caller)


class Customer(Thread):
    def __init__(self, number, table):
        super().__init__()
        self.number = number
        self.cafe = table

    def run(self):
        self.cafe.serve_customer(self)


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
