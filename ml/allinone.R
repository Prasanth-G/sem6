####################################### k-medoids

k_medoids <- function(data, K, index)
{
    cost = 0
    cost_mat = matrix(0, nrow(data), length(index) + 1)
    for(i in 1:K)
    {
        dup = t(replicate(nrow(data), data[index[i],]))
        cost_mat[,i] = rowSums(abs(data - dup))
    }
    cost_mat[,K+1] = apply(cost_mat[,1:K], 1, which.min)
    cost = sum(apply(cost_mat[,1:K], 1, min))
    print('1::')
    print(cost_mat)  
    print(cost)
    list(cost_mat,cost)
}

data = read.csv('kmedoids.csv')
row = nrow(data)
col = ncol(data)
data = sapply(data, as.numeric)
K = 3 #as.numeric(readline(prompt = 'enter K'))
index = seq(1, row)
medoids = sample(row, K)
medoids2 = medoids
non_medoids = index[! index %in% medoids]
newList = list()
newList = k_medoids(data, K, medoids)
init_cost = newList[[2]]
init_costmat = newList[[1]]
cost = init_cost
costmat = init_costmat
newList2 = list()
cost_cur = 0
costmat_cur = init_costmat 
repeat{
    for(i in 1:length(medoids))
    {
        for(j in 1:length(non_medoids))
        {
            medoids2[i] = non_medoids[j]
            cat('medoids::', medoids2)
            newList2 = k_medoids(data, K, medoids2)
            cost_cur = newList2[[2]]
            costmat_cur = newList2[[1]]
            if(cost_cur >= cost)
            {
                medoids2[i] = medoids[i]
            }
            else
            {
                cat(medoids, 'swapped to', medoids2)
                medoids = medoids2
                cost = cost_cur
                costmat = costmat_cur
            }
        }
    }
    
    if(cost >= init_cost)
        break
    else
        init_cost = cost
}
cat('cost:', cost)
cat('medoids:', medoids)
cat('clusters(check col 3):', costmat)



###################################### bayes net
dataset=read.csv(file.choose())
h=trunc(2/3*(nrow(dataset)))
t=trunc(1/3*(nrow(dataset)))
temp=head(dataset,h)
test=tail(dataset,t)
  act<-test
 # k=nrow(test)
