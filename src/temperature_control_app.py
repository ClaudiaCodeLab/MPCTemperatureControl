import streamlit as st
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from io import BytesIO

# Define the MPC function
def run_mpc(current_temp, setpoint_temp, alpha=0.1, beta=0.5, delta_t=1.0, N=10, lambda_reg=0.1):
    # Parameters
    total_time_steps = 50
    time = np.arange(total_time_steps)
    
    # Initial conditions
    T = np.zeros(total_time_steps)
    T[0] = current_temp
    u = np.zeros(total_time_steps)
    
    # Generate synthetic ambient temperature
    T_ambient = 15.0 + 5 * np.sin(0.1 * time)
    
    # MPC Optimization loop
    for t in range(total_time_steps - N):
        T_var = cp.Variable(N + 1)
        u_var = cp.Variable(N)
        
        constraints = [T_var[0] == T[t]]
        for k in range(N):
            constraints += [
                T_var[k+1] == T_var[k] + delta_t * (-alpha * (T_var[k] - T_ambient[t+k]) + beta * u_var[k]),
                u_var[k] >= 0,
                u_var[k] <= 10
            ]
        
        cost = 0
        for k in range(N):
            cost += cp.square(T_var[k+1] - setpoint_temp) + lambda_reg * cp.square(u_var[k])
        
        prob = cp.Problem(cp.Minimize(cost), constraints)
        prob.solve()
        
        u[t] = u_var.value[0]
        T[t+1] = T[t] + delta_t * (-alpha * (T[t] - T_ambient[t]) + beta * u[t])
    
    return time, T, T_ambient, u

# Streamlit app
st.title('Temperature Control with MPC')

st.sidebar.header('User Inputs')
current_temp = st.sidebar.slider('Current Temperatures (°C)', min_value=-10, max_value=40, value=20)
setpoint_temp = st.sidebar.slider('Desired Setpoint Temperatures (°C)', min_value=-10, max_value=40, value=22)

st.sidebar.text("Adjust the parameters to see the control response.")

# Run MPC
time, T, T_ambient, u = run_mpc(current_temp, setpoint_temp)

# Plot the results
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot room temperature and ambient temperature
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Temperature (°C)', color='tab:blue')
ax1.plot(time, T, label='Room Temperature', color='tab:blue')
ax1.plot(time, T_ambient, label='Ambient Temperature', linestyle='--', color='tab:orange')
ax1.plot(time, setpoint_temp * np.ones(len(time)), label='Setpoint Temperature', linestyle='-.', color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Plot heating power on a second y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Heating Power', color='tab:red')
ax2.plot(time, u, label='Heating Power', linestyle=':', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Add legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1, labels1, loc='upper left')
ax2.legend(lines2, labels2, loc='upper right')

# Adjust layout
fig.tight_layout()

# Save to BytesIO object to display in Streamlit
buf = BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
st.image(buf, use_column_width=True)
