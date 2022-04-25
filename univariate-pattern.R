library(imputeTS)
library(ggplot2)
library(missForest)
#source("common.R")


gen <- function(size, n_blocks, exp)
{
    set.seed(101)
    x <- rep(0, size)
    s <- sort(sample(1:size, n_blocks))
    e <- round(rexp(n_blocks, 1/exp))
    r <- rep(s, times=e)
    t <- rep(0, length(r))
    
    for(i in 2:length(r))
    {
        if(r[i] == r[i-1]) t[i] <- t[i-1] + 1
    }
    
    t <- t + r
    t[t <= size]
}


ampute_blocks <- function(x, n_blocks, exp)
{
    mask <- gen(length(x), n_blocks, exp)
    x[mask] <- NA
    x
}


ampute_scattr <- function(x, p)
{
    size <- length(x)
    mask <- sort(sample(1:size, round(p * size)))
    x[mask] <- NA
    x
}

