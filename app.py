import streamlit as st
import numpy as np
import pandas as pd
from models import AdvancedBatteryValueModel
import matplotlib.pyplot as plt
from constants import * # TODO: Import explicitly

# Define the model
model = AdvancedBatteryValueModel()

# Sidebar default setting
st.set_page_config(initial_sidebar_state="expanded")

# Sidebar Inputs
st.sidebar.title("Input Parameters")
# TODO: Adjust model so original price is not necessary anymore
original_price = 50 # st.sidebar.slider("Original Carprice [$]", 25000, 100000, 35000) # REMARK: Quick fix because price is not needed anymore 
soh = st.sidebar.slider("State of Health (SOH)", 0.5, 1.0, 0.8)
t = st.sidebar.slider("Battery Age [years]", 0, AGE_MAX, 3)
km = st.sidebar.slider("Distance Driven [km]", 0, DISTANCE_MAX, 60000)
fastcharge_events = st.sidebar.slider("Fastcharge Events [Nr.]", 0, FASTCHARGE_MAX, 10)
cycles = st.sidebar.slider("Cycles [Nr.]", 0, CYCLES_MAX, 500)
time_low_temp = st.sidebar.slider("Time <10°C [h]", 0, TIME_LOW_TEMP_MAX, 10)
time_charging = st.sidebar.slider("Time charging [h]", 0, TIME_CHARGING_MAX, 2000)
time_deep_discharge = st.sidebar.slider("Time <12.5% State of Charge (SOC) [h]", 0, TIME_DEEP_DISCHARGE_MAX, 10)

# Calculate remaining value
remaining_value = model.remaining_value(original_price, 
                                        soh, 
                                        t, 
                                        km, 
                                        fastcharge_events, 
                                        cycles,
                                        time_low_temp, 
                                        time_charging,
                                        time_deep_discharge)

# Display result
battery_value = original_price*BATTERY_TO_EV_VALUE_RATIO
battery_value_after_vat = battery_value * model.f_vat(VAT_RATE)
st.title("Calculate easily the Remaining Value of your EV battery")
st.write(f"The normalized remaining value of the battery with the given input parameters is {remaining_value:,.2f} from the cars original value.")
st.write(f"The following diagram shows how much each feature contributes to the value depreciation of the batteries value")

# Calculate depreciation caused by each feature
soh_dep = (battery_value_after_vat - battery_value_after_vat * model.f_soh(soh)) / battery_value_after_vat
warranty_time_dep = (battery_value_after_vat - battery_value_after_vat * model.f_warranty_time(t)) / battery_value_after_vat
warranty_distance_dep = (battery_value_after_vat - battery_value_after_vat * model.f_warranty_distance(km)) / battery_value_after_vat
fastcharge_dep = (battery_value_after_vat - battery_value_after_vat * model.f_fastcharge(fastcharge_events)) / battery_value_after_vat
cycles_dep = (battery_value_after_vat - battery_value_after_vat * model.f_cycles(cycles)) / battery_value_after_vat
time_low_temp_dep = (battery_value_after_vat - battery_value_after_vat * model.f_low_temp(time_low_temp)) / battery_value_after_vat
time_charging_dep = (battery_value_after_vat - battery_value_after_vat * model.f_time_charging(time_charging)) /battery_value_after_vat
time_deep_discharge_dep = (battery_value_after_vat - battery_value_after_vat * model.f_deep_discharge(time_deep_discharge)) / battery_value_after_vat

features = ['SOH', 'Warranty Time', 'Warranty Distance', 'Fastcharge', 'Cycles', 'Time <10°C', 'Time charging', 'Time <12.5% SOC']
depreciations = [
    soh_dep,
    warranty_time_dep,
    warranty_distance_dep,
    fastcharge_dep,
    cycles_dep,
    time_low_temp_dep,
    time_charging_dep,
    time_deep_discharge_dep
    ]

# Create a DataFrame for plotting
df = pd.DataFrame(list(zip(features, depreciations)), columns=['Feature', 'Depreciation'])
df = df.set_index('Feature')
df = df.iloc[::-1]

# Plot
fig, ax = plt.subplots()
df.plot(kind='barh', stacked=False, legend=None, ax=ax)
plt.ylabel('')
plt.xticks(rotation=45)
plt.title('Normalized Battery Value Depreciation by Feature')
plt.tight_layout()

st.pyplot(fig)

st.info("""
        Info: "Warranty Time" is derived from the battery's age and "Warranty Distance" is derived from the distance driven with the battery.
        """)

st.info("""
        Disclaimer: Please note that the content provided herein is a part of Michael Lappert's academic MSc. thesis
        conducted at Berner Fachhochschule (bfh) in Biel, Switzerland. The outcomes presented have not undergone 
        any formal validation process yet, and therefore no assurance regarding their accuracy or reliability can be given.
        """)


