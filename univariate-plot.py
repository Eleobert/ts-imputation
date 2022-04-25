
# source("common.R")
# library(ggplot2)
# library(cowplot)

# random <- read_norm()
# campyl <- read_camp()
# hpestk <- read_hpe()

# print(head(random))
# print(head(campyl))
# print(head(hpestk))

# # df <- data.frame(random, campyl, hpestk)
# # print(head(df))

# campyl <- min_max_norm(read.xlsx("datasets/campylobacter_germany.xlsx"))
# hpestk <- read.csv("datasets/HPE.csv")["Date", "Adj Close"]
# # p1 <- ggplot() + 
# #     geom_line(data = as.data.frame(campyl), aes(x=date, y=case))

# # ggsave(plot=p1, filename='p1.png', height = 2, width = 7)
# head(hpestk)
# p2 <- ggplot() + 
#     geom_line(data = hpestk, aes(x=Date, y=Adj.Close))

# ggsave(plot=p2, filename='p2.png', height = 2, width = 7) 




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('bmh')

def normalize(x):
    return (x - x.min()) / (x.max() - x.min())

campyl = pd.read_excel('datasets/campylobacter_germany.xlsx')
hpestk = pd.read_csv('datasets/HPE.csv')


plt.plot(campyl.case)
plt.show()
plt.plot(hpestk['Adj Close'])
plt.show()
plt.plot(np.random.normal(size=1500))
plt.show()