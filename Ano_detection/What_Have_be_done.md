# NASA CMAPSS Engine Data Summary

## Dataset Overview

The NASA CMAPSS dataset consists of multivariate time series data from simulated aircraft engines. Each dataset (FD001–FD004) contains data from multiple engines (units), with each engine represented by a time series of operational cycles. The data is split into training and test sets:

- **Training set:** Each engine runs until failure.
- **Test set:** Each engine runs for a period before failure; the Remaining Useful Life (RUL) is provided separately.

<!-- ### Data Structure -->
- Each row: Snapshot of an engine at a specific cycle
- **Columns:**
  1. Unit number (engine ID)
  2. Time in cycles
  3. Operational setting 1
  4. Operational setting 2
  5. Operational setting 3
  6–26. Sensor measurements 1–26

### Datasets
- **FD001:** 100 train/test engines, 1 condition, 1 fault mode
- **FD002:** 260/259 train/test engines, 6 conditions, 1 fault mode
- **FD003:** 100 train/test engines, 1 condition, 2 fault modes
- **FD004:** 248/249 train/test engines, 6 conditions, 2 fault modes

## Experimental Scenario
- Each engine starts healthy and develops faults over time.
- Sensor readings and operational settings are provided for each cycle.
- The goal: Predict the Remaining Useful Life (RUL) for each engine in the test set.

---

# What have be done

## 1. Data Loading & Preprocessing

- Downloaded NASA CMAPSS FD001 dataset (100 training engines)
- Added proper column names (engine_id, cycle, 3 settings, 21 sensors)
- Applied MinMax normalization to features
- No missing data found

## 2. Statistical Analysis

- **Engine lifespans**: Mean ~206 cycles, range 128-362 cycles
- **Sensor analysis**: Identified constant sensors and correlation patterns
- **Degradation patterns**: Found sensors showing clear degradation over time
- **Health indicators**: Created normalized cycle progression (0=start, 1=failure)

## 3. Feature Engineering

- Created RUL (Remaining Useful Life) target variable
- Added rolling averages and trend features for degradation sensors
- Selected key features showing degradation patterns

## 4. Machine Learning Model

- **Model**: Random Forest Regressor (100 trees)
- **Features**: Degradation sensors + cycle + operational settings
- **Target**: RUL prediction

