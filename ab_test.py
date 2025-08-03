import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy.stats import norm
from statsmodels.stats.proportion import proportions_ztest
df = pd.read_csv('ab_data.csv')
print(df.isnull().sum())
print(df.duplicated().sum())
print("\nРаспределение по группам:")
value_counts=df['group'].value_counts()
print(value_counts)
group_a = df[df['group'] == 'control']
group_b = df[df['group'] == 'treatment']
conversion_a = group_a['converted'].mean() * 100
conversion_b = group_b['converted'].mean() * 100
n1 = len(group_a)
n2 = len(group_b)
x1 = group_a['converted'].sum()
x2 = group_b['converted'].sum()
p= (x1 + x2) / (n1 + n2)
z_test =(conversion_a/100 -conversion_b/100) / (numpy.sqrt((p* (1 - p) * (1/n1 + 1/n2) )))
p_value = 2 * (1 - norm.cdf(abs(z_test)))
print(f"Конверсия в A: {conversion_a:.2f}%")
print(f"Конверсия в B: {conversion_b:.2f}%")
print()
print(f"Объединённая доля (p): {p:.4f}")
print(f"Размеры групп: n1={n1}, n2={n2}")
print(f"Z-статистика: {z_test:.3f}")
print (f"p_value: {p_value:.4f}")

groups = ['Control (A)', 'Treatment (B)']
conversions = [round(conversion_a,2), round(conversion_b,2)]
plt.figure(figsize=(8, 5))
plt.bar(groups, conversions, color=['blue', 'green'], alpha=0.7)
plt.errorbar(groups, conversions, fmt='none', color='black', capsize=10)
plt.title('Conversion Rates with 95% Confidence Intervals')
plt.ylabel('Conversion Rate (%)')
plt.ylim(10, 13)

for i, conv in enumerate(conversions):
    plt.text(i, conv + 0.1, f"{conv}%", ha='center')

plt.show()
results = pd.DataFrame({
    'Metric': ['Conversion A', 'Conversion B', 'p-value', 'Total Users'],
    'Value': [round(conversion_a,2),round(conversion_b,2) , p_value, len(df)]
})
results.to_csv('ab_test_results.csv', index=False)


