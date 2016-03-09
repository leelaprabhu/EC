import math
import numpy
import random

countFunc=0
def ackley(x):
    sig1=0.0
    sig2=0.0
    for i in range(0,len(x)):
        sig1= sig1+(x[i]*x[i])
        sig2= sig2+(math.cos(2.0*math.pi*x[i]))
    exp1= -0.2*math.sqrt(1.0/len(x)*sig1)
    exp2= 1.0/len(x)*sig2
    f_x= 20.0+ math.e - 20.0*math.exp(exp1) - math.exp(exp2)
    return f_x

def mutate(sample):
    mutant=''
    for i in range(len(sample)):
        prob= random.random()
        if (prob<(1.0/len(sample))):
            if (sample[i]=='1'):
                mutant=mutant+'0'
            else:
                mutant=mutant+'1'
        else:
            mutant=mutant+sample[i]
    return mutant

def initPop(noIndi, noVar, prec):
    pop= []
    for i in range(0,noIndi):
        pop.append(numpy.random.random_integers(0, int(math.pow(2,prec)-1),noVar))
    return pop

def process(x, lower, upper, prec):
    ret=[]
    step=(upper-lower)/(math.pow(2,prec)-1)
    for i in range(0, len(x)):
        ret.append(lower+step*x[i])
    return ret

def findFit(pop, lower, upper, prec):
    fit2=[]
    global countFunc
    for i in range(0, len(pop)):
        countFunc= countFunc+1
        fit2.append(ackley(process(pop[i],lower,upper,prec)))
    fitMax= max(fit2)*1.05
    fit3=[]
    for i in range(0, len(pop)):
        fit3.append(fitMax-fit2[i])
    return fit3

def scale(fit,fprev):
    fitScale=[]
    fmin=min(fit)
    xxx=fprev.pop(0)
    fprev.append(fmin)
    for i in range(0, len(fit)):
        fitScale.append(fit[i]-min(fprev))
    return fitScale

def findgreater(roulette,num):
    for i in range(0,len(roulette)):
        if roulette[i]>num:
            return i

def format(parent):
    str_parent=''
    for i in range(0,len(parent)):
        str_parent= str_parent+ '{0:016b}'.format(parent[i])
    return str_parent

def select2(indis,fitness_scaled):
    roulette=[]
    for i in range(0,len(indis)):
        roulette.append(sum(fitness_scaled[0:i+1]))
    num1= findgreater(roulette,random.random()*roulette[len(roulette)-1])
    num2=num1
    while(num1==num2):
        num2= findgreater(roulette,random.random()*roulette[len(roulette)-1])
    parent1= indis[num1]
    parent2= indis[num2]
    return [format(parent1),format(parent2)]

def selectPop(pop,fit):
    parents=[[]]
    for i in range(0,len(pop)):
        parents.append(select2(pop,fit))
    xxx=parents.pop(0)
    return parents

def crossover(parent1,parent2):
    chld=''
    p1=random.randint(0,len(parent1)-2)
    p2=p1
    while(p2==p1):
        p2=random.randint(0,len(parent2)-2)
    pt1=min(p1,p2)
    pt2=max(p1,p2)
    ch=random.randint(0,1)
    if ch==0:
        chld=parent1[0:pt1+1]+parent2[pt1+1:pt2+1]+parent1[pt2+1:len(parent2)]
    else:
        chld=parent2[0:pt1+1]+parent1[pt1+1:pt2+1]+parent2[pt2+1:len(parent2)]
    return chld

def genOperate(pop, noVar):
    popNew=[]
    for i in range((len(pop)-1)):
        parent1= pop[i][0]
        parent2= pop[i][1]
        xOverProb=random.random()
        if(xOverProb>0.4):
            chld=crossover(parent1,parent2)
        else:
            if(random.random()>0.5):
                chld=parent1
            else:
                chld=parent2
        chld2=mutate(chld)
        chld3=[]
        for j in range(0, noVar):
            chld3.append(int(chld2[j*16:(j+1)*16],2))
        popNew.append(chld3)
    return popNew

prec=16
noVar=30
upper=30
lower=-30
gen=0
noIndi=100
windowSize=5
fprev=[0.0]*windowSize

pop= initPop(noIndi, noVar, prec)
fit= findFit(pop, lower, upper, prec)
results=[]
counts=[]

while(countFunc<100000):
    results.append(ackley(process(pop[fit.index(max(fit))],lower,upper,prec)))
    counts.append(countFunc)
    print str(ackley(process(pop[fit.index(max(fit))],lower,upper,prec)))+" "+str(countFunc)
    gen=gen+1
    fitScale= scale(fit,fprev)
    fit= fitScale
    popNew= selectPop(pop,fit)
    popNew2= genOperate(popNew, noVar)
    popNew2.append(pop[fit.index(max(fit))])
    fitNew= findFit(popNew2, lower, upper, prec)
    pop= popNew2
    fit= fitNew




