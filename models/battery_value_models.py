import pandas as pd
import numpy as np

class SimpleBatteryValueModel:
    def __init__(self, base_depreciation_rate, vat_rate, warranty_period, warranty_distance, warranty_base_ratio, battery_to_ev_value_ratio): # , power
        # self.original_price = original_price
        self.base_depreciation_rate = base_depreciation_rate
        # self.power = power # REMARK: power could also be removed - just to strengthen the effect
        self.vat_rate = vat_rate
        self.warranty_period = warranty_period
        self.warranty_distance = warranty_distance
        # the value of the battery should not decrease to 0 because of the warranty expiration - setting minimal value
        self.warranty_base_ratio = warranty_base_ratio
        self.battery_to_ev_value_ratio = battery_to_ev_value_ratio
        
    def f_vat(self, vat_rate):
        # initial price of the ev gets reduced immadiately by the vat after purchase
        return (100-vat_rate)/100

    def f_soh(self, soh):
        # exponential function (and a power term) to model a steeper decline in value
        return np.exp(-self.base_depreciation_rate * (1 - soh)) # ** self.power

    def f_warranty_time(self, t):
        # function that calculates the proportional value of warranty with respect to time
        # return max(self.warranty_base_ratio, 1 - min(1, t / self.warranty_period))
        # ALTERNATIVE: logistic regression function to flatten out value decrese over time
        return 1 / (1 + np.exp(-10*(1 - t/self.warranty_period))) * (1-self.warranty_base_ratio) + self.warranty_base_ratio
        
    def f_warranty_distance(self, km):
        # function that calculates the proportional value of warranty with respect to distance
        # return max(self.warranty_base_ratio, 1 - min(1, km / self.warranty_distance))
        # ALTERNATIVE: logistic regression function to flatten out value decrese over distance
        return 1 / (1 + np.exp(-10*(1 - km/self.warranty_distance))) * (1-self.warranty_base_ratio) + self.warranty_base_ratio

    def remaining_value(self, original_price, soh, t, km):
        return original_price * self.battery_to_ev_value_ratio * self.f_vat(self.vat_rate) * self.f_soh(soh) * self.f_warranty_time(t) * self.f_warranty_distance(km)

class AdvancedBatteryValueModel(SimpleBatteryValueModel):
    def __init__(self, base_depreciation_rate, vat_rate, warranty_period, warranty_distance, warranty_base_ratio, battery_to_ev_value_ratio, fastcharge_penalty, temp_penalty, deep_discharge_penalty):
        super().__init__(base_depreciation_rate, vat_rate, warranty_period, warranty_distance, warranty_base_ratio, battery_to_ev_value_ratio)
        self.fastcharge_penalty = fastcharge_penalty
        self.temp_penalty = temp_penalty
        self.deep_discharge_penalty = deep_discharge_penalty

    def f_fastcharge(self, fastcharge_events):
        return np.exp(-self.fastcharge_penalty * np.sqrt(fastcharge_events))

    def f_temp(self, time_above_40C):
        return np.exp(-self.temp_penalty * time_above_40C)

    def f_deep_discharge(self, time_below_40_discharge):
        return np.exp(-self.deep_discharge_penalty * time_below_40_discharge)

    def remaining_value(self, original_price, soh, t, km, fastcharge_events, time_high_temp, time_deep_discharge):
        return super().remaining_value(original_price, soh, t, km) * self.f_fastcharge(fastcharge_events) * self.f_temp(time_high_temp) * self.f_deep_discharge(time_deep_discharge)

