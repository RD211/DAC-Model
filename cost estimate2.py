from numpy import *
from matplotlib.pyplot import *

t = int(input("For how many years do you want to calculate? "))
innovation_time = int(input("How many years does it take to fully improve the technology? "))
#add a innovation time vector to calculate for 5, 10, 15, 20, 25, 30 years
innovation_times = array([5, 10, 15, 20, 25, 30])
year = zeros(t + 1)
k = 0
t_bcost = array([300, 500]) / 10e9  # dollars per 
t_ccost = array([50, 500]) / 10e9  # dollars
t_scost = 10 / 10e9  # dollars
t_econs = 1200  # Kwh
t_econs2= 500 #possible technology

for i in range(2022, 2022 + t + 1):
    year[k] = i
    k = k + 1

print(year)
print(len(year))

tonnes = [0.2, 0.3, 0.3, 6.8, 13.6, 19.8, 26.1, 32.5, 59.2]
tonnes = array(tonnes)
tonnes2 = zeros(2022 + t - 2030)
slope = (980 - 59.2) / (2050 - 2030)

i = 0
while max(tonnes2) < 980 and i < len(tonnes2):
    tonnes2[i] = 59.2 + slope * (i + 1)
    i += 1

idx = tonnes2 == 0
tonnes2[idx] = 980
tonnes2 = array(tonnes2)

print(type(tonnes))
tonnes = concatenate((tonnes, tonnes2)) * 10e6

bcost = zeros([len(tonnes), 2])
bcost_var = zeros([len(tonnes)]) #Builiding cost taking decreasing cost into account
ccost = zeros([len(tonnes), 2])
ccost_var = zeros([len(tonnes)]) #Capture cost taking decreasing cost into account
scost = zeros(len(tonnes))
econs = zeros(len(tonnes))
econs2 = zeros(len(tonnes))
econs_var = zeros(len(tonnes)) #Energy consumption taking decreasing power consumption into account

#create matrix to store variable cost for different innovation times
bcost_var_tot = zeros([len(tonnes), len(innovation_times)])
ccost_var_tot = zeros([len(tonnes), len(innovation_times)])
econs_var_tot = zeros([len(tonnes), len(innovation_times)])

#Variable cost calculations
t_bcost_var = zeros(len(tonnes))
t_ccost_var = zeros(len(tonnes))
t_econs_var = zeros(len(tonnes))
t_bcost_var[0] = t_bcost[1]
t_ccost_var[0] = t_ccost[1]
t_econs_var[0] = t_econs
#create variable cost matrix for different innovation times
t_bcost_var_tot = zeros([len(tonnes), len(innovation_times)])
t_ccost_var_tot = zeros([len(tonnes), len(innovation_times)])
t_econs_var_tot = zeros([len(tonnes), len(innovation_times)])
t_bcost_var_tot[0] = t_bcost[1]
t_ccost_var_tot[0] = t_ccost[1]
t_econs_var_tot[0] = t_econs

for i in range(1,len(innovation_times)):
    for j in range(1,len(tonnes)):
        if t_bcost_var_tot[j-1,i] >min(t_bcost):
            t_bcost_var_tot[j,i] = t_bcost_var_tot[j-1,i] - (t_bcost[1] - t_bcost[0]) / innovation_times[i]
        else:
            t_bcost_var_tot[j,i] = min(t_bcost)
        if t_ccost_var_tot[j-1,i] > min(t_ccost):
            t_ccost_var_tot[j,i] = t_ccost_var_tot[j-1,i] - (t_ccost[1] - t_ccost[0]) / innovation_times[i]
        else:
            t_ccost_var_tot[j,i] = min(t_ccost)
        if t_econs_var_tot[j-1,i] > t_econs2:
            if t_econs_var_tot[j-1,i] - (t_econs - t_econs2) / innovation_times[i] > t_econs2:
                t_econs_var_tot[j,i] = t_econs_var_tot[j-1,i] - (t_econs - t_econs2) / innovation_times[i]
            else:
                t_econs_var_tot[j,i] = t_econs2
        else:
            t_econs_var_tot[j,i] = t_econs2

