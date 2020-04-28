import matplotlib.pyplot as plt
import json

adr = "C://USERS/USER/desktop/01-01.json"  #  адрес файла json
with open (adr) as file:
    y = json.load(file)
lst_y = []
lst_x = []
for j in range(len(y["/FullPackage"])):
    lst_y.append(y["/FullPackage"][j]['Value']['pulseRate'])
    lst_x.append(j/4)

plt.grid()
plt.plot(lst_x, lst_y)
plt.show()
