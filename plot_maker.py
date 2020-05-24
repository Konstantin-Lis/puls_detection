import matplotlib.pyplot as plt
import json
import numpy as np

adr_1 = "C://USERS/USER/desktop/01-01.json"  #  адрес файла json
with open (adr_1) as file_1:
    y1 = json.load(file_1)

lst_y1 = []
lst_x1 = []
for j in range(len(y1["/FullPackage"])):
    if j < 24*90+1:
        lst_y1.append(y1["/FullPackage"][j]['Value']['pulseRate'])
        lst_x1.append(j/24)

lst_y2 = []
lst_x2 = []
i = 0
adr_2 = "C://USERS/USER/desktop/01-01.txt" #  адрес блокнотовского файла
file_2 = open(adr_2, 'r')
for line in file_2:
    lst_y2.append(int(line))
    lst_x2.append(i/24 + 1)
    i += 1

lst_y3 = []
lst_x3 = []
i = 0
adr_3 = "C://USERS/USER/desktop/01-02.txt" #  адрес блокнотовского файла
file_3 = open(adr_3, 'r')
for line in file_3:
    lst_y3.append(int(line))
    lst_x3.append(i/24 + 1)
    i += 1

n = 31  #  половина от длины списка для медианного фильтра
lst = lst_y2
for i in range(n, len(lst_y2)-n):
    a = lst[i-n : i+n+1]
    b = sorted(a)
    lst_y2[i] = b[n]

lst = lst_y3
for i in range(n, len(lst_y3)-n):
    a = lst[i-n : i+n+1]
    b = sorted(a)
    lst_y3[i] = b[n]


lst_x1 = lst_x1[14*24+1 : 79*24+1]  # обрезаем графики
lst_y1 = lst_y1[14*24+1 : 79*24+1]
lst_x2 = lst_x2[14*24+1 : 79*24+1]
lst_y2 = lst_y2[14*24+1 : 79*24+1]
lst_x3 = lst_x3[14*24+1 : 79*24+1]
lst_y3 = lst_y3[14*24+1 : 79*24+1]

plt.subplot(2, 2, 1)
plt.grid()
plt.plot(lst_x1, lst_y1, color = "green")

plt.subplot(2, 2, 3)
plt.grid()
plt.plot(lst_x2, lst_y2, color = "blue")

plt.subplot(2, 2, 4)
plt.grid()
plt.plot(lst_x3, lst_y3, color = "red")

plt.subplot(2, 2, 2)
plt.grid()
plt.plot(lst_x3, np.array(lst_y3)-np.array(lst_y2), color = "red")

plt.show()
