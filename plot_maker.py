mport matplotlib.pyplot as plt
import json

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

n = 3 #  половина от длины списка для медианного фильтра
lst = lst_y2
for i in range(n, len(lst_y2)-n):
    a = lst[i-n : i+n+1]
    b = sorted(a)
    lst_y2[i] = b[n]

lst_x1 = lst_x1[15*24+1 : 80*24+1]  # обрезаем графики
lst_y1 = lst_y1[15*24+1 : 80*24+1]
lst_x2 = lst_x2[14*24+1 : 79*24+1]
lst_y2 = lst_y2[14*24+1 : 79*24+1]

plt.grid()
plt.plot(lst_x1, lst_y1)
plt.plot(lst_x2, lst_y2, color = "red")
plt.show()
