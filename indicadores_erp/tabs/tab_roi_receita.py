import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA

@st.cache_data
def run_automated_analysis(df: pd.DataFrame):
    """
    Executa um pipeline de análise automatizado no DataFrame fornecido.
    """
    df_analysis = df.copy()

    # 1. Tentar converter colunas de objeto para data/hora
    for col in df_analysis.select_dtypes(include=['object']).columns:
        try:
            df_analysis[col] = pd.to_datetime(df_analysis[col], errors='raise', format='mixed')
        except (ValueError, TypeError):
            continue # Não é uma coluna de data/hora

    # 2. Identificar tipos de colunas, agora separando datetimes
    datetime_features = df_analysis.select_dtypes(include=['datetime64']).columns
    numeric_features = df_analysis.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = df_analysis.select_dtypes(include=['object', 'category']).columns

    # Remover colunas com apenas um valor único (não informativas) das listas de features
    for col in df_analysis.columns:
        if df_analysis[col].nunique() <= 1:
            if col in numeric_features:
                numeric_features = numeric_features.drop(col)
            if col in categorical_features:
                categorical_features = categorical_features.drop(col)

    # 3. Criar pipelines de pré-processamento
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # 4. Combinar pré-processadores
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)],
        remainder='drop') # Ignora colunas não especificadas (como as de data/hora)

    # 5. Criar o pipeline de análise completo com K-Means
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('cluster', KMeans(n_clusters=4, n_init=10, random_state=42))])
    
    # 6. Executar o pipeline
    pipeline.fit(df_analysis)
    cluster_labels = pipeline.named_steps['cluster'].labels_

    # 7. Redução de dimensionalidade com PCA para visualização
    processed_data = pipeline.named_steps['preprocessor'].transform(df_analysis)
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(processed_data.toarray() if hasattr(processed_data, "toarray") else processed_data)

    # 8. Preparar o DataFrame de resultados
    df_result = df.copy()
    df_result['cluster'] = cluster_labels
    df_result['pca-one'] = pca_result[:, 0]
    df_result['pca-two'] = pca_result[:, 1]
    
    return df_result, numeric_features, categorical_features, datetime_features

def render_tab_roi_receita():
    """
    Renderiza a aba de Análise de ROI em Receita.
    """
    st.header("Análise Automática de Clusters")
    
    st.write("Faça o upload de uma planilha (CSV ou Excel) para segmentar seus dados automaticamente.")

    uploaded_file = st.file_uploader(
        "Escolha sua planilha de dados", 
        type=['csv', 'xlsx'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            @st.cache_data
            def load_data(file):
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                return df

            df_original = load_data(uploaded_file)
            st.success(f"Arquivo **{uploaded_file.name}** carregado com sucesso!")

            if df_original.empty:
                st.warning("A planilha está vazia.")
                return

            with st.spinner('Executando análise automática...'):
                df_result, numeric, categ, datetimes = run_automated_analysis(df_original)

            st.subheader("Visualização dos Clusters")
            st.markdown(
                "Os dados foram agrupados em clusters. O gráfico abaixo mostra essa separação. "
                "Pontos da mesma cor pertencem ao mesmo grupo e compartilham características semelhantes."
            )
            
            # Gráfico de dispersão
            st.scatter_chart(
                df_result,
                x='pca-one',
                y='pca-two',
                color='cluster',
                size=5,
            )
            
            st.subheader("Dados com Clusters Atribuídos")
            st.markdown("A tabela abaixo mostra os dados originais com uma nova coluna 'cluster' indicando a que grupo cada linha pertence.")
            st.dataframe(df_result.drop(['pca-one', 'pca-two'], axis=1))

            st.subheader("Resumo da Análise")
            st.write(f"Foram analisadas **{len(numeric)}** colunas numéricas e **{len(categ)}** colunas de texto.")
            if len(datetimes) > 0:
                st.info(f"As seguintes colunas de data/hora foram detectadas e **excluídas** da análise de cluster: `{list(datetimes)}`")
            st.write(f"As colunas numéricas foram: `{list(numeric)}`")
            st.write(f"As colunas de texto foram: `{list(categ)}`")


        except Exception as e:
            st.error(f"Ocorreu um erro durante a análise: {e}")
            st.error("Por favor, verifique se a planilha tem dados válidos e tente novamente.")
