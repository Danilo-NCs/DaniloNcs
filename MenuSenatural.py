import streamlit as st
import Trabalho
import Senatural

st.set_page_config(page_title="Senatural - Produtos Naturais"
                   ,layout="wide"
                   ,page_icon="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fsternmeister%2Fart%2FPacificador-Peacemaker-002-colorido-905454875&psig=AOvVaw0-bFOh5iTY70Qxkv7K998G&ust=1760447623086000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCIDn8s2goZADFQAAAAAdAAAAABAE")
st.title("Senatural - Loja de Produtos Naturais")
abas= st.tabs(["Saída de Estoque","Gráficos","Contato"])

with abas[0]:
    Trabalho.mostrar()
with abas[1]:
    Senatural.mostrar()
with abas[2]:
    st.header("Contato")
    st.write("Desenvolvido por Danilo Nasciemnto")
    st.write("Email:danilonascimento705210@gmail.com")