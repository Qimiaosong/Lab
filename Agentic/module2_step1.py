# LLM output with first draft code
import pandas as pd
import matplotlib.pyplot as plt


# Filter the DataFrame for Q1 of 2024 and 2025
df_q1_2024 = df[(df['year'] == 2024) & (df['quarter'] == 1)]
df_q1_2025 = df[(df['year'] == 2025) & (df['quarter'] == 1)]

# Group by coffee_name and sum the prices for each year
sales_2024 = df_q1_2024.groupby('coffee_name')['price'].sum()
sales_2025 = df_q1_2025.groupby('coffee_name')['price'].sum()

# Create a DataFrame for plotting
sales_comparison = pd.DataFrame({'2024': sales_2024, '2025': sales_2025}).fillna(0)

# Plotting
sales_comparison.plot(kind='bar')
plt.title('Q1 Coffee Sales Comparison (2024 vs 2025)')
plt.xlabel('Coffee Name')
plt.ylabel('Total Sales ($)')
plt.legend(title='Year')

# Save the figure
plt.savefig('chart_v1.png', dpi=300)
plt.close()
