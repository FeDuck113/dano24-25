import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Чтение данных
df = pd.read_excel('none.xlsx')

# Заполнение пропусков
df['rain.1h'] = df['rain.1h'].fillna(0)
df['snow.1h'] = df['snow.1h'].fillna(0)
df['prec'] = df['rain.1h'] + df['snow.1h']

# Вычисление корреляций
corr_temp_feels = df['temp'].corr(df['feels_like'])
corr_hum_feels = df['humidity'].corr(df['feels_like'])
corr_prec_feels = df['prec'].corr(df['feels_like'])

# Создание DataFrame для корреляций
correlations = pd.DataFrame({
    'Variable': ['Temperature', 'Humidity', 'Precipitation'],
    'Correlation': [corr_temp_feels, corr_hum_feels, corr_prec_feels]
})

# Визуализация
plt.figure(figsize=(8, 5))
sns.barplot(data=correlations, x='Variable', y='Correlation', palette='viridis', hue=None)
plt.axhline(0, color='gray', linewidth=0.8, ls='--')  # линия горизонтального нуля
plt.title('Correlation of Weather Variables with Feels Like Temperature')
plt.ylim(-1, 1)
plt.ylabel('Correlation Coefficient')
plt.xlabel('Weather Variables')
plt.show()
