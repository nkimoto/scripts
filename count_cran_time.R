#!usr/bin/env/R
library(ggplot2)

repos.names <- c("Tokyo", "Ymagata", "revolution", "rstudio", "Toronto", "California")
repos.url <- c("http://cran.ism.ac.jp/",
               "https://ftp.yz.yamagata-u.ac.jp/pub/cran/",
               "http://cran.revolutionanalytics.com",
               "http://cran.rstudio.com/",
               "http://cran.utstat.utoronto.ca/",
               "https://cran.cnr.berkeley.edu/"
               )
pkgName <- "animation"
count <- 100

install.packages(pkgName, repos="http://cran.ism.ac.jp/")
result <- sapply(1:count, function(n){
    time <- sapply(repos.url, function(url){
        system.time(install.packages(pkgName, repos=url))[3]
})
                 names(time) <- repos.names
                 time
})
rowMeans(result)

data <- data.frame(Repos=factor(rep(repos.names, count), levels=repos.names), 
                                      Time=as.vector(result))
ggplot(data, aes(x=Repos, y=Time, fill=Repos)) + geom_boxplot() + ylim(0, max(data$Time))
