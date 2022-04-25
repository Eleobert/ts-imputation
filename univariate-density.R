library("imputeTS")
library(missForest)
library(openxlsx)
library(ggplot2)
library(reshape2)

source("common.R")


p <- 0.3
truth   <- min_max_norm(read_norm())
amputed <- prodNA(truth, noNA=p)
linear <- na_interpolation(amputed)
spline <- na_interpolation(amputed, option='spline')
seadec <- na_seadec(amputed)
seaspl <- na_seasplit(amputed)
kalman <- na_kalman(amputed)


#for (reader in c(read_norm, read_camp, read_hpe))
#{
#    truth   <- min_max_norm(reader())
#    amputed <- prodNA(truth, noNA=0.1)
#    
#    linear <- mse(truth, na_interpolation(amputed))
#    spline <- mse(truth, na_interpolation(amputed, option='spline'))
#    seadec <- mse(truth, na_seadec(amputed))
#    seaspl <- mse(truth, na_seasplit(amputed))
#    kalman <- mse(truth, na_kalman(amputed))
#
#    errors <- c(linear, spline, seadec, seaspl, kalman)
#
#    MSE <- append(MSE, errors)
#}
#
#data <- rep(c('random', 'Campylobacter', 'HPE Stocks'), each=5)
#Methods <- rep(c('linear', 'spline', 'seadec', 'seasplit', 'kalman'), times=3)
#
#df <- data.frame(Methods, data, MSE)
#    
#plot <- ggplot(df, aes(fill=data, y=MSE, x=Methods)) + 
#            geom_bar(position='stack', stat='identity',  width=0.5) + coord_flip() +
#            theme(legend.position="bottom")
#ggsave(plot=plot, filename='stack.png', height = 3, width = 7)


df <- data.frame(cbind(truth, linear, spline, seadec, seaspl, kalman))
colnames(df) <- c("original", "linear", "spline", "seas. dec", "seas. spl.", "kalman")
print(head(df))
df <- melt(df)
plot <- ggplot(aes(x=value, colour=variable), data=df) + geom_density()
ggsave(plot=plot, filename=paste("density_", p*100, ".png", sep=""))
