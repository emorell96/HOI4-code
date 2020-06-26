import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, fixed_quad
import datetime


def productioneffiency(t, productioncap, baseproductionefficiency):
    return np.minimum(np.sqrt(0.002*productioncap*t+baseproductionefficiency**2), productioncap)

def dailyproduction(t, baseproduction, outputmodifier, productioncap, baseproductionefficiency):
    #output modifier gets its value from industry tech (+x% factory output)
    return baseproduction*outputmodifier*productioneffiency(t, productioncap, baseproductionefficiency)


def totalproduction(t, level, concentrated = False, productioncap = 0.6, trade = 0, research_time = False, research_bonus = 0, factory_change = False):
    research_tools = 127  #base tech (tools I)
    research_industry = 170*level #assuming no advanced of its time penalty (so this is only valid for level 1) #industry level research time
    research_tools /= 1+research_bonus
    research_industry /= 1+research_bonus

    if concentrated:
        omodif = 1+0.15*level+trade
        baseproductionefficiency = 0.1
        if research_time:
            #base case
            omodif = 1+0.15*(level-1)+trade #so you are still in the previous level of industry
            baseproductionefficiency = 0.1
            productioncap = 0.5
            if t > research_tools and t < research_tools+research_industry: #you have a higher cap now
                productioncap = 0.6 #before research of tools 1 we are capped at 50% efficiency, now we are at 60%
            elif t > research_tools+research_industry: #now you have industry as well. 
                omodif = 1+0.15*level+trade
                productioncap = 0.6
                baseproductionefficiency = 0.1
    else:
        omodif = 1+0.1*level+trade
        baseproductionefficiency = 0.1+0.05*level
        if research_time:
            #base case
            omodif = 1+0.10*(level-1)+trade #so you are still in the previous level of industry
            baseproductionefficiency = 0.1+0.05*(level-1)
            productioncap = 0.5
            if t > research_tools and t < research_tools+research_industry: #you have a higher cap now
                productioncap = 0.6 #before research of tools 1 we are capped at 50% efficiency, now we are at 60%
            elif t > research_tools+research_industry: #now you have industry as well. 
                omodif = 1+0.1*level+trade
                productioncap = 0.6
                baseproductionefficiency = 0.1+0.05*level
    return quad(dailyproduction, 0, t, args=(4.5, omodif, productioncap, baseproductionefficiency))[0], productioneffiency(t, productioncap, baseproductionefficiency)    
T = np.linspace(0, 2*365, 500)
tank_production_cost = 1
trade_bonus = 0
research = True #change this to false to ignore research time.
research_bonus = 0.1
for level in range(1, 2):
    Y = np.vectorize(lambda t: totalproduction(t, level, concentrated=False ,trade=trade_bonus, research_time=research, research_bonus=research_bonus))(T)
    plt.plot(T, Y[0]/tank_production_cost, label=f"level: {level}, dispersed")

for level in range(1,2):
    Y = np.vectorize(lambda t: totalproduction(t, level, concentrated=True, trade=trade_bonus, research_time=research, research_bonus=research_bonus))(T)
    plt.plot(T, Y[0]/tank_production_cost, label=f"level: {level}, concentrated")

plt.legend()    
plt.title("Dispersed vs Concentrated over 2 years at 50% cap, then 60% after Tools I. With Additive modifiers.\nResearch time taken into account.\nResearch bonus of 10% since day 1.")    


plt.xlabel("Time from start of the game(days)")
plt.ylabel("Production (units of production)")
plt.grid()

plt.figure()
  
plt.title("Dispersed vs Concentrated Level 1 Efficiency.\nResearch time taken into account.\nResearch bonus of 10% (since day 1)")    

Y = np.vectorize(lambda t: totalproduction(t, 1, concentrated=False ,trade=trade_bonus, research_time=research, research_bonus=research_bonus))(T)
plt.plot(T, Y[1], label="level 1 dispersed")
Y = np.vectorize(lambda t: totalproduction(t, level, concentrated=True, trade=trade_bonus, research_time=research, research_bonus=research_bonus))(T)
plt.plot(T, Y[1], label = "level 1 concentrated")
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
