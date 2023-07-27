# import streamlit as st
# import numpy as np
# from models import AdvancedBatteryValueModel
# import matplotlib.pyplot as plt

# # Define the model
# model = AdvancedBatteryValueModel()

# # Sidebar Inputs
# st.sidebar.title("Input Parameters")

# original_price = st.sidebar.slider("Original Price", 10000, 50000, 35000)
# soh = st.sidebar.slider("State of Health (SOH)", 0.0, 1.0, 0.8)
# t = st.sidebar.slider("Time (years)", 1, 10, 3)
# km = st.sidebar.slider("Distance Driven (km)", 0, 200000, 60000)
# fastcharge_events = st.sidebar.slider("Fast Charge Events", 0, 500, 200)
# time_high_temp = st.sidebar.slider("Time Spent Above 40C", 0, 500, 100)
# time_deep_discharge = st.sidebar.slider("Time Spent Below 40% Discharge", 0, 500, 50)

# # Calculate remaining value
# remaining_value = model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge)

# # Display result
# st.title("Remaining Value")
# st.write(f"The remaining value of the battery is ${remaining_value:,.2f}")

# # Plot
# fig, ax = plt.subplots()
# SOH_values = np.linspace(0, 1, 100)
# remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for soh in SOH_values]
# ax.plot(SOH_values, remaining_values)
# ax.set_xlabel('State of Health (SOH)')
# ax.set_ylabel('Remaining Value')
# ax.set_title('Remaining Value vs. State of Health')
# st.pyplot(fig)


# import streamlit as st
# import numpy as np
# from models import AdvancedBatteryValueModel
# import matplotlib.pyplot as plt

# # Define the model
# model = AdvancedBatteryValueModel()

# # Sidebar Inputs
# st.sidebar.title("Input Parameters")

# original_price = st.sidebar.slider("Original Price", 25000, 50000, 35000)
# soh = st.sidebar.slider("State of Health (SOH)", 0.0, 1.0, 0.8)
# t = st.sidebar.slider("Time (years)", 1, 10, 3)
# km = st.sidebar.slider("Distance Driven (km)", 0, 200000, 60000)
# fastcharge_events = st.sidebar.slider("Fast Charge Events", 0, 500, 200)
# time_high_temp = st.sidebar.slider("Time Spent Above 40C", 0, 500, 100)
# time_deep_discharge = st.sidebar.slider("Time Spent Below 40% Discharge", 0, 500, 50)

# # Define parameter ranges
# SOH_values = np.linspace(0.1, 1.0, 100)
# t_values = np.linspace(1, 10, 100)
# km_values = np.linspace(0, 200000, 100)
# fastcharge_values = np.linspace(0, 500, 100)
# temp_values = np.linspace(0, 500, 100)
# discharge_values = np.linspace(0, 500, 100)

# # Create plots for each parameter
# params = [(SOH_values, "SOH"), (t_values, "t"), (km_values, "km"), 
#     (fastcharge_values, "fastcharge_events"), 
#     (temp_values, "time_high_temp"), 
#     (discharge_values, "time_deep_discharge")
# ]

# for param_values, param_name in params:
#     fig, ax = plt.subplots()

#     if param_name == "SOH":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for soh in param_values]
#     elif param_name == "t":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for t in param_values]
#     elif param_name == "km":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for km in param_values]
#     elif param_name == "fastcharge_events":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for fastcharge_events in param_values]
#     elif param_name == "time_high_temp":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for time_high_temp in param_values]
#     elif param_name == "time_deep_discharge":
#         remaining_values = [model.remaining_value(original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge) for time_deep_discharge in param_values]

#     ax.plot(param_values, remaining_values)
#     ax.set_xlabel(param_name)
#     ax.set_ylabel('Remaining Value')
#     ax.set_title('Remaining Value vs. ' + param_name)

#     st.pyplot(fig)



import streamlit as st
import numpy as np
import pandas as pd
from models import AdvancedBatteryValueModel
import matplotlib.pyplot as plt
from constants import *

# Define the model
model = AdvancedBatteryValueModel()

# Sidebar default setting
st.set_page_config(initial_sidebar_state="expanded")

# Sidebar Inputs
st.sidebar.title("Input Parameters")
original_price = st.sidebar.slider("Original Carprice [$]", 25000, 100000, 35000)
soh = st.sidebar.slider("State of Health (SOH)", 0.0, 1.0, 0.8)
t = st.sidebar.slider("Battery Age [years]", 0, 10, 3)
km = st.sidebar.slider("Distance Driven [km]", 0, 200000, 60000)
fastcharge_events = st.sidebar.slider("Fast Charge Events [Nr.]", 0, 500, 200)
time_low_temp = st.sidebar.slider("Time <10°C [h]", 0, 500, 100)
time_deep_discharge = st.sidebar.slider("Time <40% State of Charge (SOC) [h]", 0, 500, 50)

# Calculate remaining value
remaining_value = model.remaining_value(original_price, soh, t, km, fastcharge_events, time_low_temp, time_deep_discharge)

# Display result
battery_value = original_price*BATTERY_TO_EV_VALUE_RATIO
battery_value_after_vat = battery_value*model.f_vat(VAT_RATE)
st.title("Remaining Value of EV battery")
st.write(f"The original value of the battery was: ${battery_value:,.2f}")
st.write(f"- Battery value due to VAT reduction: ${battery_value_after_vat:,.2f}")
st.write(f"The remaining value of the battery with the given input parameters is (min 5% of Carprice):")
st.write(f"${remaining_value:,.2f}")

# Calculate depreciation caused by each feature
features = ['SOH', 'Warranty Time', 'Warranty Distance', 'Fast Charge', 'Time <10°C', 'Time <40% SOC']
depreciations = [
    battery_value_after_vat - battery_value_after_vat * model.f_soh(soh),
    battery_value_after_vat - battery_value_after_vat * model.f_warranty_time(t),
    battery_value_after_vat - battery_value_after_vat * model.f_warranty_distance(km),
    battery_value_after_vat - battery_value_after_vat * model.f_fastcharge(fastcharge_events),
    battery_value_after_vat - battery_value_after_vat * model.f_low_temp(time_low_temp),
    battery_value_after_vat - battery_value_after_vat * model.f_deep_discharge(time_deep_discharge)
    ]

# Create a DataFrame for plotting
df = pd.DataFrame(list(zip(features, depreciations)), columns=['Feature', 'Depreciation'])
df = df.set_index('Feature')
# df = df.sort_values(by='Depreciation', ascending=False)

# Plot
# Plot
fig, ax = plt.subplots()
df.plot(kind='barh', stacked=False, legend=None, ax=ax)
# plt.xlabel('Depreciation')
plt.xticks(rotation=45)
plt.title('Depreciation by Feature in $')
plt.tight_layout()

# Add the data value on each bar
for i in range(len(df.index)):
    ax.text(df.iloc[i], i, 
            '%d' % int(df.iloc[i]), 
            ha='center')

st.pyplot(fig)

st.info("""
        Disclaimer: Please note that the content provided herein is a part of Michael Lappert's academic MSc. thesis
        conducted at Berner Fachhochschule (bfh) in Biel, Switzerland. The outcomes presented have not undergone 
        any formal validation process yet, and therefore no assurance regarding their accuracy or reliability can be given.
        """)


