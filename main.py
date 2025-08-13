import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
dates = pd.date_range(start='2022-01-01', periods=365)
sentiment_scores = np.random.normal(loc=0, scale=1, size=365) #random sentiment scores, normally distributed
engagement_scores = 100 + 50*np.sin(2*np.pi*np.arange(365)/365) + 20*np.random.normal(0,1,365) #seasonal engagement with noise
# Introduce a negative sentiment event
sentiment_scores[100:110] -= 3
# Introduce a positive sentiment event
sentiment_scores[200:210] += 2
data = {'Date': dates, 'Sentiment': sentiment_scores, 'Engagement': engagement_scores}
df = pd.DataFrame(data)
# --- 2. Data Cleaning and Preprocessing ---
# Smoothing the data using Savitzky-Golay filter to reduce noise
window_length = 7 # Adjust as needed
polyorder = 2 # Adjust as needed
df['Smoothed_Sentiment'] = savgol_filter(df['Sentiment'], window_length, polyorder)
df['Smoothed_Engagement'] = savgol_filter(df['Engagement'], window_length, polyorder)
# --- 3. Analysis ---
# Calculate rolling average of sentiment and engagement
rolling_window = 30
df['Rolling_Sentiment'] = df['Smoothed_Sentiment'].rolling(window=rolling_window).mean()
df['Rolling_Engagement'] = df['Smoothed_Engagement'].rolling(window=rolling_window).mean()
#Correlation analysis
correlation = df['Rolling_Sentiment'].corr(df['Rolling_Engagement'])
print(f"Correlation between rolling sentiment and engagement: {correlation:.2f}")
# --- 4. Visualization ---
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Rolling_Sentiment'], label='Rolling Sentiment')
plt.plot(df['Date'], df['Rolling_Engagement'], label='Rolling Engagement')
plt.xlabel('Date')
plt.ylabel('Score')
plt.title('Brand Sentiment and Engagement Trajectory')
plt.legend()
plt.grid(True)
plt.tight_layout()
output_filename = 'sentiment_engagement_trajectory.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")
plt.figure(figsize=(10,6))
sns.regplot(x='Rolling_Sentiment', y='Rolling_Engagement', data=df, scatter_kws={'alpha':0.5})
plt.xlabel("Rolling Average Sentiment")
plt.ylabel("Rolling Average Engagement")
plt.title("Sentiment vs Engagement (Rolling Average)")
output_filename2 = 'sentiment_engagement_correlation.png'
plt.savefig(output_filename2)
print(f"Plot saved to {output_filename2}")