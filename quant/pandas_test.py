import numpy as np
import pandas as pd
from pandas import Series, DataFrame

a = np.random.randint(10)
print a
s = Series(a)
print s
print s[[2,0,4]]
print s[ s > 0.5]
df = DataFrame()
index = ['alpha','beta','gamma','delta','eta']
for i in range(5):
    a = DataFrame([np.linspace(i, 5*i,5)],index=[index[i]])
    df = pd.concat([df,a],axis=0)
print df

pd.set_option('display.width',200)

dates = pd.date_range('20150101', periods = 5)
print dates
df = pd.DataFrame(np.random.randn(5,4),index=dates,columns=list('ABCD'))
print df

df2 = pd.DataFrame({ 'A' : 1., 'B': pd.Timestamp('20150214'),
                     'C': pd.Series(1.6,index=list(range(4)),dtype='float64'),
                     'D' : np.array([4] * 4, dtype='int64'),
                     'E' : 'hello pandas!' })
print df2
