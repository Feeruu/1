import matplotlib.pyplot as plt
import  numpy as np

# Пример данных опроса
data = {
    "satisfaction": ["Очень доволен", "Доволен", "Нейтрален", "Недоволен", "Очень недоволен"],
    "satisfaction_counts": [50, 100, 70, 30, 20],
    "factors": ["Зарплата", "Условия труда", "Коллектив", "Гибкий график", "Другие"],
    "factors_counts": [150, 130, 120, 100, 60],
    "job_satisfaction_scale": [1, 2, 3, 4, 5],
    "job_satisfaction_counts": [10, 20, 30, 80, 60],
    "hours_worked": ["0-10", "11-20", "21-30", "31-40", "41+"],
    "hours_counts": [5, 15, 40, 100, 30],
    "ranking": ["Зарплата", "Гибкий график", "Возможности для развития", "Коллектив", "Условия труда"],
    "ranking_avg_positions": [1.2, 2.5, 2.8, 3.3, 4.1]
}

# Построение графика удовлетворенности работой
plt.figure(figsize=(10, 6))
plt.bar(data["satisfaction"], data["satisfaction_counts"], color='skyblue')
plt.xlabel("Оценка удовлетворенности")
plt.ylabel("Количество ответов")
plt.title("Удовлетворенность работой компании")
plt.show()

# Построение графика важности факторов
plt.figure(figsize=(10, 6))
plt.bar(data["factors"], data["factors_counts"], color='lightgreen')
plt.xlabel("Факторы")
plt.ylabel("Количество ответов")
plt.title("Важные факторы для комфорта на рабочем месте")
plt.show()

# Построение графика по шкале Лайкерта
plt.figure(figsize=(10, 6))
plt.bar(data["job_satisfaction_scale"], data["job_satisfaction_counts"], color='lightcoral')
plt.xlabel("Оценка по шкале Лайкерта")
plt.ylabel("Количество ответов")
plt.title("Удовлетворенность работой по шкале Лайкерта")
plt.show()

# Построение графика количества отработанных часов
plt.figure(figsize=(10, 6))
plt.bar(data["hours_worked"], data["hours_counts"], color='lightsalmon')
plt.xlabel("Количество отработанных часов в неделю")
plt.ylabel("Количество ответов")
plt.title("Количество отработанных часов в неделю")
plt.show()

# Построение графика ранжирования факторов
plt.figure(figsize=(10, 6))
plt.bar(data["ranking"], data["ranking_avg_positions"], color='lightblue')
plt.xlabel("Факторы")
plt.ylabel("Средняя позиция")
plt.title("Ранжирование факторов по важности")
plt.gca().invert_yaxis()  # Инвертируем ось Y для отображения 1-го места наверху
plt.show()
