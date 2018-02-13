entropy <- function(p){
  return(-sum(p * log2(p)))
}

info_gain <- function(data, feature){
  # for each unique possible values for the feature find entropy and sum it
  
  for (i in 1:len(unique(train_df[feature]))){
    val = unique(train_df[feature])[i]
    pos_example = train_df[train_df[feature] == val && train_df$type == TRUE]
    print(pos_example)
    break
    
  }
}

train_df = read.csv("zoo1.csv")
train_df = train_df[-1]
train_df$type = train_df$type == 'mammal'


no_of_yes = sum(train_df$hair == TRUE)
no_of_no = sum(train_df$hair == FALSE)

info_gain(train_df, 'hair')

for (each in colnames(train_df)){
  
}

# find information gain for each attr ( to find info.gain we need to find entropy)
# set attr as root node which is having max information gain
# 

a <- function(data, feature){
  for (i in 1:length(unique(train_df[feature]))){
    val = unique(train_df[feature])[i]
    print(val)
    print("asdf")
  }
  
}
