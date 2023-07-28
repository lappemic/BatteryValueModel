import pandas as pd
import numpy as np

from constants import *


class SimpleBatteryValueModel:
    def __init__(self, base_depreciation_rate, vat_rate, warranty_period, warranty_distance, warranty_base_ratio, battery_to_ev_value_ratio): # , power
        # base_depreciation_rate describes average rate at which the battery value depreciates
        self.base_depreciation_rate = base_depreciation_rate
        # VAT rate is also the same per country - to reduce confusions for user this should be preset per country
        self.vat_rate = vat_rate
        # how long does the manufacturer give warranty to the battery (time- and distancewise)
        # - assumed to be constant for every manufactuerer - no user setting
        self.warranty_period = warranty_period
        self.warranty_distance = warranty_distance
        # the value of the battery should not decrease to 0 because of the warranty expiration - setting minimal value
        self.warranty_base_ratio = warranty_base_ratio
        self.battery_to_ev_value_ratio = battery_to_ev_value_ratio
        
    def f_vat(self, vat_rate):
        # initial price of the ev gets reduced immadiately by the vat after purchase
        return 1-vat_rate

    def f_soh(self, soh):
        # Exponential function to model a steeper decline in value
        return np.exp(-self.base_depreciation_rate * (1 - soh)) 

    def f_warranty_time(self, t):
        # Logistic regression function to flatten out value decrese over time
        # TODO: Check options to mitigate if statement
        if t == 0:
            return 1
        else:
            return 1 / (1 + np.exp(-10*(1 - t/self.warranty_period))) * (1-self.warranty_base_ratio) + self.warranty_base_ratio
        
    def f_warranty_distance(self, km):
        # Logistic regression function to flatten out value decrese over distance
        # TODO: Check options to mitigate if statement
        if km == 0:
            return 1
        else:
            return 1 / (1 + np.exp(-5*(1 - km/self.warranty_distance))) * (1-self.warranty_base_ratio) + self.warranty_base_ratio

    def remaining_value(self, original_price, soh, t, km):
        # Combining all functions to get the final remaaining value of the battery
        remaining_value=  max(
            original_price * MIN_BATTERY_VALUE_RATIO,
            original_price * self.battery_to_ev_value_ratio * self.f_vat(self.vat_rate) * self.f_soh(soh) * self.f_warranty_time(t) * self.f_warranty_distance(km)
        )
        
        # Normalize the remaining value to be between 0 and 1 for the return of the SimpleBatteryModel
        remaining_value_normalized = remaining_value / (original_price * BATTERY_TO_EV_VALUE_RATIO)
        
        return remaining_value_normalized, remaining_value

class AdvancedBatteryValueModel(SimpleBatteryValueModel):
    def __init__(self):
        super().__init__(BASE_DEPRECIATION_RATE, VAT_RATE, WARRANTY_PERIOD, WARRANTY_DISTANCE, WARRANTY_BASE_RATIO, BATTERY_TO_EV_VALUE_RATIO)
        self.fastcharge_penalty = FASTCHARGE_PENALTY
        self.temp_penalty = TEMP_PENALTY
        self.deep_discharge_penalty = DEEP_DISCHARGE_PENALTY


    def f_fastcharge(self, fastcharge_events):
        return np.exp(-self.fastcharge_penalty * np.sqrt(fastcharge_events))

    def f_low_temp(self, time_low_temp):
        return np.exp(-self.temp_penalty * time_low_temp)

    def f_deep_discharge(self, time_deep_discharge):
        return np.exp(-self.deep_discharge_penalty * time_deep_discharge)

    def remaining_value(self, original_price, soh, t, km, fastcharge_events, time_low_temp, time_deep_discharge):
        # Combining all functions to get the final remaaining value of the battery        
        remaining_value = max(
            original_price * MIN_BATTERY_VALUE_RATIO,
            super().remaining_value(original_price, soh, t, km)[1] * self.f_fastcharge(fastcharge_events) * self.f_low_temp(time_low_temp) * self.f_deep_discharge(time_deep_discharge)
        )
        
        # Normalize the remaining value to be between 0 and 1
        remaining_value_normalized = remaining_value / (original_price * BATTERY_TO_EV_VALUE_RATIO)
        
        return remaining_value_normalized * BATTERY_TO_EV_VALUE_RATIO
