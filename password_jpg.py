import numpy as np
from PIL import Image
from scipy.stats import mstats
from urllib.request import urlopen


def Sorted(averages):
    threshold = 0.01
    unique_values = []
    for value in averages:
        if not any(abs(value - uv) < threshold for uv in unique_values):
            unique_values.append(value)

    sorted_unique_values = unique_values
    Quantization(sorted_unique_values)


def Quantization(sorted_unique_values):
    SYMBOLS = ['R', '6', '#', '7', 'P', '!', 'M', 'x', '8', 'b', 'K', '1', 'G', 'L', '3', '5', 'T', 'C', '4', 'q', 'e',
               'Z', '*', 'w', '0', 'i', 't', 'o', '9', '2', 'r', 'A', 'X', '@', 'F', 'V', 'D', 'h', 'c', '%', '^', 'n',
               'J', 's', 'Q', 'S', 'g', 'W', 'E', 'Y', 'Z', '_']
    QUANT = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36,
             0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72,
             0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1]

    quantile_edges = mstats.mquantiles(averages, prob=QUANT)

    result_symbols = []
    for avg in sorted_unique_values:
        for i in range(len(quantile_edges) - 1):
            if quantile_edges[i] <= avg < quantile_edges[i + 1]:
                result_symbols.append(SYMBOLS[i])
                break

    result_string = ''.join(result_symbols)
    print("Твой пароль:", result_string)


def inpout_link():
    while True:
        a = input('Введи 1, если хочешь взять локальную картинку/ Введи 2, если хочешь взять картинку из интернета')
        if a == "1":
            link = input(r"Вставь полную ссылку до изображения без кавычек: ")
            img = Image.open(link)
            break
        elif a == "2":
            img = Image.open(urlopen(input('Введи сюда URL на изображение')))
            break
        else:
            print("Попробуй ещё раз, ты где-то ошибся")
    return img


img = inpout_link()
arr = np.asarray(img, dtype='uint8')

writable_arr = arr[:, :, :3] / 255

result = np.sum(writable_arr, axis=1, keepdims=True)
max_values = np.max(result, axis=2, keepdims=True)
norm_znach = result / max_values

norm_znach_squeezed = np.squeeze(norm_znach, axis=1)

# Фильтруем строки, оставляя только те, где не все значения одинаковы
filtered_result = np.array([row for row in norm_znach_squeezed if not np.all(row == row[0])])
averages = np.mean(filtered_result, axis=1)
Sorted(averages)
