rm(list = ls())
kaggle = read.csv("bodyfatkaggle.csv")
head(kaggle)
fat = read.csv("cleaned_data.csv")
head(fat)
D = fat$DENSITY
B = fat$BODYFAT
error = B - (495/D - 450)
error
dim(fat)
library(ggplot2)

# Residue Plot
#fat$WRIST_OVER_THIGH = fat$WRIST/fat$THIGH
lmmodel = lm(BODYFAT ~ ABDOMEN + WEIGHT + WRIST + FOREARM, data = fat)
# max(predict(lmmodel))
# min(predict(lmmodel))
# max(resid(lmmodel))
# min(resid(lmmodel))
par(mfrow=c(2,2))
plot(lmmodel)
anova(lmmodel)
par(mfrow = c(1,1))
plot(predict(lmmodel),resid(lmmodel),pch=19,cex=1.2,cex.lab=1.5,cex.main=1.5, 
     xlim = c(0,45), ylim = c(-10,10), xlab="Predicted Body Fat %",
     ylab="Residuals",main="Residual Plot")
abline(a=0,b=0,col="red",lwd=3)
legend("bottomright",c("y=0", "Residuals"), pch = c(NA,19),
       lty = c(1,NA), col= c("red", "black"), lwd = c(3,1), cex =0.7)

# Q_Q norm
qqnorm(rstandard(lmmodel),pch=19,cex=1.2,cex.lab=1.5,cex.main=1.5,
       main="Normal Q-Q Plot of the Residuals")
abline(a=0,b=1,col="red",lwd=3)
legend("bottomright",c("y=x", "Points"), pch = c(NA,19), lty = c(1,NA), col= c("red", "black"), lwd = c(3,1))
shapiro.test(resid(lmmodel))


# Independence (Residual Plot)
#plot(resid(lmmodel), type = "l",xlab = "Index", ylab = "Residuals", main = "Test of Independence Plot")
x = 1:length(fat$BODYFAT)
ggplot()+geom_line(aes(x, y = resid(lmmodel),col ="Residuals"),size = 1)+
  theme(legend.position = c(0.93, 0.05), legend.key.height = unit(0.2, 'cm'))+
  scale_colour_manual("",values = c("Residuals" = "black"))+
  ggtitle("Test of Independence Residual Plot")+
  xlab("Index")+ylab("Residuals") +
  theme(plot.title = element_text(hjust = 0.5))

#legend("bottomright",c("Residuals"),pch="",col= "red",lwd=1)

# Constant Variance (Residual Plot)
#plot(fitted(lmmodel), resid(lmmodel), xlab = "Fitted Value",
#     ylab = "Residuals", main = "Test of Constant Variance Plot")
ggplot()+geom_point(aes(x = fitted(lmmodel), y = resid(lmmodel),col ="Residuals"),size = 2)+
  theme(legend.position = c(0.9, 0.1))+
  scale_colour_manual("",values = c("Residuals" = "red"))+
  ggtitle("Test of Constant Variance Plot")+
  xlab("Fitted Value")+ylab("Residuals") +
  theme(plot.title = element_text(hjust = 0.5))












