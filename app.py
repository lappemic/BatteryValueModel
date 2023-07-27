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
fastcharge_events = st.sidebar.slider("Fastcharge Events [Nr.]", 0, 500, 200)
time_low_temp = st.sidebar.slider("Time <10°C [h]", 0, 100, 10)
time_deep_discharge = st.sidebar.slider("Time <40% State of Charge (SOC) [h]", 0, 100, 10)

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
soh_dep = battery_value_after_vat - battery_value_after_vat * model.f_soh(soh)
warranty_time_dep = battery_value_after_vat - battery_value_after_vat * model.f_warranty_time(t)
warranty_distance_dep = battery_value_after_vat - battery_value_after_vat * model.f_warranty_distance(km)
fastcharge_dep = battery_value_after_vat - battery_value_after_vat * model.f_fastcharge(fastcharge_events)
time_low_temp_dep = battery_value_after_vat - battery_value_after_vat * model.f_low_temp(time_low_temp)
time_deep_discharge_dep = battery_value_after_vat - battery_value_after_vat * model.f_deep_discharge(time_deep_discharge)

features = ['SOH', 'Warranty Time', 'Warranty Distance', 'Fastcharge', 'Time <10°C', 'Time <40% SOC']
depreciations = [
    soh_dep,
    warranty_time_dep,
    warranty_distance_dep,
    fastcharge_dep,
    time_low_temp_dep,
    time_deep_discharge_dep
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


