library(imputeTS)
library(missForest)
library(ggplot2)

source("common.R")

MSE <- c()

for (reader in c(read_norm, read_camp, read_hpe))
{
    truth   <- min_max_norm(reader())
    amputed <- prodNA(truth, noNA=0.1)
    
    linear <- mse(truth, na_interpolation(amputed))
    spline <- mse(truth, na_interpolation(amputed, option='spline'))
    seadec <- mse(truth, na_seadec(amputed))
    seaspl <- mse(truth, na_seasplit(amputed))
    kalman <- mse(truth, na_kalman(amputed))

    errors <- c(linear, spline, seadec, seaspl, kalman)

    MSE <- append(MSE, errors)
}

data <- rep(c('random', 'Campylobacter', 'HPE Stocks'), each=5)
Methods <- rep(c('linear', 'spline', 'seadec', 'seasplit', 'kalman'), times=3)

df <- data.frame(Methods, data, MSE)
    
plot <- ggplot(df, aes(fill=data, y=MSE, x=Methods)) + 
            geom_bar(position='stack', stat='identity',  width=0.5) + coord_flip() +
            theme(legend.position="bottom")
ggsave(plot=plot, filename='stack.png', height = 3, width = 7) 