p=1
  yes=0
  no=0
  predicted=c(1:nrow(test))

  for(i in 1:nrow(temp))
  {
    if(temp[i,ncol(temp)]=="yes")
    {
      yes=yes+1
    }else
    {
      no=no+1
    }
  }
  feature=matrix(c(0),nrow=4,ncol=3,byrow=TRUE)
  feature1=matrix(c(0),nrow=4,ncol=2,byrow=TRUE)
  j=1
  cnt=1
  while(j<=2)
  {
    for(i in 1:nrow(temp))
    {
      now=temp[i,j]
      val=which(unique(temp[,j])==now)
      if(temp[i,ncol(temp)]=="yes")
      {
        feature[cnt,val]= feature[cnt,val]+1 
      }else if(temp[i,ncol(temp)]=="no")
      {
        feature[(cnt+1),val]= feature[(cnt+1),val]+1 
      }
      
    }
  
    flag=0
    if(any(feature[cnt,]==0))
    {
      flag=1
      len=unique(temp[,j])
      for(i in 1:ncol(feature))
      {
        feature[cnt,i]=feature[cnt,i]+(1/length(len))
      }
    }
    if(flag==0)
    {
      feature[cnt,]=feature[cnt,]/yes
    }else
    {
      feature[cnt,]=feature[cnt,]/(yes+1)
    }
    flag=0
    if(any(feature[cnt+1,]==0)) 
    { 
      flag=1
      len=unique(temp[,j])
      for(i in 1:ncol(feature))
      {
        feature[cnt+1,i]=feature[cnt+1,i]+(1/length(len))
      }
    }
    
    if(flag==0)
      feature[cnt+1,]=feature[cnt+1,]/no
    else
      feature[cnt+1,]=feature[cnt+1,]/(no+1)
    j=j+1
    cnt=cnt+2
  }
  
  j=3
  cnt=1
  while(j<=4)
  {
    for(i in 1:nrow(temp))
    {
      now=temp[i,j]
      val=which(unique(temp[,j])==now)
      if(temp[i,ncol(temp)]=="yes")
      {
        feature1[cnt,val]= feature1[cnt,val]+1 
      }else if(temp[i,ncol(temp)]=="no")
      {
        feature1[(cnt+1),val]= feature1[(cnt+1),val]+1 
      }
    }
  
    flag=0
    if(any(feature1[cnt,]==0))
    {
      flag=1
      len=unique(temp[,j])
      for(i in 1:ncol(feature1))
      {
        feature1[cnt,i]=feature1[cnt,i]+(1/length(len))
      }
    }
    if(flag==0)
    {
      feature1[cnt,]=feature1[cnt,]/yes
    }else
    {
      feature1[cnt,]=feature1[cnt,]/(yes+1)
    }
    flag=0
    if(any(feature1[cnt+1,]==0)) 
    { 
      flag=1
      len=unique(temp[,j])
      for(i in 1:ncol(feature1))
      {
        feature1[cnt+1,i]=feature1[cnt+1,i]+(1/length(len))
      }
    }
    
    if(flag==0)
      feature1[cnt+1,]=feature1[cnt+1,]/no
    else
      feature1[cnt+1,]=feature1[cnt+1,]/(no+1)
    j=j+1
    cnt=cnt+2
  }
  for(i in 1:nrow(test))
  {
    ytestfeature=test[i,]
    start=1
    res1=1
    cnt1=1
    while(start<=(nrow(feature)-1))
    {
      val=ytestfeature[cnt1]
      storearray=unique(temp[,cnt1])
      storearray=as.character(storearray)
      for(iterator in 1:length(storearray))
      {
        if (val==storearray[iterator])
        {
          posit=iterator
          break
        }
      }
      
      #res1=res1*(feature[start,which((unique(temp[,cnt1])==val))])
      res1=res1*(feature[start,posit])
      
      start=start+2
      cnt1=cnt1+1
    }
    #res11=res1*(b/nrow(temp))
    start=2
    res2=1
    cnt2=1
    while(start<=nrow(feature))
    {
      val=ytestfeature[cnt2]
      storearray=unique(temp[,cnt2])
      storearray=as.character(storearray)
      for(iterator in 1:length(storearray))
      {
        if (val==storearray[iterator])
        {
          posit=iterator
          break
        }
      }
      res2=res2*(feature[start,posit])
      # res2=res2*(feature[start,which((unique(temp[,cnt2])==val))])
      start=start+2
      cnt2=cnt2+1
    }
    start=1
    cnt1=3
    while(start<=(nrow(feature1)-1))
    {
      val=ytestfeature[cnt1]
      storearray=unique(temp[,cnt1])
      storearray=as.character(storearray)
      for(iterator in 1:length(storearray))
      {
        if (val==storearray[iterator])
        {
          posit=iterator
          break
        }
      }
      
      #res1=res1*(feature[start,which((unique(temp[,cnt1])==val))])
      res1=res1*(feature1[start,posit])
      
      start=start+2
      cnt1=cnt1+1
    }
    res11=res1*(yes/nrow(temp))
    start=2
    cnt2=3
    while(start<=nrow(feature))
    {
      val=ytestfeature[cnt2]
      storearray=unique(temp[,cnt2])
      storearray=as.character(storearray)
      for(iterator in 1:length(storearray))
      {
        if (val==storearray[iterator])
        {
          posit=iterator
          break
        }
      }
      res2=res2*(feature1[start,posit])
      # res2=res2*(feature[start,which((unique(temp[,cnt2])==val))])
      start=start+2
      cnt2=cnt2+1
    }
    
    res22=res2*(no/nrow(temp))
    drsum=res11+res22
    res11=res11/drsum
    res22=res22/drsum
    if(res11<res22)
    {
      res=res22
      predicted[p]="yes"
      p=p+1
    }else
    {
      res=res11
      predicted[p]="no"
      p=p+1
    }
  }
  print(predicted)
  tp=0
  tn=0
  fp=0
  fn=0
  for(i in 1:nrow(test))
  {
    if(predicted[i]=="yes" && act[i,ncol(temp)]=="yes")
    {
      tp=tp+1
    }
    else if(predicted[i]=="no" && act[i,ncol(temp)]=="yes")
    {
      fn=fn+1
    }
    else if(predicted[i]=="yes" && act[i,ncol(temp)]=="no")
    {
      fp=fp+1
    }
    else if(predicted[i]=="no" && act[i,ncol(temp)]=="no")
    {
      tn=tn+1
    }
  }
  accuracy=(tp+tn)/(tp+tn+fp+fn)
  prepos=tp/(tp+fp)
  preneg=tn/(tn+fn)
  recpos=tp/(tp+fn)
  recneg=tn/(tn+fp)
  fpos=(2*prepos*recpos)/(prepos+recpos)
  fneg=(2*preneg*recneg)/(preneg+recneg)
  tpr=tp/(tp+fn)
  fpr=fp/(fp+tn)
  tnr=fn/(tp+fn)
  fnr=tn/(fp+tn)



