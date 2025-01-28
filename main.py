import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


arquivo = "Database.xlsx"
df = pd.read_excel(arquivo)
st.set_page_config(layout="wide")
def salvar(mt,ic,d,co,al,dt):
    if mt and ic and co and al and dt and d:
        novos_dados = [
            {
            'Materia': mt,
            'H Inicio': ic,
            'Duração': d,
            'Aluno': al,
            'Conteudo':co,
            'Data': dt
            }
        ]
        
        df_novos_dados = pd.DataFrame(novos_dados)
        df_atualizado = pd.concat([df, df_novos_dados], ignore_index=True) 
        df_atualizado.to_excel(arquivo, index=False)
        st.success("Salvo")
    else:
        st.error("Preencha todos os campos")
 



materias_escolares = [
    "Matemática",
    "Português",
    "História",
    "Geografia",
    "Ciências",
    "Biologia",
    "Física",
    "Química",
    "Inglês",
    "Filosofia",
    "Sociologia",
    "Literatura",
    "Redação",
]
alunos = [
    "Felipe",
    "Gustavo",
]


# controle
st.header("Controle de estudo")


st.subheader("Adicionar aula")
aluno = st.selectbox("Selecione o Aluno", options=alunos)


mat =  st.selectbox("Matérias",options= materias_escolares)
inicio = st.time_input("Hora inicio")
fim = st.time_input("Duração")
Conteudo = st.text_input("Conteudo da aula")
data = st.date_input("Data")
if st.button("Salvar"):
    salvar(mat,inicio,fim,Conteudo,aluno,data)

# Baixar conteúdo
st.sidebar.subheader("Baixar conteúdos estudados")
df_para_csv = df.loc[df['Aluno'] == aluno]
csv_file = df_para_csv.to_csv(index=False)

st.sidebar.download_button(label="Download data as CSV",data=csv_file,file_name="controle.csv",mime="text/csv",)
st.sidebar.subheader("Deleter aula")
delete = st.sidebar.number_input("Linha da aula à ser deletada",0)

if st.sidebar.button("Deletar"):
   if delete >= 0:
        df = df.drop(index=delete)
        df.to_excel(arquivo, index=False)
        st.success("Aula deletada com sucesso")
   else:
    st.error("Preencha todos os campos") 

    


col1,col2 = st.columns(2)
col3 = st.columns(1)



pizza = px.pie(df_para_csv,df_para_csv['Materia'])
col1.plotly_chart(pizza)
bar = px.bar(df_para_csv,x=df_para_csv["Data"],color=df_para_csv["Materia"])    
col2.plotly_chart(bar)  


st.table(df_para_csv)