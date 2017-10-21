x <- read.table("preemptible-operations.tsv", sep="\t", header=TRUE, na.strings = "");
x$preempt_time <- as.character(x$preempt_time);
x$start <- as.character(x$start);
x$end <- as.character(x$end);

# note: raw date times are not being parsed properly...
z1 <- x$start[9]
z2 <- x$preempt_time[9]

as.POSIXct(z2) - as.POSIXct(z1)

