import streamlit as st
import pandas as pd


def pega_fatura(arquivo):
    try:
        path=pd.read_excel(arquivo, engine="pyxlsb")
    except Exception as e:
        path=pd.read_csv(arquivo)
    return path

st.set_page_config(
    page_title="KOS INVOICE",
    page_icon='$$$',
    initial_sidebar_state="expanded",
)
st.title(
    ''' 
    ***KOS INVOICE*** 
    ''')
st.header(" Fatura ")

upload=st.file_uploader(label='Clique aqui para inserir sua fatura', type=['csv','xlsx','xlsb'])
if upload :
    fat=pega_fatura(upload)
    num_select = st.selectbox('Select', fat.Ass_B.unique())
    fat_val=pd.DataFrame(fat.loc[fat.Ass_B == num_select],columns=['Unnamed: 12','Min','Val_S_Imp'])
    fat_val.columns=['Plano','Minutos','Valor'] 
    fat_val['Tarifa']=fat_val.Valor/fat_val.Minutos.values
    tax=pd.DataFrame(fat_val,columns=['Plano','Tarifa'])
    st.dataframe(fat.style.set_precision(2))
    st.write(" *Tarifa por plano* ")
    st.dataframe(tax.groupby(['Plano']).mean().style.set_precision(2))
    st.write(" *Total de minutos* ")
    st.dataframe(fat_val.groupby(['Plano']).agg({'Minutos':'sum','Valor':'sum','Tarifa':'mean'}).style.set_precision(2))
    st.write(" *Valor médio por minuto* ")
    st.dataframe(fat_val.groupby(['Plano']).mean().style.set_precision(2))
else :
    st.write(" *Insira sua fatura* ")
