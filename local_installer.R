#!/usr/bin/env R
# Usage: Rscript GetPetitBC.r repodir targetpkg1 targetpkg2 ... targetpkgn
# Example: Rscript GetPetitBC.r ./miniBC GenomicRanges edgeR
# ----
# source("https://bioconductor.org/biocLite.R")
# biocLite("BiocInstaller")
# ----
# install.packages(pkgs, repos=repodir)

library(miniCRAN)

args <- commandArgs(trailingOnly=TRUE)
if(!file.exists(args[1])){
        dir.create(args[1], recursive=TRUE)
}
revolution <- c(CRAN = "http://cran.microsoft.com")
my.pkgs <- c()
for (i in 2:length(args)){
    my.pkgs <- append(my.pkgs, args[i])
}

pkgs <- pkgDep(my.pkgs, suggests = TRUE, enhances=FALSE)
makeRepo(pkgs = pkgs, path=args[1], repos=revolution, type = c("source"))

