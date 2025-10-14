import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from geopy.geocoders import Nominatim
import time
def mostrar():
    st.title("📊 Dashboard - Senatural")

    def carregar_dados(arquivo):
        try:
            with open(arquivo,'r') as file:
                linhas=file.readlines()
            produtos=[]
            produto={}
            for linha in linhas:
                linha=linha.strip()
                if linha.startswith("Código:"):
                    produto["Código"] = linha.split("Código:")[1].strip()

                elif linha.startswith("Nome:"):
                    produto["Nome"]=linha.split("Nome:")[1].strip()

                elif linha.startswith("Valor:"):
                    produto["Valor"]=float(linha.split("Valor:")[1].replace(',','.'))

                elif linha.startswith("Quantidade:"):
                    produto["Quantidade"]=int(linha.split("Quantidade:")[1].strip())

                elif linha.startswith("Categoria"):
                    produto["Categoria"]=linha.split("Categoria:")[1].strip()

                elif linha.startswith("Descrição:"):
                    produto["Descrição"]=linha.split("Descrição:")[1].strip()

                elif linha.startswith("Total:"):
                    produto["Total"]=float(linha.split("Total:")[1].replace(",","."))

                elif linha.startswith("Data:"):
                    produto["Data"]=linha.split("Data:")[1].strip()

                elif linha.startswith("CEP:"):
                    produto["CEP"]=linha.split("CEP:")[1].strip()
                
                elif linha.startswith("Número:"):
                    produto["Número"]=linha.split("Número:")[1].strip()

                elif linha.startswith("Endereço:"):
                    produto["Endereço"]=linha.split("Endereço:")[1].strip()

                elif linha.startswith("Cidade:"):
                    produto["Cidade"]=linha.split("Cidade:")[1].strip()

                elif linha.startswith("Estado:"):
                    produto["Estado"]=linha.split("Estado:")[1].strip()

                elif linha.startswith("-"):
                    produtos.append(produto)
                    produto = {}
            df = pd.DataFrame(produtos)
            df.columns = df.columns.str.strip().str.lower()
            df.columns = df.columns.str.capitalize()
            
            df["Data"] = pd.to_datetime(df["Data"],errors="coerce")
            return df

        except FileNotFoundError:
            st.error("Arquivo não encontrado")
            return pd.DataFrame()
    df = carregar_dados("produtos.txt")
    if not df.empty:
        st.header("Tabela com os dados!")
        st.dataframe(df)
        df_categoria = df.groupby("Categoria")["Total"].sum().reset_index()
        graf_pizza = px.pie(df_categoria, names= "Categoria", values="Total",title="Participação no valor total por categoria",color_discrete_sequence=["#FF0000","#7FFFD4","#E2725B","#48D1CC"])
        st.plotly_chart(graf_pizza)

        graf_disp = px.scatter(df,x="Valor",y="Quantidade",color="Categoria",hover_data=["Nome"],title="Correlação entre preço e qtd")
        st.plotly_chart(graf_disp)

        top5 = df.sort_values(by="Valor",ascending = False).head(5)
        graf_bar = px.bar(top5,x="Nome",y="Valor",color="Categoria",title="Top 5 produtos mais caros")
        st.plotly_chart(graf_bar)

        df_data = df.groupby("Data")["Total"].sum().reset_index()
        graf_linha = px.line(df_data,x="Data",y="Total",markers=True,title="Total vendido por data")
        st.plotly_chart(graf_linha)
        geolocalização = Nominatim(user_agent="Senatural_dashboard")

        def obter_coordenadas(row):
            endereco = f'{row["Endereço"]},{row["Número"]}, {row["Cidade"]},{row["Estado"]},Brasil'
            try:
                localizacao = geolocalização.geocode(endereço, timeout=10)
                if localizacao:
                    return pd.Series({'lat': localizacao.latitude,
                                    'lon': localizacao.longitude})
            except:
                return pd.Series({'lat': None, 'lon': None})
            return pd.Series({'lat': None, 'lon': None})
        if "lat" not in df.columns or "lon" not in df.columns:
            coords= df.apply(obter_coordenadas, axis= 1)
            df["lat"] = coords["lat"]
            df["lon"] = coords["lon"]
        mapa_df= df.dropna(subset=["lat","lon"])
        if not mapa_df.empty:
            st.map(mapa_df[["lat","lon"]])
        else:
            st.warning("Nenhum endereço válido para mostrar no mapa")   
    else:
        st.warning("Nenhum dados cadastrado!")





