import pandas as pd
from scipy import stats

file1 = 'file1.xlsx'
file2 = 'file2.xlsx'

data1 = pd.read_excel(file1)
data2 = pd.read_excel(file2)

# Приведение к числовому типу и удаление NaN
data1['finish_time'] = pd.to_numeric(data1['finish_time'], errors='coerce')
data2['finish_time'] = pd.to_numeric(data2['finish_time'], errors='coerce')
data1 = data1.dropna(subset=['finish_time'])
data2 = data2.dropna(subset=['finish_time'])

# Удаление NaN в столбцах признаков
features = ['temp', 'humidity', 'dew_point', 'precipitation']
for col in features:
    data1 = data1.dropna(subset=[col])
    data2 = data2.dropna(subset=[col])

data1['source'] = 'group1'
data2['source'] = 'group2'
combined_data = pd.concat([data1, data2], ignore_index=True)

# Создание категорий для других признаков
binned_columns = {
    'temp': [-float('inf'), 0, 10, 20, float('inf')],
    'humidity': [0, 30, 60, 100],
    'dew_point': [-float('inf'), 0, 10, float('inf')],
    'precipitation': [-float('inf'), 0, 10, float('inf')]
}

results_summary = []

# Обработка других признаков
for column, bins in binned_columns.items():
    combined_data[f'{column}_category'] = pd.cut(combined_data[column], bins=bins)

    for value in combined_data[f'{column}_category'].unique():
        group1 = combined_data[(combined_data['source'] == 'group1') & (combined_data[f'{column}_category'] == value)][
            'finish_time']
        group2 = combined_data[(combined_data['source'] == 'group2') & (combined_data[f'{column}_category'] == value)][
            'finish_time']

        if not group1.empty and not group2.empty:
            # Проверка на нормальность
            if len(group1) > 3 and len(group2) > 3:
                stat1, p1 = stats.shapiro(group1)
                stat2, p2 = stats.shapiro(group2)
                normal1 = p1 >= 0.05  # Нормальность для group1
                normal2 = p2 >= 0.05  # Нормальность для group2
            else:
                normal1 = normal2 = True

            # Выполнение t-теста
            if normal1 and normal2:
                t_statistic, p_value = stats.ttest_ind(group1, group2)
            else:
                t_statistic, p_value = stats.mannwhitneyu(group1, group2)

            effect_size = abs(group1.mean() - group2.mean()) / (
                group1.std() + group2.std() if (group1.std() + group2.std()) != 0 else 1)
            alpha = 0.05
            significant = p_value < alpha

            results_summary.append({
                'variable': column,
                'binned_value': str(value),
                'p_value': p_value,
                'significant': significant
            })

# Обработка столбца track_description_surface
surface_groups = combined_data.groupby('track_description_surface')

for surface, group in surface_groups:
    group1 = group[group['source'] == 'group1']['finish_time']
    group2 = group[group['source'] == 'group2']['finish_time']

    if not group1.empty and not group2.empty:
        if len(group1) > 3 and len(group2) > 3:
            stat1, p1 = stats.shapiro(group1)
            stat2, p2 = stats.shapiro(group2)
            normal1 = p1 >= 0.05  # Нормальность для group1
            normal2 = p2 >= 0.05  # Нормальность для group2
        else:
            normal1 = normal2 = True

        # Выполнение t-теста
        if normal1 and normal2:
            t_statistic, p_value = stats.ttest_ind(group1, group2)
        else:
            t_statistic, p_value = stats.mannwhitneyu(group1, group2)

        effect_size = abs(group1.mean() - group2.mean()) / (
            group1.std() + group2.std() if (group1.std() + group2.std()) != 0 else 1)
        alpha = 0.05
        significant = p_value < alpha

        results_summary.append({
            'variable': 'track_description_surface',
            'binned_value': surface,
            'p_value': p_value,
            'significant': significant
        })

# Создание датафрейма для результатов
results_df = pd.DataFrame(results_summary)

# Вывод результата в требуемом формате
print("\nРезультаты сравнения:\n")
print(results_df[['variable', 'binned_value', 'p_value', 'significant']])





