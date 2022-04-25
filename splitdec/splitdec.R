library(missForest)
library(openxlsx)
library(imputeTS)

min_max_norm <- function(x)
{
    (x - min(x)) / (max(x) - min(x))
}

df <- read.xlsx("../misc/campylobacter/campylobacter_germany.xlsx")["case"]
df <- min_max_norm(df)
df_nans <- prodNA(df, noNA=0.2)
df_imputed <- na_seasplit(df_nans)
print(mean(as.matrix((df - df_imputed)^2)))
print(mean(as.matrix((df - na_mean(df_nans))^2)))