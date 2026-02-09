import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


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

# verificação de limpeza dos dados
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

#criar períodos do dia

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

#criar coluna order_hour
df_clean['Time_Period'] = df_clean['Order_Hour'].apply(get_time_period)

# verificar resultados

print("resultados após tratamento")
print(df_clean[['Order_DateTime', 'Order_Weekday', 'Order_Hour', 'Time_Period']].head())


# analise de distribuição

# veiculos mais utilizados
plt.figure(figsize=(8, 5))
ax = sns.countplot(
    x='Vehicle',
    data=df_clean,
    order=df_clean['Vehicle'].value_counts().index,
    palette='Set2'
)

# Adicionar porcentagens
total = len(df_clean)
for p in ax.patches:
    percentage = f'{100 * p.get_height() / total:.1f}%'
    ax.annotate(percentage, 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom')

plt.title('Distribuição de Veículos')
plt.xlabel('')
plt.ylabel('Número de Entregas')
#plt.show()

# areas mais comuns
plt.figure(figsize=(8, 5))
ax = sns.countplot(
    x='Area',
    data=df_clean,
    order=df_clean['Area'].value_counts().index,
    palette='Set3'
)

for p in ax.patches:
    percentage = f'{100 * p.get_height() / total:.1f}%'
    ax.annotate(percentage, 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom')

plt.title('Distribuição por Área')
plt.xlabel('')
plt.ylabel('Número de Entregas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
#plt.show()

# categorias mais vendidas
plt.figure(figsize=(12, 6))
top_10 = df_clean['Category'].value_counts().nlargest(10)
ax = sns.barplot(
    x=top_10.values,
    y=top_10.index,
    palette='crest'
)

# Adicionar valores
for i, v in enumerate(top_10.values):
    percentage = f'{100 * v / total:.1f}%'
    ax.text(v + 3, i, f'{v} ({percentage})', va='center')

plt.title('Top 10 Categorias de Produtos')
plt.xlabel('Número de Entregas')
plt.ylabel('')
plt.tight_layout()
#plt.show()


### observa-se que:
# uso de motos é mais frequente com 58.5%
# area principal de entrega são as metropolitanas com 74.8%
# os 3 principais produtos são eletronicos, livros e joias


# correlação das notas dos agentes

sns.set_style('whitegrid')
plt.figure(figsize=(15,10))

plt.subplot(2,2,1)

# criar lsita de notas

notas = [0,1,2,3,4,5]
label_nota = ['0-1','1-2', '2-3', '3-4','4-5']

# criar categoria
df_clean['Rating_Group'] = pd.cut(df_clean['Agent_Rating'], bins = notas, labels = label_nota)

rating_time = df_clean.groupby('Rating_Group')['Delivery_Time'].mean().reset_index()

sns.barplot(
    x = 'Rating_Group',
    y = 'Delivery_Time',
    data = df_clean,
    palette = 'viridis'
)

plt.title("Relação de Nota pelo Tempo de Entrega")
plt.xlabel("Nota do Agente")
plt.ylabel("Tempo de Entrega")
plt.xticks(rotation=45)

for i, row in rating_time.iterrows():
    plt.text(i, row['Delivery_Time'] + 1,
             f"{row['Delivery_Time']:.1f}min",
             ha='center', va='bottom')

# Tempo de Entrega x Clima
plt.subplot(2,2,2)

sns.barplot(
    x = 'Weather',
    y = 'Delivery_Time',
    data = df_clean,
    palette='viridis'
)

plt.title('Tempo de Entrega de Acordo com o Clima')
plt.xlabel('Condição do Clima')
plt.ylabel('Tempo de Entrega')
plt.xticks(rotation=45)
plt.show()







