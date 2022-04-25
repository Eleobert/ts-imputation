library("imputeTS")
library(ggplot2)

source("common.R")
source("univariate-pattern.R")

theme = ggplot2::theme_gray()

norm <- min_max_norm(read_norm())
norm$amputed <- ampute_scattr(norm$truth, 0.16)
camp <- min_max_norm(read_camp())
camp$amputed <- ampute_scattr(camp$truth, 0.16)
hpes <- min_max_norm(read_hpe())
hpes$amputed <- ampute_scattr(hpes$truth, 0.16) 

ggplot_na_distribution(norm$amput, theme=theme)
ggplot_na_distribution(camp$amput, theme=theme)
ggplot_na_distribution(hpes$amput, theme=theme)

norm <- ts(norm, frequency=1)
camp <- ts(camp, frequency=53)
hpes <- ts(hpes, frequency=1)

MSE <- c()

for (x in list(norm, camp, hpes))
{
    truth   <- x[, "truth"]
    amputed <- x[, "amputed"]
    
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
            geom_bar(position='stack', stat='identity',  width=0.5) + 
	    coord_flip() + theme(legend.position="bottom")
plot
#ggsave(plot=plot, filename='stack.png', height = 3, width = 7) 
