from typing import Any
import numpy as np

random_generator = np.random.default_rng(42)
np.random.seed(42)


temperature_data = random_generator.uniform(-10.0, 40.0, size=(365, 5))
identity_matrix = np.eye(5)
evenly_spaced = np.linspace(0, 100, 50)
sales_matrix = random_generator.integers(1000, 5000, size=(12, 4))


def print_general_info(temperature_data, identity_matrix, evenly_spaced, sales_matrix):
    print("temperature data:")
    print("shape:", temperature_data.shape)
    print("dimension:", temperature_data.ndim)
    print("data type:", temperature_data.dtype)
    print("size:", temperature_data.size)
    print("\n")
    print("sales matrix:")
    print(sales_matrix)
    print("\n")
    print("identity matrix:")
    print(identity_matrix)
    print()
    print("evenly spaced values from 0 to 100:")
    print(evenly_spaced)

def basic_slicing(temperature_data):
    january_data = temperature_data[:31, :]

    # June-August
    summer_data = temperature_data[152:243, :]
    weekend_data = temperature_data[5::7, :]

    print("January shape:", january_data.shape)
    print("Summer shape:", summer_data.shape)
    print("Weekend shape:", weekend_data.shape)

def boolean_indexing(
    temperature_data: np.ndarray[tuple[Any, ...], np.dtype[np.float64]],
):
    high_temp_dates = (temperature_data > 35).any(axis=1)
    print(temperature_data[high_temp_dates])

    low_temp_date_quantity = (temperature_data < 0).sum(axis=0)

    average_temp = (temperature_data >= 15) & (temperature_data <= 25)

    temperature_data_cleaned = temperature_data.copy()
    temperature_data_cleaned[temperature_data_cleaned < -5] = -5
    
    print(average_temp)
    print(low_temp_date_quantity)
    print(temperature_data_cleaned)

def indexing(temperature_data: np.ndarray[tuple[Any, ...], np.dtype[np.float64]]):
    # Specific days
    specific_days_idx = np.array([0, 1, 97, 150, 310])
    specific_days_data = temperature_data[specific_days_idx, :]
    print("Data for specific days:")
    print(specific_days_data)
    
    #  Quarterlt averages
    quarters = [
        temperature_data[0:91, :],  
        temperature_data[91:182, :],  
        temperature_data[182:274, :],  
        temperature_data[274:365, :],  
    ]
    quarterly_averages = np.array([q.mean(axis=0) for q in quarters])
    print("Quarterly averages:\n", quarterly_averages)

    # Rearange cities by annual average temperature
    annual_avg_per_city = temperature_data.mean(axis=0)
    sorted_city_indexes = np.argsort(-annual_avg_per_city)  

    print("Annual average per city:", annual_avg_per_city)
    print("Sorted city indices (desc):", sorted_city_indexes)
    
def temperature_analysis(temperature_data: np.ndarray[tuple[Any, ...], np.dtype[np.float64]]):
    mean_per_city = temperature_data.mean(axis=0)
    median_per_city = np.median(temperature_data, axis=0)
    std_per_city = temperature_data.std(axis=0)
    
    print("Mean per city:", mean_per_city)
    print("Median per city:", median_per_city)
    print("Std deviation per city:", std_per_city)  
    
    hottest_day_idx = np.argmax(temperature_data.max(axis=1))
    hottest_day_temp = temperature_data[hottest_day_idx].max()
    print(f"Hottest day: Day {hottest_day_idx}, Temperature: {hottest_day_temp:.2f}")

    coldest_day_idx = np.argmin(temperature_data.min(axis=1))
    coldest_day_temp = temperature_data[coldest_day_idx].min()
    print(f"Coldest day: Day {coldest_day_idx}, Temperature: {coldest_day_temp:.2f}")
    
    correlation_matrix = np.corrcoef(temperature_data.T)
    print("Correlation between cities:\n", correlation_matrix)
    
def sales_analysis(sales_matrix: np.ndarray[tuple[Any, ...], np.dtype[np.float64]]):

    total_sales_per_product = sales_matrix.sum(axis=0)
    print("Total sales:", total_sales_per_product)

  
    avg_sales_per_product = sales_matrix.mean(axis=0)
    print("Average sales:", avg_sales_per_product)

    # 3) Best performing month 
    total_sales_per_month = sales_matrix.sum(axis=1)
    best_month_idx = np.argmax(total_sales_per_month)
    print( best_month_idx)
    print( total_sales_per_month[best_month_idx])

    # 4) Best performing category
    best_product_idx = np.argmax(total_sales_per_product)
    print("Best performing index", best_product_idx)
    print("Total sales of that product:", total_sales_per_product[best_product_idx])
    
    
def advanced_computations(temperature_data: np.ndarray[tuple[Any, ...], np.dtype[np.float64]]):
    window_size = 7
    moving_avg = np.array([
        np.convolve(temperature_data[:, i], np.ones(window_size)/window_size, mode='valid')
        for i in range(temperature_data.shape[1])
    ]).T  

    print("7-day moving average shape:", moving_avg.shape)

    # 2) Compute z-scores for each  temperatures
    mean_per_city = temperature_data.mean(axis=0)
    std_per_city = temperature_data.std(axis=0)
    z_scores = (temperature_data - mean_per_city) / std_per_city

    print("Z-scores shape:", z_scores.shape)

    # 3) Percentiles (25th, 50th, 75th) 
    percentiles = np.percentile(temperature_data, [25, 50, 75], axis=0)
    print("Percentiles (25th, 50th, 75th):\n", percentiles)
    
def main():
    print_general_info(temperature_data, identity_matrix, evenly_spaced, sales_matrix)
    basic_slicing(temperature_data)
    boolean_indexing(temperature_data)
    indexing(temperature_data)
    temperature_analysis(temperature_data)
    sales_analysis(sales_matrix)
    advanced_computations(temperature_data)
    
    
if __name__ == '__main__':
    main()