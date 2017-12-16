# R version of analysis.py
library(plyr)
library(tibble)
library(dplyr)
library(lubridate)
require(stats)

# sprintf is like print() in Python3 EXCEPT 
# you use comma separator for values in R

# the df[col] syntax does not work in R
# instead use df$col to index col

# a gotcha: when subsetting a df, remember to specify the indices
#   for the col as well df[df$col == '', ]
# this is like Python's slicing syntax using : like so df[]
# If you want to avoid the gotcha, you can also use subset(), which
# will allow you to simply pass in df and condition for 2nd arg

# Flexibility of assignment in R
# Holds all the questions
df <- read.csv('QueryQuestions.csv')
# read.csv('QueryQuestions.csv') -> df
# gotcha: be sure to surround variable name in quotes for assign
# assign("df", read.csv('QueryQuestions.csv'))

# Next confusion is regarding:
#   data type assumption
#   subset by variable name 
#   subset by two conditions (confusing with &)

# Note the flexibility of subsetting in R, you can use 3 versions:
#   df[df[,'col'] operator value, ]
#   df[df$col operator value, ]
#   subset(df, col operator value)

# In Python ClosedDate without data was NA, in R it is '', it's hard knowing
# when empty values will turn into NA or ''
# Use head to peek at rows from top
# head(df[, 'ClosedDate'], 100)
# Mistake: using is.na
# df_q <- subset(df, is.na(ClosedDate))
# df_q <- subset(df, ClosedDate == '')
# Equivalents:
# df_q <- df[df[, 'ClosedDate'] == '', ]
# df_q <- df[df$ClosedDate == '',]

# Logical operator for and is & not &&
# Als note here that = is used for select not <- or ->
# df_q <- subset(df, ClosedDate == '' & Score == 0, 
#     select = c('ClosedDate', 'Score'))
# Equivalents:
# Note here how () is NOT needed for conditions
# df_q <- df[df$ClosedDate == '' & df$Score == 0, c('ClosedDate', 'Score')]
# df_q <- df[which(df$ClosedDate == '' & df$Score > 0),]
# select(df, 1:10)[1:2,]
df <- read.csv('QueryQuestions.csv')
df_q <- subset(df, ClosedDate == '' & AnswerCount > 0 & Score > 0, 
    select = c('ClosedDate', 'Score'))

# Base R for filter
df_q <- df[df$ClosedDate == '' & df$AnswerCount > 0 & df$Score > 0,]
# dplyr filter
# Can use comma for & or just &, | for or
# Note that nothing is modified in-place if not assigned to var
df_q <- filter(df, ClosedDate == '', AnswerCount > 0, Score > 0)
# Another way
# df_q <- filter(df, ClosedDate == '' & AnswerCount > 0 & Score > 0)

# Base R for select (hard to write)
df_q <- df_q[ ,c('AnswerCount', 'Score')]
# dplyr select, easier; it even looks more Pythonic :)
df_q <- select(df_q, AnswerCount, Score, Title)
# fancier one that uses condition of selecting cols
# df_q <- select(df_q, AnswerCount, Score, contains("Date"))
df_q[['ClosedDate']]
# Base R arrange/order
# df_q <- df_q[]

fx <- function(x) {
    return(ifelse(!is.na(x),1,0))
}

# Base R approach
df <- read.csv('QueryQuestions.csv')
# c <- 1:dim(df)[1]
df <- df[df$ClosedDate == '' & df$Score > 0, ]
# most basic way of populating a new column with binary value
df$Accepted <- unlist(ifelse(!is.na(df$AcceptedAnswerId), 1, 0))
# this has the same effect as above
# df$Accepted <- Vectorize(ifelse(!is.na(df$AcceptedAnswerId), 1, 0))
# another way is to use lapply which returns a list, apply unlist to vectorize
# df$Accepted <- unlist(lapply(df$AcceptedAnswerId, function(x) ifelse(!is.na(x), 1, 0)))
# a better way if using an apply() is to use sapply() which vectorizes results
# df$Accepted <- sapply(df$AcceptedAnswerId, function(x) ifelse(!is.na(x), 1, 0))
# cols <- 
df <- df[, c("Score", "Accepted", "ViewCount", "AnswerCount", "CommentCount")]
# trick/gotcha: you don't even need the data=df_q OR FUN=mean
# gotcha: you need to caps the FUN
# gotcha: you need to make data all lower
# trick: add a - operator for desc instead of decreasing=TRUE
df <- aggregate(. ~ Score, data=df, FUN=mean, na.rm=TRUE)
df <- df[order(-df$Score), ]
cor(df, use="complete.obs", method="pearson")
print(head(df, 10))