print(paste("accuray",accuracy))
print(paste("prepos", prepos))
print(paste("preneg", preneg))
print(paste("recapos", recpos))
print(paste("recaneg", recneg))
print(paste("fpos", fpos))
print(paste("fneg", fneg))
print(paste("tpr", tpr))
print(paste("tnr", tnr))
print(paste("fpr", fpr))
print(paste("fnr", fnr))


########################## KNN
# Data Set Information:
#   
#   Data were extracted from images that were taken from genuine and forged banknote-like specimens. For digitization, an industrial camera usually used for print inspection was used. The final images have 400x 400 pixels. Due to the object lens and distance to the investigated object gray-scale pictures with a resolution of about 660 dpi were gained. Wavelet Transform tool were used to extract features from images.
# 
# 
# Attribute Information:
#   
# 1. variance of Wavelet Transformed image (continuous) 
# 2. skewness of Wavelet Transformed image (continuous) 
# 3. curtosis of Wavelet Transformed image (continuous) 
# 4. entropy of image (continuous) 
# 5. class (integer) 



data<- read.csv(file.choose())

data[data=='?']=NA
data=na.omit(data)
smp_size <- floor(0.9 * nrow(data))
train_ind <- sample(nrow(data), size = smp_size)

data <- data[train_ind, ]
data_test<- data[-train_ind, ]

n=nrow(data)
k=5
truePos=0
trueNeg=0
falsePos=0
falseNeg=0
classI=ncol(data)
disI=classI+1
for( i in (1:nrow(data_test)))
{
  data[,disI]=0
  for( j in (1:(ncol(data_test)-1)))
  {
        data[,disI]<-data[,disI]+(data[,j]-data_test[i,j])**2
  }
  data1<-data[order(data$V6),]   #data$ncol(data)+1
  data1<-data1[1:k,]
  class<-as.data.frame(table(data1[,classI]))
  c<-which.max(class$Freq)
  if(class$Var1[c]==data_test[i,classI] && data_test[i,classI]==0 )
    truePos=truePos+1
  else if(class$Var1[c]==data_test[i,classI] && data_test[i,classI]==1)
    trueNeg=trueNeg+1
  else if(class$Var1[c]!=data_test[i,classI] && data_test[i,classI]==0)
    falseNeg=falseNeg+1
  else if(class$Var1[c]!=data_test[i,classI] && data_test[i,classI]==1)
    falsePos=falsePos+1
}
precision=truePos/(truePos+falsePos)
recall=truePos/(truePos+falseNeg)
fmeasure=2*(precision*recall)/(precision+recall)

print("Recall: ")
print(recall)
print("Precision")
print(precision)
print("fmeasure")
print(fmeasure)

#################################### k Means

K_means <- function(data, centroids, K)
{
    cluster = matrix(0,nrow(data),1)
    distance_mat = matrix(0.0, nrow(data), K)
    d = matrix(0.0, nrow(data), K)
    for(i in 1:K)
    {
        centroid_mat = t(replicate(nrow(data), centroids[i,]))
        distance_mat[,i] = sqrt(rowSums((data - centroid_mat)**2))
    }
    cluster = apply(distance_mat, 1, which.min)
    for( i in 1:K)
    {
        index = which(cluster == i)
        if(length(index) != 1)
            centroids[i,] = colSums(data[index,])/length(index)
        else
            centroids[i,] = data[index,]
    }
    print(cluster)
    print(centroids)
    list(cluster,centroids)
}

