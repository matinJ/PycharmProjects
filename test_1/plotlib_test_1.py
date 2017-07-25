# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt

years=[1950,1960,1970,1980,1990,2000,2010]
gdp=[300.2,543.3,1075.9,2826.5,5979.6,10287.9,14589.7]

plt.plot(years,gdp,color='green',marker='o',linestyle='solid')
plt.title("名义GDP")
plt.ylabel("十亿美元")
plt.show()