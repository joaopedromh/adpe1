import pandas as pd
import matplotlib
import seaborn as sea


# definir dataframe

df = pd.read_csv('amazon_delivery.csv')

print(f"Dataset: {df.shape[0]} linhas e {df.shape[1]} colunas")

# análise exploratória

print(df.info())
print(df.head())
print(df.describe())


# verificando valores nulos

print("Valores vazios por coluna")
print("-"*40)

missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100 

# cria dataframe para valores nulos
missing_df = pd.DataFrame({
    'Valores ausentes (soma)' : missing_values,
    'Percentual' : missing_percentage
})


print(missing_df[missing_df['Valores ausentes (soma)'] > 0])
if missing_df['Valores ausentes (soma)'].sum() == 0:
    print("Nenhum valor ausente encontrado!")
print()


# verificar tempos de entrega muito baixos

delivery_outlier = df[df['Delivery_Time'] < 15].shape[0]
print(f'Pedidos com tempo de entrega menor que 10 minutos: {delivery_outlier} ({delivery_outlier/len(df)*100:.2f}%)')

# limpeza de dados

# criar um DF secundário para tratar

df_clean = df.copy()

# Agent_Rating nulos

missing_rating = df_clean[df_clean('Agent_Rating').isnull()]


