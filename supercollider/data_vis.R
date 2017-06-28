setwd("/Users/alexandriaguo/Documents/2016-2017/*misc/EMW/test code")

library(ggplot2)

biota <- read.csv("dataStreams.csv")
biota.edit <- data.frame(sector=biota$SECTOR, diam=biota$DIAMETER, dens=biota$SECTOR.DENSITY)
biota.edit$sector <- as.factor(biota.edit$sector)

ggplot(biota.edit, aes(diam, dens)) + 
  #geom_point(mapping=aes(color=sector, alpha=0.5, size=2)) +
  geom_count(mapping=aes(color=sector, alpha =0.5, size=2))

ggplot(biota.edit, aes(diam, fill=sector)) +
  geom_dotplot(stackgroups=TRUE, stackdir="down", binpositions="all", binwidth=1)
