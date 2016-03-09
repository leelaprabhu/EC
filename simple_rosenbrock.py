import math
import numpy
import random

countFunc=0
def rosenbrock(x):
    f_x=100*(x[0]*x[0] - x[1])*(x[0]*x[0] - x[1]) + (1 - x[0])*(1 - x[0])
    return f_x

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
        fit2.append(rosenbrock(process(pop[i],lower,upper,prec)))
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

def genOperate(pop, noVar):
    popNew=[]
    for i in range((len(pop)-1)):
        parent1= pop[i][0]
        parent2= pop[i][1]
        chld= crossover(parent1, parent2)
        chld2=mutate(chld)
        chld3=[]
        for j in range(0, noVar):
            chld3.append(int(chld2[j*16:(j+1)*16],2))
        popNew.append(chld3)
    return popNew

prec=16
noVar=2
upper=2.048
lower=-2.048
gen=0
noIndi=100
windowSize=5
fprev=[0.0]*windowSize

results=[]
counts=[]

pop= initPop(noIndi, noVar, prec)
fit= findFit(pop, lower, upper, prec)

while(countFunc<10000):
    results.append(rosenbrock(process(pop[fit.index(max(fit))],lower,upper,prec)))
    counts.append(countFunc)
    print str(rosenbrock(process(pop[fit.index(max(fit))],lower,upper,prec)))+" "+str(countFunc)
    gen=gen+1
    fitScale= scale(fit,fprev)
    fit= fitScale
    popNew= selectPop(pop,fit)
    popNew2= genOperate(popNew, noVar)
    popNew2.append(pop[fit.index(max(fit))])
    fitNew= findFit(popNew2, lower, upper, prec)
    pop= popNew2
    fit= fitNew




