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
print(f'Pedidos com tempo de entrega menor que 15 minutos: {delivery_outlier} ({delivery_outlier/len(df)*100:.2f}%)')

# limpeza de dados

# criar um DF secundário para tratar

df_clean = df.copy()

# remover nulos

df_clean = df_clean.dropna()

rows_cleaned = df.shape[0] - df_clean.shape[0]
percentage_cleaned = (rows_cleaned / df.shape[0]) * 100
print(f"deletadas {rows_cleaned} linhas, totalizando um percentual de {percentage_cleaned:.2f}%")


# tratamento das datas

df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'], format = '%Y-%m-%d')
df_clean['Order_Time'] = pd.to_datetime(df_clean['Order_Time'], format = '%H:%M:%S')
df_clean['Pickup_Time'] = pd.to_datetime(df_clean['Pickup_Time'], format = '%H:%M:%S')

df_clean['Order_DateTime'] = pd.to_datetime(
    df_clean['Order_Date'].astype(str) + ' ' + df_clean['Order_Time'].astype(str)
    )

# dt.dayofweek : Monday=0, Sunday=6.
df_clean['Order_Weekday'] = df_clean['Order_DateTime'].dt.dayofweek

# hora do dia
df_clean['Order_Hour'] = df_clean['Order_DateTime'].dt.hour

# determinar periodo do dia

def get_time_period(hour):
    if 5 <= hour < 12:
        return 'Manha'
    elif 12 <= hour < 18:
        return 'Tarde'
    elif 18 <= hour < 23:
        return 'Noite'
    else:
        'Madrugada'

df_clean['Time_Period'] = df_clean['Order_Hour'].apply(get_time_period)

# verificar resultados

print("resultados após tratamento")
print(df_clean[['Order_DateTime', 'Order_Weekday', 'Order_Hour', 'Time_Period']].head())






