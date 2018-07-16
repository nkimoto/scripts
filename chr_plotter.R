library(karyoploteR)

args <- commandArgs(trailingOnly=TRUE)

selected_chr <- args
## selected_chr <- c("ChrZ")
## Write Reference genome
ref <- read.table("Length_Silkbase.Sheet1.tsv", sep = "\t", row.names = 1)
chr <- paste0("Chr", rownames(ref))
ref <- as.character(ref[,1])
start <- rep(1, length(chr))
end_tmp <- c()
end <- c()
for (i in strsplit(ref, "\\.\\.")){end_tmp <- append(end_tmp, i[2])}
for (i in strsplit(end_tmp, " \\(")){end <- append(end, i[1])}
end <- as.integer(end)
custom.genome <- toGRanges(data.frame(chr, start, end))

pdf("test_plot")
kp <- plotKaryotype(genome = custom.genome, plot.type=4, cex = 0.6, chromosomes=selected_chr)
#kpAddBaseNumbers(kp, tick.dist = 10000000, tick.len = 10, tick.col="red", cex=1,
#                 minor.tick.dist = 1000000, minor.tick.len = 5, minor.tick.col = "gray")

## Write Genes
genes <- read.table("tblastx_HitTable_orth_test.tsv.txt", header = TRUE, sep = "\t", row.names = 1)
genes["SB_chr"] <- sapply(strsplit(as.character(genes[["SB_chr"]]), "_"), function(x){x[2]})
genes[["SB_chr"]] <- sub("Chr1", "ChrZ", genes[["SB_chr"]])

Trinity_ID <- rownames(genes)
SB_start <- genes[["SB_start"]]
SB_end <- genes[["SB_end"]]
gene.symbols <- c(Trinity_ID)
granges <- makeGRangesFromDataFrame(genes,
#                                    seqinfo=seqinfo(custom.genome),
                                    seqnames.field="SB_chr",
                                    start.field="SB_start",
                                    end.field="SB_end")
values(granges) <- genes[setdiff(colnames(genes), c("SB_chr", "SB_start", "SB_end"))]


kpAddLabels(kp, "MetaData", label.margin = 0.1, srt=90, pos=3, cex=0.8,
            data.panel=1)
kpAddLabels(kp, "TRINITY_ID", r0=0, r1=0.3, cex=0.6,
            data.panel=1)
kpAddLabels(kp, "SB_ID", r0=0.6, r1=0.8, cex=0.6,
            data.panel=1)
kpAddLabels(kp, "bitscore", r0=0.875, r1=0.9, cex=0.6,
            data.panel=1)
kpAddLabels(kp, "evalue", r0=0.975, r1=1.0, cex=0.6,
            data.panel=1)


kpPlotMarkers(kp,
              data=granges,
              cex=0.7, 
              labels=names(granges),
              label.color = "black",
              marker.parts = c(0.2, 0.7, 0.1),
              r0=0, r1 = 0.05,
              adjust.label.position = TRUE,
              data.panel=1)
kpPlotMarkers(kp,
              data=granges,
              cex=0.7, 
              labels=granges$SB_ID,
              label.color = "red",
              marker.parts = c(0.2, 0.7, 0.1),
              r0=0.5, r1=0.55,
              data.panel=1)
kpPlotMarkers(kp,
              data=granges,
              cex=0.7, 
              labels=as.factor(granges$bitscore),
              r0=0.85, r1=0.90,
              #              pos=1,
              #              marker.parts = c(0.2, 0.7, 0.1),
              label.color="blue",
              data.panel=1)
kpPlotMarkers(kp,
              data=granges,
              cex=0.7,
              labels=as.factor(granges$evalue),
              r0=0.95, r1=1.0,
              #              pos=3,
              #              marker.parts = c(0.2, 0.7, 0.1),
              label.color="purple", 
              data.panel=1)
dev.off()

