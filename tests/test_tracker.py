import unittest
import json
import os
from main import TrainingPlanner

# Путь к файлу данных, используемому в тестах
TEST_DATA_FILE = "data/test_trainings.json"

class TestTrainingPlanner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем экземпляр класса для тестирования методов."""
        # Создаем временное окно Tkinter, чтобы можно было тестировать методы, зависящие от self.root
        cls.root = tk.Tk()
        cls.root.withdraw()  # Скрываем главное окно, чтобы оно не мешало при запуске тестов
        cls.app = TrainingPlanner(cls.root)
        cls.app.DATA_FILE = TEST_DATA_FILE  # Перенаправляем сохранение в тестовый файл

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовый файл данных после всех тестов."""
        cls.root.destroy()
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)

    def setUp(self):
        """Перед каждым тестом очищаем файл данных."""
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)
        self.app.load_data()  # Загружаем (создаем пустой) список тренировок

    def test_01_add_valid_training(self):
        """Тест: добавление тренировки с валидными данными."""
        self.app.date_entry.insert(0, "2026-04-30")
        self.app.type_entry.insert(0, "Бег")
        self.app.duration_entry.insert(0, "45")
        
        self.app.add_training()
        
        # Проверяем, что данные сохранились в файл
        self.assertTrue(os.path.exists(TEST_DATA_FILE))
        
        with open(TEST_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], "2026-04-30")
        self.assertEqual(data[0]['type'], "Бег")
        self.assertEqual(data[0]['duration'], 45.0)

    def test_02_add_invalid_date_format(self):
        """Тест: добавление тренировки с некорректным форматом даты."""
        self.app.date_entry.insert(0, "30-04-2026") # Неверный формат
        self.app.type_entry.insert(0, "Плавание")
        self.app.duration_entry.insert(0, "60")
        
        # Ожидаем, что метод не добавит запись и покажет ошибку (в реальном приложении это был бы messagebox)
        # Здесь мы проверяем, что данные не сохранились в файл
        self.app.add_training()
        
        self.assertFalse(os.path.exists(TEST_DATA_FILE) or os.path.getsize(TEST_DATA_FILE) == 0)

    def test_03_add_negative_duration(self):
        """Тест: добавление тренировки с отрицательной длительностью."""
        self.app.date_entry.insert(0, "2026-05-01")
        self.app.type_entry.insert(0, "Йога")
        self.app.duration_entry.insert(0, "-15")
        
        self.app.add_training()
        
        # Проверяем, что запись не добавилась
        self.assertFalse(os.path.exists(TEST_DATA_FILE) or os.path.getsize(TEST_DATA_FILE) == 0)

    def test_04_filter_by_type(self):
        """Тест: фильтрация тренировок по типу."""
        # Сначала добавляем несколько тренировок для теста фильтрации
        test_data = [
            {"date": "2026-04-29", "type": "Силовая", "duration": 60},
            {"date": "2026-04-30", "type": "Кардио", "duration": 30},
            {"date": "2026-05-01", "type": "Силовая", "duration": 45}
        ]
        
        with open(TEST_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)
            
        self.app.load_data()
        
        # Устанавливаем фильтр и применяем его
        self.app.filter_type.delete(0, tk.END)
        self.app.filter_type.insert(0, "Силовая")
        
        # Очищаем таблицу перед применением фильтра (имитация поведения GUI)
        for i in self.app.tree.get_children():
            self.app.tree.delete(i)
            
        self.app.apply_filter()
        
        # Получаем видимые строки из таблицы (в Treeview они имеют идентификаторы)
        children = self.app.tree.get_children()
        
        # Проверяем количество и содержимое отфильтрованных строк
        self.assertEqual(len(children), 2)
        
        values_sila_1 = self.app.tree.item(children[0])['values']
        values_sila_2 = self.app.tree.item(children[1])['values']
        
        self.assertIn("Силовая", values_sila_1)
        self.assertIn("Силовая", values_sila_2)


if __name__ == '__main__':
    import tkinter as tk # Импортируем здесь, чтобы избежать конфликтов при запуске тестов напрямую
    unittest.main()
