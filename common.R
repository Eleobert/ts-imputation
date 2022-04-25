library(openxlsx)


read_norm <- function()
{
    df <- as.data.frame(rnorm(1500))
    colnames(df)[1] <- "truth"
    df
    
}

read_camp <- function()
{
    df <- read.xlsx("datasets/campylobacter_germany.xlsx")["case"]
    colnames(df) <- c("truth")
    df
}


read_hpe <- function()
{
    df <- read.csv("datasets/HPE.csv")["Adj.Close"]
    colnames(df) <- c("truth")
    df
}

min_max_norm <- function(x)
{
    (x - min(x)) / (max(x) - min(x))
}

mse <- function(a, b)
{
    e <- abs(a - b)
    counter <- (e > 1e-9)
    sqrt((1 / sum(counter)) * sum(e))
}
