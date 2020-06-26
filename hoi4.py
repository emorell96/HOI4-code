import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, fixed_quad
import datetime


def productioneffiency(t, productioncap, baseproductionefficiency):
    return np.minimum(np.sqrt(0.002*productioncap*t+baseproductionefficiency**2), productioncap)

def dailyproduction(t, baseproduction, outputmodifier, productioncap, baseproductionefficiency):
    #output modifier gets its value from industry tech (+x% factory output)
    return baseproduction*outputmodifier*productioneffiency(t, productioncap, baseproductionefficiency)


def totalproduction(t, level, concentrated = False, productioncap = 0.6, trade = 0):
    if concentrated:
        omodif = 1+0.15*level+trade
        baseproductionefficiency = 0.1
    else:
        omodif = 1+0.1*level+trade
        baseproductionefficiency = 0.1+0.05*level
    return quad(dailyproduction, 0, t, args=(4.5, omodif, productioncap, baseproductionefficiency))[0]    
T = np.linspace(0, 365, 100)
tank_production_cost = 1
trade_bonus = 0.1
for level in range(1, 2):
    Y = np.vectorize(lambda t: totalproduction(t, level, trade=trade_bonus))(T)/tank_production_cost
    plt.plot(T, Y, label=f"level: {level}, dispersed")

total = 0
for week in range(1, 52):
    total += 50*(totalproduction(week*7, 3)-totalproduction((week-1)*7, 3))/13
print(total)
for level in range(1,2):
    Y = np.vectorize(lambda t: totalproduction(t, level, True, trade=trade_bonus))(T)
    plt.plot(T, Y/tank_production_cost, label=f"level: {level}, concentrated")

plt.legend()    
plt.title("Dispersed vs Concentrated over 2 years at 60% cap. With Additive modifiers.")    


plt.xlabel("Time (days)")
plt.ylabel("Production (units of production)")
plt.grid()

plt.figure()
  
plt.title("Dispersed vs Concentrated Level 1 Efficiency")    
plt.plot(T, productioneffiency(T, 0.60, 0.1+0.05), label="level 1 dispersed")
plt.plot(T, productioneffiency(T, 0.60, 0.1), label = "level 1 concentrated")
plt.legend()   
plt.xlabel("Time (days)")
plt.ylabel("Production efficiency (%)")
plt.grid()
# actual game data:
# Dates = []
# for i in range(13):
#     if i == 0:
#         Dates.append(datetime.date(1937, 1, 1))
#         Dates.append(datetime.date(1937, i+1, 31))
#     else:
#         if i >= 12:
#             year = 1
#         else:
#             year = 0
#         if i > 1:
#             Dates.append(datetime.date(1937+year, (i)%12+1, 1))
# print(Dates)
# Tanks = [0, 30, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

# days = []
# for date in Dates:
#     days.append((date - datetime.date(1937,1,1)).days)

# plt.scatter(days, Tanks, label="real amount of tanks produced")



plt.show()