for i in range(1,len(tonnes)):
    if t_bcost_var[i-1] >min(t_bcost):
        if t_bcost_var[i-1] - (t_bcost[1] - t_bcost[0]) / innovation_time > min(t_bcost):
            t_bcost_var[i] = t_bcost_var[i-1] - (t_bcost[1] - t_bcost[0]) / innovation_time
        else:
            t_bcost_var[i] = min(t_bcost)
        
    else:
        t_bcost_var[i] = min(t_bcost)

for i in range(1,len(tonnes)):
    if t_ccost_var[i-1] > min(t_ccost):
        if t_ccost_var[i-1] - (t_ccost[1] - t_ccost[0]) / innovation_time > min(t_ccost):
            t_ccost_var[i] = t_ccost_var[i-1] - (t_ccost[1] - t_ccost[0]) / innovation_time
        else:
            t_ccost_var[i] = min(t_ccost)
    else:
        t_ccost_var[i] = min(t_ccost)

for i in range(1,len(tonnes)):
    if t_econs_var[i-1] > t_econs2:
        if t_econs_var[i-1] - (t_econs - t_econs2) / innovation_time < t_econs2:
            t_econs_var[i] = t_econs_var[i-1] - (t_econs - t_econs2) / innovation_time
        else:
            t_econs_var[i] = t_econs2
        
    else:
        t_econs_var[i] = t_econs2   



#Cost calculations
for i in range(len(tonnes)):
    if i + 2 < len(tonnes):
        bcost[i] = (tonnes[i + 2] - tonnes[i + 1]) * t_bcost
        bcost_var[i] = (tonnes[i + 2] - tonnes[i + 1]) * t_bcost_var[i]
        ccost[i] = tonnes[i] * t_ccost
        ccost_var[i] = tonnes[i] * t_ccost_var[i]
        scost[i] = tonnes[i] * t_scost
        econs[i] = tonnes[i] * t_econs
        econs2[i] = tonnes[i] * t_econs2
        econs_var[i] = tonnes[i] * t_econs_var[i]
    else:
        bcost[i] = bcost[i - 1]
        bcost_var[i] = bcost_var[i - 1]
        ccost[i] = tonnes[i] * t_ccost
        ccost_var[i] = tonnes[i] * t_ccost_var[i]
        scost[i] = tonnes[i] * t_scost
        econs[i] = tonnes[i] * t_econs
        econs2[i] = tonnes[i] * t_econs2
        econs_var[i] = tonnes[i] * t_econs_var[i]

#calculate costs for different innovation times
for i in range(len(innovation_times)):
    for j in range(len(tonnes)):
        if j + 2 < len(tonnes):
            bcost_var_tot[j,i] = (tonnes[j + 2] - tonnes[j + 1]) * t_bcost_var_tot[j,i]
            ccost_var_tot[j,i] = tonnes[j] * t_ccost_var_tot[j,i]
            econs_var_tot[j,i] = tonnes[j] * t_econs_var_tot[j,i]
        else:
            bcost_var_tot[j,i] = bcost_var_tot[j - 1,i]
            ccost_var_tot[j,i] = tonnes[j] * t_ccost_var_tot[j,i]
            econs_var_tot[j,i] = tonnes[j] * t_econs_var_tot[j,i]
#calculate cumulative cost
cum_bcost = cumsum(bcost, axis=0)
cum_bcost_var = cumsum(bcost_var, axis=0)
cum_ccost = cumsum(ccost, axis=0)
cum_ccost_var = cumsum(ccost_var, axis=0)
cum_scost = cumsum(scost, axis=0)
cum_econs = cumsum(econs, axis=0)
cum_econs2 = cumsum(econs2, axis=0)
cum_econs_var = cumsum(econs_var, axis=0)

#calculate cumulative cost for different innovation times
cum_bcost_var_tot = cumsum(bcost_var_tot, axis=0)
cum_ccost_var_tot = cumsum(ccost_var_tot, axis=0)
cum_econs_var_tot = cumsum(econs_var_tot, axis=0)





