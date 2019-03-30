import math
import xlwt
import numpy as np
from csv import reader
def get_F():
    """
    Получить аэродинамическую силу
    из файла F.csv

    возвращается массивы F, V
    """
    reader_F = reader(open("F.csv", "r"))
    F_sequence = []
    v_sequence = []
    trigger = 1
    for line in reader_F:
        if trigger:
            trigger = 0
        else:
            v_sequence.append(float(line[0]))
            F_sequence.append(float(line[1]))
    return F_sequence, v_sequence


def get_Wind():
    """
    Получить аэродинамическую силу
    из файла Wind.csv

    возвращается массивы Wx, Wy, H
    """
    reader_wind = reader(open("Wind.csv", "r"))
    h_sequence = []
    v_wind_sequence_x = []
    v_wind_sequence_y = []

    trigger = 1
    for line in reader_wind:
        if trigger:
            trigger = 0
        else:
            h_sequence.append(float(line[0]))
            v_wind_sequence_x.append(float(line[1]))
            v_wind_sequence_y.append(float(line[2]))
    return v_wind_sequence_x, v_wind_sequence_y, h_sequence


def get_mass_k_wind(w, h):
    """
    получить массив коэффициентов
    для линейной аппроксимации проекций W
    """
    n = len(h) - 1
    k = [0] * n
    for i in range(n):
        k[i] = (w[i+1] - w[i]) / (h[i + 1] - h[i])
    return k


def get_Wx(H):
    """
    получить Wx на высоте H
    """
    n = len(h) - 1
    for i in range(n):
        if h[i] <= H <= h[i+1]:
            return k_wind_x[i]


def get_Wy(H):
    """
    получить Wy на высоте H
    """
    n = len(h) - 1
    for i in range(n):
        if h[i] <= H <= h[i+1]:
            return k_wind_y[i]


def get_k_F(F, V):
    """
    получить приближённый коэффициент, зависимости
    F = -k *| V| * V
    """
    summ = 0
    count = 0
    for f, v in zip(F, V):
        if v:
            summ += f / (v * v)
            count += 1
    return summ / count


def get_v_xy(v_0: float, k: float, m: float, delta_t: float) -> float:
    '''
    получить компоненту скорости на проекции на X или Y
    '''
    return v_0 - k / m * v_0 * delta_t


def get_vz(v_0z: float, k: float, m: float, delta_t: float) -> float:
    """
    получить компоненту скорости на проекцию Z
    """
    return v_0z - (g + k / m * v_0z) * delta_t


def get_coor_p_pr(r_0_pr, v_0r_pr, delta_t):
    """
    получить следущую координату 
    """
    return r_0_pr + v_0r_pr * delta_t


def projectile(k, x_0, y_0, z_0, z_target):
    """
    моделирование движения материальной точки
    в поле тяжести с учётом аэродинамической силы
    и направления ветров на разных высотах

    k - коэффициент сопративления
    x_0, y_0, z_0 - точка запуска материальной точки 

    выходные данные
    x, y, z - три массива зависимости координаты от времени
    vx, vy, vz - три массива зависимости скорости от времени
    t - соответствующее время
    """
    vx = [V0 * math.cos(a)]
    vy = [V0 * math.sin(a)]
    vz = [0]

    x = [x_0]
    y = [y_0]
    z = [z_0]

    # vz = [20]
    # z[0] = H

    j = 0
    t = [0]
    while z[j] > z_target:
        vx[j] += get_Wx(z[j])
        vy[j] += get_Wy(z[j])

        vx.append(get_v_xy(vx[j], k, m, delta_t))

        vy.append(get_v_xy(vy[j], k, m, delta_t))

        vz.append(get_vz(vz[j], k, m, delta_t))

        x.append(get_coor_p_pr(x[j], vx[j], delta_t))

        y.append(get_coor_p_pr(y[j], vy[j], delta_t))

        z.append(get_coor_p_pr(z[j], vz[j], delta_t))

        j += 1
        t.append(delta_t * j)
    return x, y, z, vx, vy, vz, t


