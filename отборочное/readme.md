# Устанока зависимостей:
- Перейдите в директорию проекта
- Выполните команду `pip install -r requirements.txt`

# Организация ввода:
 
- `H0` (м) - высота сброса (не более `1400м`)
- `V0` (м/с) - начальная скорость (не более `250 м/с`) 
- `m`  (кг) - масса груза
- Аэродинамическая сила и направление ветра считываются из csv файлов (`Wind.csv, F.csv`)

## Координаты точек приземления:
- Координаты точек приземления вводятся в одну строку через пробел (`x y z`)

## Выходные данные:
На выходе происходит отрисовка траектории сброса.
В консоли будет напечатана следующая информация: 
- Координаты сброса через пробел: `x y z`
- Направление вектора скорости (угол `alpha`)
- Создаются два текстовых файла (`coordinates.txt`, `V.txt`)

## Описание вывода:

### `coordinates.txt`:
- Зависимость координат от времени.

### `V.txt`:
- Зависимость скорости от времени.


# Запуск:
- Перейдите в директорию проекта
- Выполните команду `python ProjectileFlightSimulation.py`
