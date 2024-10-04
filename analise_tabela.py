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

# Categorias de análise
st.title('Análise de Destinos Europeus')

analysis_category = st.selectbox(
    "Escolha uma categoria de análise:",
    [
        "Ver todos os gráficos",
        "Análise Social",
        "Análise Cultural",
        "Análise Geográfica",
        "Análise Demográfica"
    ]
)

# Função para converter valores para numéricos


def convert_to_numeric(value):
    if isinstance(value, str):
        value = value.strip()
        if 'million' in value.lower():
            value = value.lower().replace('million', '').strip()
            value = value.replace(',', '')
            try:
                return float(value) * 1_000_000
            except ValueError:
                return None  # Retornar None se a conversão falhar
        else:
            value = value.replace(',', '')
            try:
                return float(value)
            except ValueError:
                return None  # Retornar None se a conversão falhar
    return None  # Retornar None para valores não string


# Criar df_cleaned antes de usá-lo
df_cleaned = df.dropna(subset=['Approximate Annual Tourists'])
df_cleaned['Approximate Annual Tourists'] = df_cleaned['Approximate Annual Tourists'].apply(
    convert_to_numeric)
df_cleaned = df_cleaned.dropna(subset=['Approximate Annual Tourists'])

# Mostrar gráficos com base na categoria selecionada
if analysis_category == "Ver todos os gráficos":
    # Gráficos de Análise Social
    st.subheader('Paises com mais destinos seguros')
    safety_counts = df['Safety Level'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    safety_counts.plot(kind='bar', color='green', ax=ax)
    plt.xlabel('Nível de Segurança')
    plt.ylabel('Número de Destinos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    st.subheader('Paises com o Maior Custo de Vida')
    high_cost_countries = df[df['Cost of Living Level'].isin(
        ["Extremely high", "High"])]['Country'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    high_cost_countries.plot(kind='bar', color='purple', ax=ax)
    plt.xlabel('País')
    plt.ylabel('Número de Destinos com Custo de Vida Alto')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Gráfico de Religião
    religion_counts = df['Majority Religion'].value_counts()
    st.subheader('Distribuição de Destinos por Religião Predominante')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.pie(religion_counts, labels=religion_counts.index,
            autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(fig, use_container_width=False)

    # Gráfico de Comidas Famosas
    famous_foods_clean = df['Famous Foods'].dropna()
    food_counter = {}

    for food in famous_foods_clean:
        foods = [f.strip() for f in food.split(',')]
        for f in foods:
            food_counter[f] = food_counter.get(f, 0) + 1

    top_5_foods = sorted(food_counter.items(),
                         key=lambda x: x[1], reverse=True)[:5]
    foods = [item[0] for item in top_5_foods]
    counts = [item[1] for item in top_5_foods]

    st.subheader('Top 5 Comidas Mais Famosas')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.barh(foods, counts, color='skyblue')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Gráfico de Línguas
    language_counts = df['Language'].value_counts()
    top_languages = language_counts.head(5)

    st.subheader('Top 5 Línguas Mais Comuns em Destinos Turísticos')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.bar(top_languages.index, top_languages.values, color='lightgreen')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Top 10 Destinos Mais Visitados
    tourist_counts = df_cleaned.groupby(['Destination', 'Country'])[
        'Approximate Annual Tourists'].sum().reset_index()
    top_destinations = tourist_counts.sort_values(
        by='Approximate Annual Tourists', ascending=False).head(10)

    st.subheader('Top 10 Destinos Mais Visitados')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.bar(top_destinations['Destination'],
            top_destinations['Approximate Annual Tourists'], color='orange')
    plt.title('Top 10 Destinos Mais Visitados')
    plt.xlabel('Destino')
    plt.ylabel('Número Aproximado de Visitantes Anuais')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Análise das Categorias Mais Visitadas
    category_counts = df_cleaned.groupby(
        'Category')['Approximate Annual Tourists'].sum().reset_index()
    top_categories = category_counts.sort_values(
        by='Approximate Annual Tourists', ascending=False).head(5)

    st.subheader('Top 5 Categorias Mais Visitadas')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.bar(top_categories['Category'],
            top_categories['Approximate Annual Tourists'], color='lightblue')
    plt.xlabel('Categoria')
    plt.ylabel('Número de Visitantes Anuais')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Frequência das Moedas
    df_cleaned['Currency'] = df_cleaned['Currency'].str.strip().str.upper()
    currency_counts = df_cleaned['Currency'].value_counts().reset_index()
    currency_counts.columns = ['Currency', 'Count']

    st.subheader('Frequência das Moedas por Destinos')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.bar(currency_counts['Currency'],
            currency_counts['Count'], color='lightgreen')
    plt.title('Frequência das Moedas por Destinos')
    plt.xlabel('Moeda')
    plt.ylabel('Número de Destinos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Melhor época para visitar
    df_cleaned['Best Time to Visit'] = df_cleaned['Best Time to Visit'].str.extract(
        r'(Winter|Spring|Summer|Year-round)')[0]
    best_time_counts = df_cleaned['Best Time to Visit'].value_counts(
    ).reset_index()
    best_time_counts.columns = ['Best Time', 'Count']

    st.subheader('Número de Destinos por Melhor Época para Visitar')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.barh(best_time_counts['Best Time'],
             best_time_counts['Count'], color='yellow')
    plt.title('Número de Destinos por Melhor Época para Visitar')
    plt.xlabel('Número de Destinos')
    plt.ylabel('Melhor Época para Visitar')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif analysis_category == "Análise Social":
    st.subheader('Paises com mais destinos seguros')
    safety_counts = df['Safety Level'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    safety_counts.plot(kind='bar', color='green', ax=ax)
    plt.xlabel('Nível de Segurança')
    plt.ylabel('Número de Destinos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    st.subheader('Distribuição de Destinos por Religião Predominante')
    religion_counts = df['Majority Religion'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.pie(religion_counts, labels=religion_counts.index,
            autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(fig, use_container_width=False)

elif analysis_category == "Análise Cultural":
    st.subheader('Paises com o Maior Custo de Vida')
    high_cost_countries = df[df['Cost of Living Level'].isin(
        ["Extremely high", "High"])]['Country'].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    high_cost_countries.plot(kind='bar', color='purple', ax=ax)
    plt.xlabel('País')
    plt.ylabel('Número de Destinos com Custo de Vida Alto')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    st.subheader('Top 5 Comidas Mais Famosas')
    famous_foods_clean = df['Famous Foods'].dropna()
    food_counter = {}

    for food in famous_foods_clean:
        foods = [f.strip() for f in food.split(',')]
        for f in foods:
            food_counter[f] = food_counter.get(f, 0) + 1

    top_5_foods = sorted(food_counter.items(),
                         key=lambda x: x[1], reverse=True)[:5]
    foods = [item[0] for item in top_5_foods]
    counts = [item[1] for item in top_5_foods]

    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.barh(foods, counts, color='skyblue')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    language_counts = df['Language'].value_counts()
    top_languages = language_counts.head(5)

    st.subheader('Top 5 Línguas Mais Comuns em Destinos Turísticos')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.bar(top_languages.index, top_languages.values, color='lightgreen')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif analysis_category == "Análise Geográfica":
    tourist_counts = df_cleaned.groupby(['Destination', 'Country'])[
        'Approximate Annual Tourists'].sum().reset_index()
    top_destinations = tourist_counts.sort_values(
        by='Approximate Annual Tourists', ascending=False).head(10)

    st.subheader('Top 10 Destinos Mais Visitados')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.bar(top_destinations['Destination'],
            top_destinations['Approximate Annual Tourists'], color='orange')
    plt.title('Top 10 Destinos Mais Visitados')
    plt.xlabel('Destino')
    plt.ylabel('Número Aproximado de Visitantes Anuais')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Frequência das Moedas
    df_cleaned['Currency'] = df_cleaned['Currency'].str.strip().str.upper()
    currency_counts = df_cleaned['Currency'].value_counts().reset_index()
    currency_counts.columns = ['Currency', 'Count']

    st.subheader('Frequência das Moedas por Destinos')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.bar(currency_counts['Currency'],
            currency_counts['Count'], color='lightgreen')
    plt.title('Frequência das Moedas por Destinos')
    plt.xlabel('Moeda')
    plt.ylabel('Número de Destinos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif analysis_category == "Análise Demográfica":
    # Melhor época para visitar
    df_cleaned['Best Time to Visit'] = df_cleaned['Best Time to Visit'].str.extract(
        r'(Winter|Spring|Summer|Year-round)')[0]
    best_time_counts = df_cleaned['Best Time to Visit'].value_counts(
    ).reset_index()
    best_time_counts.columns = ['Best Time', 'Count']

    st.subheader('Número de Destinos por Melhor Época para Visitar')
    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho ajustado
    plt.barh(best_time_counts['Best Time'],
             best_time_counts['Count'], color='yellow')
    plt.title('Número de Destinos por Melhor Época para Visitar')
    plt.xlabel('Número de Destinos')
    plt.ylabel('Melhor Época para Visitar')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Análise das Categorias Mais Visitadas
    category_counts = df_cleaned.groupby(
        'Category')['Approximate Annual Tourists'].sum().reset_index()
    top_categories = category_counts.sort_values(
        by='Approximate Annual Tourists', ascending=False).head(5)

    st.subheader('Top 5 Categorias Mais Visitadas')
    fig, ax = plt.subplots(figsize=(5, 4))  # Tamanho reduzido
    plt.bar(top_categories['Category'],
            top_categories['Approximate Annual Tourists'], color='lightblue')
    plt.xlabel('Categoria')
    plt.ylabel('Número de Visitantes Anuais')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
