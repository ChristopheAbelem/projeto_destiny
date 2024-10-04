import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_excel('destinations.xlsx')
df = df.drop_duplicates()

st.set_page_config(layout='wide')
# Função para classificar o nível de segurança


def classify_safety(value):
    if isinstance(value, str):
        if "Generally safe" in value and "but" not in value:
            return "Alta segurança"
        elif "Generally safe, but" in value:
            return "Média segurança"
    return "Baixa segurança"


df['Safety Level'] = df['Safety'].apply(classify_safety)

# Gráfico de segurança por país
safety_counts = df['Safety Level'].value_counts()
country_safety_counts = df[df['Safety Level'] ==
                           "Alta segurança"]['Country'].value_counts()

st.title('Análise de Destinos Europeus')

# Primeira linha de colunas (3 gráficos)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Países com mais destinos seguros')
    fig, ax = plt.subplots(figsize=(5, 5))
    country_safety_counts.plot(kind='bar', color='green', ax=ax)
    plt.xlabel('País')
    plt.ylabel('Número de Destinos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Função para classificar o custo de vida


def classify_cost_of_living(value):
    if isinstance(value, str):
        if "Extremely high" in value:
            return "Extremely high"
        elif "High" in value:
            return "High"
        elif "Medium-high" in value:
            return "Medium-high"
        elif "Medium" in value:
            return "Medium"
        elif "Free" in value:
            return "Free"
    return "Unknown"


df['Cost of Living Level'] = df['Cost of Living'].apply(
    classify_cost_of_living)

# Gráfico de custo de vida por país
high_cost_countries = df[df['Cost of Living Level'].isin(
    ["Extremely high", "High"])]['Country'].value_counts()

with col2:
    st.subheader('Países com o Maior Custo de Vida')
    fig, ax = plt.subplots(figsize=(5, 5))
    high_cost_countries.plot(kind='bar', color='purple', ax=ax)
    plt.xlabel('País')
    plt.ylabel('Número de Destinos com Custo de Vida Alto')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Análise de religião
religion_counts = df['Majority Religion'].value_counts()
with col3:
    st.subheader('Distribuição de Destinos por Religião Predominante')
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.pie(religion_counts, labels=religion_counts.index,
            autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(fig, use_container_width=True)

# Segunda linha de colunas (3 gráficos)
col4, col5, col6, col7 = st.columns(4)

# Análise de comidas famosas
famous_foods_clean = df['Famous Foods'].dropna()
food_counter = {}

for food in famous_foods_clean:
    foods = [f.strip() for f in food.split(',')]
    for f in foods:
        if f in food_counter:
            food_counter[f] += 1
        else:
            food_counter[f] = 1

top_5_foods = sorted(food_counter.items(),
                     key=lambda x: x[1], reverse=True)[:5]
foods = [item[0] for item in top_5_foods]
counts = [item[1] for item in top_5_foods]

with col4:
    st.subheader('Top 5 Comidas Mais Famosas')
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.barh(foods, counts, color='skyblue')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Análise de idiomas
language_counts = df['Language'].value_counts()
top_languages = language_counts.head(5)

with col5:
    st.subheader('Top 5 Línguas Mais Comuns em Destinos Turísticos')
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.bar(top_languages.index, top_languages.values, color='lightgreen')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Substituição do gráfico "Top 10 Destinos Mais Visitados"
df_cleaned = df.dropna(subset=['Approximate Annual Tourists'])


def convert_to_numeric(value):
    if isinstance(value, str):
        value = value.strip()
        if not all(c.isdigit() or c in [' ', 'm', 'M', 'i', 'I', 'l', 'L', 'o', 'O', 'n', 'N', '-', ',', '(', ')'] for c in value):
            return None
        if 'million' in value:
            value = value.replace('million', '').strip()
            value = value.replace(',', '')
            if '-' in value:
                value = value.split('-')[-1].strip()
            return float(value) * 1_000_000
        else:
            value = value.replace(',', '')
            return float(value)
    try:
        return float(value)
    except ValueError:
        return None


df_cleaned['Approximate Annual Tourists'] = df_cleaned['Approximate Annual Tourists'].apply(
    convert_to_numeric)
df_cleaned = df_cleaned.dropna(subset=['Approximate Annual Tourists'])

tourist_counts = df_cleaned.groupby(['Destination', 'Country'])[
    'Approximate Annual Tourists'].sum().reset_index()
top_destinations = tourist_counts.sort_values(
    by='Approximate Annual Tourists', ascending=False).head(10)

total_tourists = top_destinations['Approximate Annual Tourists'].sum()
top_destinations['Percentage'] = (
    top_destinations['Approximate Annual Tourists'] / total_tourists) * 100

country_colors = {
    'France': 'skyblue',
    'United Kingdom': 'pink',
    'Turkey': 'purple',
    'Italy': 'lightcoral',
    'Germany': 'lightgreen',
    'Spain': 'lightsalmon',
    'Russia': 'brown',
}

with col6:
    st.subheader('Top 10 Destinos Mais Visitados')
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = plt.bar(top_destinations['Destination'], top_destinations['Approximate Annual Tourists'], color=[
                   country_colors.get(country, 'grey') for country in top_destinations['Country']])

    plt.title('Top 10 Most Visited Destinations')
    plt.xlabel('Destination')
    plt.ylabel('Approximate Annual Tourists')

    sorted_countries = top_destinations.groupby(
        'Country')['Percentage'].first().reset_index()
    sorted_countries = sorted_countries.sort_values(
        by='Percentage', ascending=False)

    legend_labels = [f"{row['Country']} ({
        row['Percentage']:.2f}%)" for _, row in sorted_countries.iterrows()]
    handles = [plt.Rectangle((0, 0), 1, 1, color=country_colors.get(
        country, 'grey')) for country in sorted_countries['Country']]

    plt.legend(handles, legend_labels, title='Countries',
               loc='upper left', bbox_to_anchor=(1, 1))

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)


# Análise de categorias de destinos mais visitados
category_counts = df_cleaned.groupby(
    'Category')['Approximate Annual Tourists'].sum().reset_index()
top_categories = category_counts.sort_values(
    by='Approximate Annual Tourists', ascending=False).head(5)

with col7:
    st.subheader('Top 5 Categorias Mais Visitadas')
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.bar(top_categories['Category'],
            top_categories['Approximate Annual Tourists'], color='lightblue')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
