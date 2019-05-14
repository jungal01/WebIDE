# Title     : TODO
# Objective : TODO
# Created by: JasonHu
# Created on: 4/30/2019

require(data.table)
require(dplyr)
require(reshape2)
require(ggplot2)
require(tidyr)
require(plotly)

models<-c(
"LSTM",
"bibow",
"bigramLSTM",
"tranbowsmallvocab",
"transtd",
"vocabbow",
"vocabbowbatchpkl",
"vocablstm",
"mixedbow4"
)

# I want two plots.
# First plot is a cross comparisons of all models, with maximum likelihood loss and hit percentage
csv_dir_path<-"./csv/"
meltdts<-list()
for (model in models){
  model_path<-paste(model,"_train.csv",sep="")
  csv_path<-paste(csv_dir_path,model_path,sep='')
  dt<-fread(csv_path)
  mbs<-max(dt$batch)
  col<-"all"
  if (model =="mixedbow4"){
    col<-"ml"
  }
  
  to_melt<-data.table(point=dt$epoch*mbs+dt$batch,loss=dt[[col]], hit=dt$hit)
  
  meltdts[[model]]<-to_melt
}

loss_dt<-rbindlist(meltdts,idcol=T)
# loss_dt<-melt(meltdts,id=c("point"), measure.vars=c("loss","hit"))
loss_dt<-loss_dt %>% filter(point<2e06) %>% setDT()
lossplot<-ggplot()+
  geom_smooth(data=loss_dt,span=0.3,se=F,aes(x=point,y=loss,color=.id))+
  labs(y="Training Time Cross Entropy Loss", x="Data point", color="Model")
lossplot <- ggplotly(lossplot)
lossplot

loss_dt<-loss_dt %>% filter(point<2e06) %>% setDT()
hitplot<-ggplot()+
  geom_smooth(data=loss_dt,span=0.3,se=F,aes(x=point,y=hit,color=.id))+
  labs(y="Accuracy", x="Data point", color="Model")
hitplot <- ggplotly(hitplot)
hitplot

# Second plot is the winning model, mixed objectives and validations.
model_path<-paste("mixedbow4","_train.csv",sep="")
csv_path<-paste(csv_dir_path,model_path,sep='')
train<-fread(csv_path)
mbs<-max(train$batch)
train<-train %>% mutate(datapoint=mbs*epoch+batch) %>% select(-epoch, -batch) %>% setDT()
train <- melt(train ,  id.vars = 'datapoint', variable.name = 'series')
# valid set
model_path<-paste("mixedbow4","_valid.csv",sep="")
csv_path<-paste(csv_dir_path,model_path,sep='')
valid<-fread(csv_path)
valid<-valid %>% mutate(datapoint=mbs*(epoch)) %>% select(-epoch) %>% setDT()
valid <- melt(valid ,  id.vars = 'datapoint', variable.name = 'series') 

train_valid<-rbindlist(list(train=train,valid=valid),idcol=T)

winplot<-ggplot()+
  geom_smooth(data=train_valid,span=0.1,se=F,aes(x=datapoint,y=value,color=series, linetype=.id))+
  labs(x="Data point",y="Cross Entropy", color="model",linetype="training or validation")
winplot <- ggplotly(winplot)
winplot
