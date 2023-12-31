# Base ratios
BASE_DEPRECIATION_RATE = 0.15
BATTERY_TO_EV_VALUE_RATIO = 0.3
MIN_BATTERY_VALUE_RATIO = 0.025
VAT_RATE = 0.19

# Warranties
WARRANTY_PERIOD = 8
WARRANTY_DISTANCE = 150000
WARRANTY_BASE_RATIO = 0.6

# Penalties
## Derived from the importance of the feature importance analysis of the model
FASTCHARGE_PENALTY = 0.27
CYCLES_PENALTY = 0.13
TEMP_PENALTY = 0.07
TIME_CHARGING_PENALTY = 0.11
DEEP_DISCHARGE_PENALTY = 0.06

# Slidervalues
AGE_MAX = 20
DISTANCE_MAX = 200000
FASTCHARGE_MAX = 100
CYCLES_MAX = 2000
TIME_LOW_TEMP_MAX = 100
TIME_CHARGING_MAX = 8000
TIME_DEEP_DISCHARGE_MAX = 100