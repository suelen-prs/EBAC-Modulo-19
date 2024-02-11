import timeit
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


sns.set_theme(style='ticks',
              rc={'axes.spines.right': False,
                  'axes.spines.top': False})


# Carregando os dados
@st.cache_data
def load_data(file_data: str, sep: str) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=file_data, sep=sep)


def multiselect_filter(data: pd.DataFrame,
                       col: str,
                       selected: list[str]
                       ) -> pd.DataFrame:
    if 'all' in selected:
        return data
    else:
        return data[data[col].isin(selected)].reset_index(drop=True)


def main():
    st.set_page_config(
        page_title="EBAC - Streamlit II - Exercício 1",
        page_icon="../img/telmarketing_icon.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar
    image = Image.open(fp='../img/Bank-Branding.jpg')
    st.sidebar.image(image=image)

       # Título principal da aplicação
    st.write('# Telemarketing analysis')
    st.markdown(body='---')

    bank_raw = load_data(
        file_data='../data/input/bank-additional-full.csv', sep=';')
    bank = bank_raw.copy()

    st.write('## Antes dos filtros')
    st.write(bank_raw)
    st.write('Quantidade de linhas:', bank_raw.shape[0])
    st.write('Quantidade de colunas:', bank_raw.shape[1])

    with st.sidebar.form(key='my_form'):
        # Idade
        min_age = min(bank['age'])
        max_age = max(bank['age'])

        idades = st.slider(label='Idade',
                           min_value=min_age,
                           max_value=max_age,
                           value=(min_age, max_age),
                           step=1)

        # Profissões
        jobs_list = bank['job'].unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.multiselect(
            label='Profissões', options=jobs_list, default=['all'])

        # Estado Civil
        marital_list = bank['marital'].unique().tolist()
        marital_list.append('all')
        marital_selected = st.multiselect(
            'Estado Civil', marital_list, ['all'])

        # Default
        default_list = bank['default'].unique().tolist()
        default_list.append('all')
        default_selected = st.multiselect(
            'Default', default_list, ['all'])

        # Financiamento
        housing_list = bank['housing'].unique().tolist()
        housing_list.append('all')
        housing_selected = st.multiselect(
            'Tem financiamento imobiliário?', housing_list, ['all'])

        # Emprestimo
        loan_list = bank['loan'].unique().tolist()
        loan_list.append('all')
        loan_selected = st.multiselect('Tem empréstimo?', loan_list, ['all'])

        # Contato
        contact_list = bank['contact'].unique().tolist()
        contact_list.append('all')
        contact_selected = st.multiselect(
            'Meio de contato', contact_list, ['all'])

        # Mês do contato
        month_list = bank['month'].unique().tolist()
        month_list.append('all')
        month_selected = st.multiselect('Mês do contato', month_list, ['all'])

        # Dia da semana
        day_of_week_list = bank['day_of_week'].unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected = st.multiselect(
            'Dia da semana do contato', day_of_week_list, ['all'])

        bank = (bank.query('age >= @idades[0] and age <= @idades[1]')
                    .pipe(multiselect_filter, 'job', jobs_selected)
                    .pipe(multiselect_filter, 'marital', marital_selected)
                    .pipe(multiselect_filter, 'default', default_selected)
                    .pipe(multiselect_filter, 'housing', housing_selected)
                    .pipe(multiselect_filter, 'loan', loan_selected)
                    .pipe(multiselect_filter, 'contact', contact_selected)
                    .pipe(multiselect_filter, 'month', month_selected)
                    .pipe(multiselect_filter, 'day_of_week', day_of_week_selected))

        submit_button = st.form_submit_button(label='Aplicar')

    st.write('## Após os filtros')
    st.write(bank)
    st.write('Quantidade de linhas:', bank.shape[0])
    st.write('Quantidade de colunas:', bank.shape[1])

    st.markdown('---')

    # Gráficos
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    # Coluna 1
    bank_raw_target_pct = bank_raw['y'].value_counts(
        normalize=True).to_frame() * 100
    bank_raw_target_pct = bank_raw_target_pct.sort_index()
    sns.barplot(x=bank_raw_target_pct.index,
                y='proportion',
                data=bank_raw_target_pct,
                ax=axes[0])
    axes[0].bar_label(container=axes[0].containers[0])
    axes[0].set_title(label='Dados brutos', fontweight='bold')
    # Coluna 2
    bank_target_pct = bank['y'].value_counts(normalize=True).to_frame() * 100
    bank_target_pct = bank_target_pct.sort_index()
    sns.barplot(x=bank_target_pct.index,
                y='proportion',
                data=bank_target_pct,
                ax=axes[1])
    axes[1].bar_label(container=axes[1].containers[0])
    axes[1].set_title(label='Dados filtrados', fontweight='bold')
    st.write('## Proporção de aceite')
    st.pyplot(plt)


if __name__ == '__main__':
    main()