#plot cumulative total cost for different innovation times
plot(year, cum_bcost_var_tot[:,0]+cum_ccost_var_tot[:,0]+cum_scost, label="5 years")
plot(year, cum_bcost_var_tot[:,1]+cum_ccost_var_tot[:,1]+cum_scost, label="10 years")
plot(year, cum_bcost_var_tot[:,2]+cum_ccost_var_tot[:,2]+cum_scost, label="15 years")
plot(year, cum_bcost_var_tot[:,3]+cum_ccost_var_tot[:,3]+cum_scost, label="20 years")
plot(year, cum_bcost_var_tot[:,4]+cum_ccost_var_tot[:,4]+cum_scost, label="25 years")
plot(year, cum_bcost_var_tot[:,5]+cum_ccost_var_tot[:,5]+cum_scost, label="30 years")
#title('Cumulative costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()
# Save the plot instead of showing it
savefig('Cumulative cost for different innovation times',dpi=900)
clf()  # Clear the current figure






#plot cumulative cost
plot(year, cum_bcost_var, label="Building cost")
plot(year, cum_ccost_var, label="Capture cost")
plot(year, cum_scost, label="Storage cost")
plot(year, cum_bcost_var + cum_ccost_var + cum_scost, label="Total cost")
title('Cumulative costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()
# Save the plot instead of showing it
savefig('Cumulative cost',dpi=900)
clf()  # Clear the current figure

#plot cumulative cost comparing with yearly us military budget
plot(year, cum_bcost_var, label="Building cost")
plot(year, cum_ccost_var, label="Capture cost")
plot(year, cum_scost, label="Storage cost")
plot(year, cum_bcost_var + cum_ccost_var + cum_scost, label="Total cost")
#plot US military budget as a yline
#what do i do to plot a purple line?
axhline(y=2010, color='k', linestyle='-', label="US yearly military budget")
#make y axis up to 2100
ylim(0, 2100)
title('Cumulative costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()
# Save the plot instead of showing it
savefig('Cumulative cost compared',dpi=900)
clf()  # Clear the current figure


plot(year, bcost[:, 1], label="Upper bound")
plot(year, bcost_var, label="Variable cost")
plot(year, bcost[:, 0], label="Lower bound")



title('Plant building cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()
# Save the plot instead of showing it
savefig('plant_building_cost.png',dpi=900)
clf()  # Clear the current figure


#plot different energy consumption
plot(year, econs, label="Upper bound",color='r')
plot(year, econs2, label="Lower bound",color='g')
plot(year, econs_var, label="Variable cost",color='b')
title('Energy consumption scenarios for 2050 net-zero')
xlabel("Year")
ylabel("kWh")
grid()
legend()
savefig('energy_consumption.png',dpi=900)
clf()  # Clear the current figure

#plot worse case cost breakdown
plot(year, bcost[:, 1], label="Construction")
plot(year, ccost[:, 1], label="Capture")
plot(year, scost, label="Storage")
title('Costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()

# Save the plot instead of showing it
savefig('costs_worst_case.png',dpi=900)
clf()  # Clear the current figure

#plot better case cost breakdown
plot(year, bcost[:, 0], label="Construction")
plot(year, ccost[:, 0], label="Capture")
plot(year, scost, label="Storage")
title('Costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()

# Save the plot instead of showing it
savefig('costs_best_case.png',dpi=900)
clf()  # Clear the current figure

#plot variable cost breakdown
plot(year, bcost_var, label="Construction")
plot(year, ccost_var, label="Capture")
plot(year, scost, label="Storage")
title('Costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()

# Save the plot instead of showing it
savefig('costs_variable.png',dpi=900)
clf()  # Clear the current figure

plot(year, bcost[:, 1] + ccost[:, 1] + scost, label="Total cost - higher bound")
plot(year, bcost_var + ccost_var + scost, label="Total cost - variable")
plot(year, bcost[:, 0] + ccost[:, 0] + scost, label="Total cost - lower bound")
hlines(1000, xmin=min(year), xmax=max(year), label="Netherlands GDP 2022", colors="r")
title('Total cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
legend(loc="upper right")
yticks(ticks=range(0, 1000, 100))
grid()

# Save the plot instead of showing it
savefig('total_cost_compared.png',dpi=900)
clf()  # Clear the current figure


xlabel("Year")
ylabel("CO2 tonnes")
plot(year, tonnes, label="Yearly captured CO2")
hlines(36.8e9, xmin=min(year), xmax=max(year), label="World emissions 2022", colors='g')
legend(loc="upper right")
grid()

# Save the plot instead of showing it
savefig('captured_co2.png',dpi=900)

clf()  # Clear the current figure
xlabel("Year")
ylabel("kWh")
plot(year, econs, label="Energy usage - lower bound",color='r')
plot(year, econs_var, label="Energy usage - variable",color='b')
plot(year, econs2, label="Energy usage - higher bound",color='g')
hlines(2.2848e+13, xmin=min(year), xmax=max(year), label="World energy consumption 2022", colors= 'y')
legend(loc="upper right")
grid()
30
# Save the plot instead of showing it
savefig('energy.png',dpi=900)
clf()  # Clear the current figure

#plot total cost without comparing it with GDP
plot(year, bcost[:, 1] + ccost[:, 1] + scost, label="Total cost - higher bound")
plot(year, bcost_var + ccost_var + scost, label="Total cost - variable")
plot(year, bcost[:, 0] + ccost[:, 0] + scost, label="Total cost - lower bound")
title('Total cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
legend(loc="upper left")
yticks(ticks=range(0, 1000, 100))
grid()

# Save the plot instead of showing it
savefig('total_cost.png',dpi=900)
clf()  # Clear the current figure

#plot total cumulative cost
plot(year, cum_bcost[:, 1] + cum_ccost[:, 1] + cum_scost, label="Total cost - higher bound")
plot(year, cum_bcost_var + cum_ccost_var + cum_scost, label="Total cost - variable")
plot(year, cum_bcost[:, 0] + cum_ccost[:, 0] + cum_scost, label="Total cost - lower bound")
title('Total cumulative cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
legend(loc="upper left")
yticks()
grid()

# Save the plot instead of showing it
savefig('total_cumulative_cost.png',dpi=900)
clf()  # Clear the current figure


#compare capture cost for different scenarios
plot(year, ccost[:, 1], label="Capture cost - higher bound")
plot(year, ccost_var, label="Capture cost - variable")
plot(year, ccost[:, 0], label="Capture cost - lower bound")
title('Capture cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
legend(loc="upper left")
yticks()
grid()


# Save the plot instead of showing it
savefig('capture_cost.png',dpi=900)
clf()  # Clear the current figure


#plot total cumulative cost for different scenarios
plot(year, cum_bcost[:, 1] + cum_ccost[:, 1] + cum_scost, label="Total cost - higher bound")
plot(year, cum_bcost_var + cum_ccost_var + cum_scost, label="Total cost - variable")
plot(year, cum_bcost[:, 0] + cum_ccost[:, 0] + cum_scost, label="Total cost - lower bound")
#title('Total cumulative cost for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
legend(loc="upper left")
yticks()
grid()

# Save the plot instead of showing it
savefig('total_cumulative_cost_escenarios.png',dpi=900)
clf()  # Clear the current figure

#plot cumulative cost by type for the scenario with 20 years innovation time
plot(year, cum_bcost_var_tot[:,3], label="Building cost")
plot(year, cum_ccost_var_tot[:,3], label="Capture cost")
plot(year, cum_scost, label="Storage cost")
plot(year, cum_bcost_var_tot[:,3] + cum_ccost_var_tot[:,3] + cum_scost, label="Total cost")
#title('Cumulative costs for 2050 net-zero')
xlabel("Year")
ylabel("Billion $")
grid()
legend()

# Save the plot instead of showing it
savefig('Cumulative cost for 20 years innovation time',dpi=900)
clf()  # Clear the current figure

#plot yearly energy consumption for the scenario with 20 years innovation time, comparing it with world yearly energy consumption
xlabel("Year")
ylabel("kWh")
plot(year, econs_var_tot[:,3], label="Energy usage",color='b')
hlines(2.2848e+13, xmin=min(year), xmax=max(year), label="World energy consumption 2022", colors= 'r')
legend(loc="upper right")
grid()

# Save the plot instead of showing it
savefig('energy for 20 years innovation time.png',dpi=900)
clf()  # Clear the current figure
