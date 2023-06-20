import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from models import AdvancedBatteryValueModel

def main():

    st.title('Advanced Battery Value Model')

    st.sidebar.write('Input parameters to calculate the remaining battery value.')

    # user input
    base_depreciation_rate = st.sidebar.slider('Base Depreciation Rate', min_value=0.0, max_value=1.0, value=0.2)
    vat_rate = st.sidebar.slider('VAT Rate', min_value=0.0, max_value=1.0, value=0.2)
    warranty_period = st.sidebar.slider('Warranty Period', min_value=0, max_value=10, value=3)
    warranty_distance = st.sidebar.slider('Warranty Distance', min_value=0, max_value=200000, value=150000)
    warranty_base_ratio = st.sidebar.slider('Warranty Base Ratio', min_value=0.0, max_value=1.0, value=0.5)
    battery_to_ev_value_ratio = st.sidebar.slider('Battery to EV Value Ratio', min_value=0.0, max_value=1.0, value=0.3)
    fastcharge_penalty = st.sidebar.slider('Fastcharge Penalty', min_value=0.0, max_value=1.0, value=0.05)
    temp_penalty = st.sidebar.slider('Temperature Penalty', min_value=0.0, max_value=1.0, value=0.05)
    deep_discharge_penalty = st.sidebar.slider('Deep Discharge Penalty', min_value=0.0, max_value=1.0, value=0.05)

    # Battery value calculation params
    original_price = st.sidebar.slider('Original Price', min_value=0, max_value=100000, value=50000)
    t = st.sidebar.slider('Time', min_value=0, max_value=10, value=2)
    km = st.sidebar.slider('Distance Covered', min_value=0, max_value=200000, value=60000)
    fastcharge_events = st.sidebar.slider('Fastcharge Events', min_value=0, max_value=1000, value=500)
    time_high_temp = st.sidebar.slider('Time above 40C', min_value=0, max_value=1000, value=500)
    time_deep_discharge = st.sidebar.slider('Time below 40% discharge', min_value=0, max_value=1000, value=500)

    soh_values = np.linspace(0.1, 1, 100)  # SOH range
    remaining_values = []

    model = AdvancedBatteryValueModel(
        base_depreciation_rate=base_depreciation_rate, 
        vat_rate=vat_rate, 
        warranty_period=warranty_period, 
        warranty_distance=warranty_distance,
        warranty_base_ratio=warranty_base_ratio,
        battery_to_ev_value_ratio=battery_to_ev_value_ratio,
        fastcharge_penalty=fastcharge_penalty, 
        temp_penalty=temp_penalty, 
        deep_discharge_penalty=deep_discharge_penalty
    )

    for soh in soh_values:
        remaining_value = model.remaining_value(
            original_price=original_price, 
            soh=soh, 
            t=t, 
            km=km, 
            fastcharge_events=fastcharge_events, 
            time_high_temp=time_high_temp, 
            time_deep_discharge=time_deep_discharge
        )
        remaining_values.append(remaining_value)

    fig, ax = plt.subplots()
    ax.plot(soh_values, remaining_values)
    ax.set_xlabel('SOH')
    ax.set_ylabel('Remaining Value')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
