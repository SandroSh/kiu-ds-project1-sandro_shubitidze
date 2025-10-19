import numpy as np

# Not fully completed, activity levels by steps is not implemented

np.random.seed(42)

n_users = 100
n_days = 90
n_metrics = 4 

# Generate realistic data
daily_steps = np.random.randint(2000, 15001, size=(n_users, n_days))
calories = np.random.randint(1500, 3501, size=(n_users, n_days))
active_minutes = np.random.randint(20, 181, size=(n_users, n_days))
avg_heart_rate = np.random.randint(60, 121, size=(n_users, n_days))

# Combine metrics 
data = np.stack([daily_steps, calories, active_minutes, avg_heart_rate], axis=2)

#  NaNs 
nan_mask = np.random.rand(*data.shape) < 0.05
data = data.astype(float)
data[nan_mask] = np.nan

#  outliers 
outlier_mask = np.random.rand(*data.shape) < 0.02
data[outlier_mask] *= 10 

# User metadata
user_metadata = np.zeros((n_users, 3))
user_metadata[:, 0] = np.arange(1, n_users+1)  
user_metadata[:, 1] = np.random.randint(18, 71, size=n_users)  
user_metadata[:, 2] = np.random.randint(0, 2, size=n_users)  



def handle_missing(data):
    # Replace NaN 
    for m in range(data.shape[2]):
        col_mean = np.nanmean(data[:, :, m])
        nan_idx = np.isnan(data[:, :, m])
        data[nan_idx, m] = col_mean if np.isscalar(col_mean) else col_mean
    return data

def remove_outliers(data, metric_index):
    metric_data = data[:, :, metric_index]
    Q1 = np.percentile(metric_data, 25)
    Q3 = np.percentile(metric_data, 75)
    IQR = Q3 - Q1
    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR
    outliers = (metric_data < low) | (metric_data > high)
    median = np.median(metric_data)
    metric_data[outliers] = median
    data[:, :, metric_index] = metric_data
    return data

for m in range(n_metrics):
    data = remove_outliers(data, m)
data = handle_missing(data)



# metrics per user
avg_metrics_per_user = data.mean(axis=1)

# Z-score for all metrics per user
z_scores = (avg_metrics_per_user - avg_metrics_per_user.mean(axis=0)) / avg_metrics_per_user.std(axis=0)
combined_z = z_scores.sum(axis=1)
top_10_users = np.argsort(-combined_z)[:10]

# Users with lowest std deviation
user_std = data.std(axis=1).sum(axis=1)
most_consistent_users = np.argsort(user_std)[:10]



# 7-day rolling averages for population metrics
rolling_avg = np.array([
    np.convolve(data[:, :, m].mean(axis=0), np.ones(7)/7, mode='valid')
    for m in range(n_metrics)
]).T

# Correlation matrix 
corr_matrix = np.corrcoef(data.reshape(-1, n_metrics).T)

# Goal achievement
steps_goal = 8000
calories_goal = 2000
active_minutes_goal = 60
goal_mask = (data[:, :, 0] >= steps_goal) & (data[:, :, 1] >= calories_goal) & (data[:, :, 2] >= active_minutes_goal)
goal_achievement_rate = goal_mask.sum(axis=1) / n_days * 100
consistent_goal_users = np.where(goal_achievement_rate > 80)[0]


print("=== Fitness Tracker Report ===\n")
print("Top 10 most active users:", top_10_users + 1)
print("Most consistent users:", most_consistent_users + 1)
print("Correlation matrix between metrics:\n", corr_matrix)
print("Number of users consistently meeting all goals (>80% days):", len(consistent_goal_users))