# Tidy-verse approach
df_t <- read.csv('QueryQuestions.csv') %>% 
    filter(ClosedDate == '', Score > 0) %>%
    mutate(Accepted = ifelse(!is.na(AcceptedAnswerId), 1, 0)) %>%
    select(Score, Accepted, ViewCount, AnswerCount, CommentCount) %>%
    group_by(Score) %>%
    # summarise_at(funs(mean), list("Accepted", "ViewCount", "AnswerCount", "CommentCount"))
    summarise_all(funs(mean)) %>%
    # This is how you'd do it if renaming and picking what funs to apply
    # summarise(Accepted = mean(Accepted), 
    #     ViewCount = mean(ViewCount), 
    #     AnswerCount = mean(AnswerCount), 
    #     CommentCount = mean(CommentCount)) %>%
    arrange(desc(Score))
# Look at correlation btw two things (Pearson default)
# cor(df_q$Score, df_q$Accepted)
cor(df_t, use="complete.obs", method="pearson") 
print(head(df_t, 10))
# Forces tibble into a dataframe when printing
# data.frame(head(df_q,25))

# print(head(df_q, 100))
# R subset df: 
#   format -> 
# df[num|range|list of cols : num|range|list of cols, +/-step]
# All Rows and All Columns
# df[,]
# # First row and all columns
# df[1,]
# # First two rows and all columns
# df[1:2,]
# Add a comman and a -num to go in reverse 
# df[6:1,1:3,-1]
# # First and third row and all columns
# Gotcha: what happens with row at 0?
# There is no error, it is simply ignored
# df_q[c(1,3), ]
# # First Row and 2nd and third column
# df[1, 2:3]
# # First, Second Row and Second and Third COlumn
# df[1:2, 2:3]
# # Just First Column with All rows
# df[, 1]
# # First and Third Column with All rows
# df[,c(1,3)]


# Gotcha: In Python df[1:4] slices and prints result but in R it prints all
# rows with the first 4 columns. 
# Gotcha: Also note how 1:4 is inclusive in R, meaning we count 4 items but 
# in Python 4 is exclusive. This is bc it's 1-based whereas Python is 0-based.
# all rows with 4 cols
# print(df_q[1:4,1:4])
# 4 rows with all cols
# print(df_q[1:4,])

# specifying cols gives us values for the specific column
# Gotcha: typeof
# note how the typeof for the result here is actual typeof of the col, not the
# result of the subsetting! So typeof is more about the element of the result.
# Above, typeof(df_q[1:4,]) would give us list bc each element is a list of 
# values by col
# print(df_q[1:2000,1])


# select(df_q[df_q$Score == 0 && df_q,], CreationDate, Title)
# Subset according to list of columns
# df_q[,c("CreationDate", "Title", "Score", "AnswerCount")][1:5,]

# Holds all the answers
df_a <- read.csv('QueryAllAnswers.csv')
df_at <- nrow(df_a)
# sprintf("Number of answers total: %d", df_at)

# Function defintion differs from Python 
# Notice the functional-style of programming
# function has to be assigned to a variable, a function is
# just like a variable, although the same can be done in
# Python, it's not enforced as functions are not first-class
# by default (programmers are more used to using def by itself)
# Notice how the s is assigned with '=' this is bc in this case
# <- is not allowed and now it makes sense when to use which.
#   You will get an unexpected assignment error if you try <-
ps <- function(df, s="some stat") {
    # Flexibility: notice how the data type for df_qt didn't have to
    # be converted to a float in order to get the decimal points for
    # pct
    sprintf("Number of questions with %s: %d (%.2f%%)", 
        s, 
        nrow(df), 
        (nrow(df) / df_qt) * 100)
}

# questions with at least an answer
df_answer <- df_q[df_q$AnswerCount > 0,]
# ps(df_answer)

# questions with no answer
df_no_answer <- df_q[df_q$AnswerCount == 0,]
# ps(df_no_answer, 'no answers')
