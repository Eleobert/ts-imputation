library(Amelia)
library(missForest)

min_max_norm <- function(x)
{
    (x - min(x)) / (max(x) - min(x))
}

df <- read.csv2("../datasets/AirQualityUCI.csv")[0:9357, 3:15]
df <- min_max_norm(df)
print(head(df))
df_nans <- prodNA(df, noNA=0.2)
df_imputed <- amelia(df_nans)
print(head(df_imputed$imputations$imp5))
print(mean(as.matrix((df - df_imputed$imputations$imp5)^2)))