library(ggvis)
library(dplyr)
library(data.table)
library(ggplot2)

# this one works!!
scorecard = group_by(Scorecard, st_fips) %>% filter(AVGFACSAL != "NA") %>% summarize(mean = mean(AVGFACSAL))
survey = group_by(ss13pusa, ST) %>% filter(PINCP != "NA") %>% summarize(mean = mean(PINCP))
# find average for state income in survey
survey = group_by(ss13pusa, ST) %>% filter(PINCP != "NA") %>% summarize(mean = mean(PINCP))

#merge them
total = merge(scorecard, ss13pusa, by.x = "st_fips", by.y = "ST")

#plot them
ggplot(total, aes(x = AVGFACSAL, y = PINCP,col = STABBR)) + geom_point()
