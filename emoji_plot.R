setwd("/home/mike/Documents/Horde Analysis/Horde_Analysis/")
library(ggplot2)
library(plyr)


emoji_df <-read.csv("data/emoji_data.csv")
emoji_df$user=as.character(emoji_df$user)

emoji_sum <- ddply(emoji_df, .(emoji_code), summarise,
                   count = nrow(piece))
emoji_sum <- arrange(emoji_sum, -count)[0:10,]


emoji_df <- subset(emoji_df, emoji_code %in% emoji_sum$emoji_code)

user_sum = ddply(emoji_df, .(user), summarise,
                 count = nrow(piece))
user_sum = arrange(user_sum, - count)[1 : 6,]

emoji_user_sum <- ddply(emoji_df, .(emoji_code,user), summarise,
                   count = nrow(piece))
emoji_user_sum$user[1:10]
user_sum$user[1:10]
emoji_user_sum$user = sapply(emoji_user_sum$user, function(name) {
  if(name %in% user_sum$user) {
    name} else {
      'Other'
    } 
})

emoji_user_sum = arrange(emoji_user_sum, -count)

# custom function for x axis label.
my_axis <- function () {
  structure(
    function(label, x = 0.5, y = 0.5, ...) {
      absoluteGrob(
        do.call("gList", mapply(symbolsGrob, pics[label], x, y, SIMPLIFY = FALSE)),
        height = unit(1.5, "cm"))
    }
  )}

ggplot(emoji_user_sum, aes(x=emoji_code,fill = user)) + 
  geom_histogram(aes(y=count),stat="identity") + coord_flip()