def visualization(x, y, z, vx, vy, vz, t):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # определяем графики проекций движения
    axe_x = plt.subplot(321)
    axe_y = plt.subplot(323, sharex=axe_x)
    axe_z = plt.subplot(325, sharex=axe_x)

    axe_vx = plt.subplot(322)
    axe_vy = plt.subplot(324, sharex=axe_vx)
    axe_vz = plt.subplot(326, sharex=axe_vx)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.axis('equal')

    axe_x.plot(t, x, color="red", label="x(t)")
    axe_y.plot(t, y, color="green", label="y(t)")
    axe_z.plot(t, z, color="blue", label="z(t)")

    axe_vx.plot(t, vx, color="red", label="Vx(t)")
    axe_vy.plot(t, vy, color="green", label="Vy(t)")
    axe_vz.plot(t, vz, color="blue", label="Vz(t)")
    
    axe_x.legend()
    axe_y.legend()
    axe_z.legend()

    axe_vx.legend()
    axe_vy.legend()
    axe_vz.legend()
    
    coor = zip(x, y, z)
    x_t, y_t, z_t = next(coor)
    for x1, y1, z1 in coor:
        ax.quiver(x_t, y_t, z_t, x1 - x_t, y1 -
                  y_t, z1-z_t, arrow_length_ratio=0)
        x_t, y_t, z_t = x1, y1, z1
    plt.show()



def write_files(filename, list1, list2, list3, time):
    with open(filename, "w") as file:
        for i, j, k, u in zip(list1, list2, list3, time):
            file.write("{:.6f} {:.6f} {:.6f} {:.6f}\n".format(i, j, k, u))


# блок настройки
delta_t = 0.01
a = 0  # math.pi / 2
incorect = True
while incorect:
    try:
        H = float(input("введите H0: "))
        V0 = float(input("введите V0: "))
        m = float(input("введите m:  "))

        print("введите координаты цели в одну строчку через пробел")
        x_target, y_target, z_target = map(float, input().split())

        if not (0 <= H <= 1400) or not (-250 <= V0 <= 250):
            print("too much value\n")
        elif m <= 0:
            print("масса должна быть положительной")
        else:    
            incorect = False
    except Exception as e:
        print("Incorrect value")
        print(e)


# -------------

# ускорение свободного падения
g = 9.81

# считать таблицы
F, v = get_F()
Wx, Wy, h = get_Wind()

# получить коэффицент соправтивления воздуха
k = get_k_F(F, v)


# апроксимировать зависимость направления ветра от высоты
k_wind_x = get_mass_k_wind(Wx, h)
k_wind_y = get_mass_k_wind(Wy, h)


# начало моделирования
x, y, z, vx, vy, vz, t = projectile(k, 0, 0, H, z_target)

# получили координаты попадания при выпущенном снаряде из координат центра
x_mark, y_mark, z_mark = x[-1], y[-1], z[-1]
# конец моделирования


# если выпустить из координат цели то попадём
# в (x_mark, y_mark, z_mark)


print("Координаты сброса мат точки:", end=" ")
print(x_target-x_mark, y_target-y_mark, H)

# проверка полученных данных
x, y, z, vx, vy, vz, t = projectile(
    k, x_target-x_mark, y_target-y_mark, H, z_target)
x_mark, y_mark, z_mark = x[-1], y[-1], z[-1]

# если вупустить из расчитанных координат куда попадём
print("Координаты попадания: ", end="")
print(x_mark, y_mark, z_mark)

r_2 = (x_mark - x_target)**2 + (y_mark - y_target)**2 + (z_mark - z_target)**2

# расстояние от цели
print("расстояние от цели = {:.6f}".format(math.sqrt(r_2)))

if r_2 < 25:
    print("Засчитано")
else:
    print("Промах")

write_files("coordinates.txt", x, y, z, t)
write_files("V.txt", vx, vy, vz, t)

print("Визуализировать траекторию точки? (y/n)")
vis = input().lower()
if 'y' in vis:
    visualization(x, y, z, vx, vy, vz, t)
