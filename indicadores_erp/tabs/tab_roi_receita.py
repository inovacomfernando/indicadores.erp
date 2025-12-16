import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA

@st.cache_data
def intelligent_load_and_clean(file):
    """
    Carrega dados de um arquivo e realiza uma limpeza de tipos inteligente.
    """
    df = pd.read_csv(file, encoding='utf-8', sep=None, engine='python') if file.name.endswith('.csv') else pd.read_excel(file)

    # Tenta converter colunas para numéricas de forma agressiva
    for col in df.columns:
        # Tenta converter para numérico. Se a coluna já for numérica ou data, ignora.
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col])
    
    return df

@st.cache_data
def engineer_dates_and_identify_types(df: pd.DataFrame):
    """
    Converte datas, cria features a partir delas e identifica os tipos de colunas para a análise.
    """
    df_engineered = df.copy()
    
    original_datetime_features = []
    for col in df_engineered.select_dtypes(include=['object']).columns:
        try:
            df_engineered[col] = pd.to_datetime(df_engineered[col], errors='raise', format='mixed')
            original_datetime_features.append(col)
        except (ValueError, TypeError):
            continue

    for col in original_datetime_features:
        df_engineered[f'{col}_Ano'] = df_engineered[col].dt.year
        df_engineered[f'{col}_Mês'] = df_engineered[col].dt.month
        df_engineered[f'{col}_Dia'] = df_engineered[col].dt.day
        df_engineered[f'{col}_DiaDaSemana'] = df_engineered[col].dt.dayofweek

    numeric_features = df_engineered.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = df_engineered.select_dtypes(include=['object', 'category']).columns

    for col in list(numeric_features) + list(categorical_features):
        if df_engineered[col].nunique() <= 1:
            if col in numeric_features:
                numeric_features = numeric_features.drop(col)
            if col in categorical_features:
                categorical_features = categorical_features.drop(col)

    return df_engineered, list(numeric_features), list(categorical_features), original_datetime_features

@st.cache_data
def run_analysis(df: pd.DataFrame, numeric_features: list, categorical_features: list):
    """
    Executa o pipeline de clustering e PCA.
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)],
        remainder='drop')

    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('cluster', KMeans(n_clusters=4, n_init='auto', random_state=42))])
    
    pipeline.fit(df)
    cluster_labels = pipeline.named_steps['cluster'].labels_

    processed_data = pipeline.named_steps['preprocessor'].transform(df)
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(processed_data)

    return cluster_labels, pca_result

def render_tab_roi_receita():
    st.header("Análise Semi-Automática de Clusters")
    st.write("Faça o upload de uma planilha (CSV ou Excel) para segmentar seus dados.")

    uploaded_file = st.file_uploader("Escolha sua planilha", type=['csv', 'xlsx'], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            df_cleaned = intelligent_load_and_clean(uploaded_file)
            st.success(f"Arquivo **{uploaded_file.name}** carregado e pré-processado!")

            if df_cleaned.empty:
                st.warning("A planilha está vazia."); return

            df_engineered, numeric, categ, datetimes = engineer_dates_and_identify_types(df_cleaned)

            with st.expander("Clique para ver o Plano de Análise", expanded=True):
                st.markdown("##### O que será analisado:")
                if not numeric and not categ:
                    st.warning("Nenhuma coluna válida para análise foi encontrada.")
                else:
                    st.write("**Colunas Numéricas:**", f"`{numeric}`" if numeric else "Nenhuma")
                    st.write("**Colunas de Texto:**", f"`{categ}`" if categ else "Nenhuma")
                    if datetimes:
                        st.info(f"**Colunas de Data (`{datetimes}`) foram transformadas em features numéricas (Ano, Mês, Dia, etc.) e incluídas na análise.**")
            
            if st.button("Confirmar e Executar Análise", type="primary"):
                with st.spinner('Executando análise... Isso pode levar um momento.'):
                    cluster_labels, pca_result = run_analysis(df_engineered, numeric, categ)
                    
                    # Usa o df_cleaned para mostrar os dados originais, antes da engenharia de datas
                    df_result = df_cleaned.copy()
                    df_result['cluster'] = cluster_labels
                    df_result['pca-one'] = pca_result[:, 0]
                    df_result['pca-two'] = pca_result[:, 1]

                    st.subheader("Visualização dos Clusters")
                    st.markdown("Os dados foram agrupados. O gráfico abaixo mostra a separação.")
                    st.scatter_chart(df_result, x='pca-one', y='pca-two', color='cluster')
                    
                    st.subheader("Dados com Clusters Atribuídos")
                    st.dataframe(df_result.drop(['pca-one', 'pca-two'], axis=1))

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
            st.error("Verifique se a planilha é válida. O erro pode ocorrer se o formato do arquivo for incompatível ou se uma coluna de texto contiver valores que parecem datas mas não são consistentes.")

