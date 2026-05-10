import os
import csv

class DataProcessor:
    def __setattr__(self, name, value):  # Пункт 4
        self.__dict__[name] = value

    def __getitem__(self, index):  # Пункт 5
        if hasattr(self, 'data'):
            return self.data[index]
        raise IndexError("No data available")

    def __repr__(self):  # Пункт 2
        if hasattr(self, 'data'):
            return f"DataProcessor(data={len(self.data) if self.data else 0} records)"
        return "DataProcessor(no data)"

    def __iter__(self):  # Пункт 1
        if hasattr(self, 'data'):
            return iter(self.data)
        return iter([])

    @staticmethod  # Пункт 6
    def process_temperature(temp):
        return temp

    def temperature_generator(self):  # Пункт 7
        if hasattr(self, 'data'):
            for row in self.data:
                yield row['показание температуры']


# Класс-наследник (Пункт 3)
class ExtendedDataProcessor(DataProcessor):
    pass


# Подсчет файлов
def count_files(directory="papka"):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])


print(f"количество файлов: {count_files()}")


# Работа с CSV
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['№'] = int(row['№'])
            row['показание температуры'] = float(row['показание температуры'])
            data.append(row)
    return data


def save_csv(data, filename="data.csv"):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['№', 'широта', 'долгота', 'показание температуры', 'дата и время'])
        writer.writeheader()
        writer.writerows(data)


data = read_csv("papka\data.csv")

# Добавляем новую запись
new_record = {
    '№': len(data) + 1,
    'широта': 57.153,
    'долгота': 65.534,
    'показание температуры': 26.3,
    'дата и время': "2024-03-16 09:15:00"
}

# Сортировка по строковому полю
data = sorted(data, key=lambda x: x['дата и время'])

# Сортировка по числовому полю
data = sorted(data, key=lambda x: x['показание температуры'])

# Фильтрация (температура > 20)
data = [row for row in data if row['показание температуры'] > 20]

data.append(new_record)

# Использование класса для демонстрации пунктов
processor = ExtendedDataProcessor()  # Пункт 3
processor.data = data  # Через __setattr__ (Пункт 4)

save_csv(data, "papka\data_updated.csv")

# Демонстрация пунктов:
print(f"repr: {repr(processor)}")  # Пункт 2
print(f"Доступ по индексу [0]: {processor[0]}")  # Пункт 5
print("Итератор:")  # Пункт 1
for item in processor:
    print(item)
print(f"Статический метод: {DataProcessor.process_temperature(25.5)}")  # Пункт 6
print("Генератор температур:")  # Пункт 7
for temp in processor.temperature_generator():
    print(temp)