data = read.csv('kmeans.csv')
row = nrow(data)
col = ncol(data)
data = Matrix::as.matrix(data)
K = 2
index = sample(1:row, K)
#K = as.integer(readline(prompt = 'enter K'))
centroids = data[index,]
cluster = matrix(0,nrow(data),1)
newList = list(cluster, centroids)
while(TRUE)
{
    newList = K_means(data, centroids, 2)
    cluster1 = newList[[1]]
    centroids_re = newList[[2]]
    newList = K_means(data, centroids_re, 2)
    cluster2 = newList[[1]]
    centroid_re2 = newList[[2]]
    if(all(cluster1 == cluster2) | all(centroids_re == centroid_re2))
        break
    else
        centroids = centroid_re2
}

######################## LDA

library(matlib)
library(plot3D)
dataSet = iris

row = nrow(dataSet)
col = ncol(dataSet)

data1 = c()
for(i in 1:col) {
  data1 = c(data1,c(dataSet[,i]))
}

data = matrix(data = data1,row,col)

class = levels(iris$Species)

x = list()
covMat = list()
m = list()
C = matrix(0,4,4)


rowSize = c()
for( i in 1:length(class)){
  
  s = subset(iris,iris[,5] == class[i])
  m[[i]] = colMeans(s[,1:4])
  rowSize = c(rowSize,nrow(s))
  x[[i]] = s
  c = matrix(0,4,4)
  for(j in 1:4){
    for(k in 1:4){
      c[j,k] = cov(s[,j],s[,k])
    }
  }
  covMat[[i]] = c
}

for(i in 1:4){
  for(j in 1:4){
    for(k in 1:length(covMat)){
      C[i,j] = C[i,j] + rowSize[k] * covMat[[k]][i,j]
    }
    c[i,j] = c[i,j]/nrow(dataSet)
  } 
}

Cinv = inv(C)

P = rowSize/nrow(dataSet)

output = matrix(0,150,2)
x = c()
y = c()
z = c()
for(j in 1:150){
  f = c()
  testInstance = dataSet[j,1:4] 
  for(i in 1:length(class)){
    f[i] = m[[i]] %*% Cinv %*% t(testInstance) - 0.5 * m[[i]] %*% Cinv %*% (m[[i]]) + log(P[i], base = exp(1))
  }
  output[j,1] = max(f)
  output[j,2] = which.max(f)
  
  x = c(x,f[1])
  y = c(y,f[2])
  z = c(z,f[3])

}

output = cbind(output,data[,5])

# plot(output[,1],col = c("red","blue","purple")[output[,2]])

scatter3D(x,y,z,colvar = output[,2])


##################################### PCA

#setwd('G:/Programs/Sem6/ML/pca')
#dataSet = read.csv('iris data.csv')
dataSet = iris
k = 2 

# x = c(2.50,0.5,2.2,1.9,3.1,2.3,2,1,1.5,1.2)
# y = c(2.40,.7,2.9,2.2,3,2.7,1.6,1.1,1.6,.9)

row = nrow(dataSet)
col = ncol(dataSet)

data1 = c()
for(i in 1:col) {
  data1 = c(data1,c(dataSet[,i]))
}

data = matrix(data = data1,row,col)

means = colMeans(data)

data = data[,1:4]

covMat = matrix(0,4,4)

for( i in 1:4){
  for( j in 1:4){
    covMat[i,j] = cov(data[,i],data[,j])
  }
}

eig = svd(covMat)

uReduce = eig$u[,1:k]

z = data %*% uReduce

z1 = cbind(z,dataSet[,5])

plot(z1[,1],z1[,2],col = c("red","blue","green")[z1[,3]])
    
    
######### linear reg
val <- read.csv(file.choose())
age <- val$A1
sp <- val$B
reg <- lm(sp~age)
 
val <- val[-2,]
 
age <- val$A1
sp <- val$B
plot(age,sp,col = "blue",main = "age & pressure regression",
     abline(lm(sp~age)),cex = 1.3,pch = 16,xlab = "age",ylab = "systolic pressure")
age_ = mean(age)
sp_ = mean(sp)
 
ssxy = sum((age - age_)*(sp - sp_))
ssxx = sum((age - age_)**2)
b1 = ssxy/ssxx
b0 = sp_ - (b1*age_)
sp_cap = b0 + b1*age
sse = sum((sp-sp_cap)**2)
sy = sum((sp - sp_)**2)
R2 = 1 - (sse/sy)
print(R2)
