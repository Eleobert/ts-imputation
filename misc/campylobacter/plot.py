import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')

df = pd.read_excel('misc/campylobacter/campylobacter_germany.xlsx')
head = df.head(262)
print(head)
plt.plot(head.date, head.case)
plt.show()
df.to_csv('datasets/campylobacter_germany.csv', index=False)