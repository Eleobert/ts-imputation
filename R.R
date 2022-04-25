
library("pcaMethods", quietly = T)
library(DMwR)


v <- c(2.00, 0.03, 1.32, 0.44,
4.38, 7.24, 8.25, 3.36,
0.29, 1.36, 2.43, 3.01,
2.97, 0.71, 4.67, 1.14,
1.00, 4.31, 3.59, 2.76)
m <- matrix(v, nrow=5, byrow=T)
m.missing <- m
m.missing[2, 1] <- NA
m.missing[4, 1] <- NA

print(m)
m.missing.scaled <- scale(m.missing)
print(m.missing.scaled)
res <- completeObs(pca(m.missing.scaled, method="svdImpute"))
print(unscale(res, res))
print(cor(m))
