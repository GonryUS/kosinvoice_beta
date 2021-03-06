import streamlit as st
import pandas as pd

def pega_fatura(arquivo):
  try:
    path=pd.read_excel(arquivo, engine="pyxlsb")
  except Exception as e:
    path=pd.read_csv(arquivo)
  return path


st.header(" Fatura ")
upload=st.file_uploader(label='Clique aqui para inserir sua fatura', type=['csv','xlsx','xlsb'], help='Clique em browse files para fazer upload da fatura')
if upload :
  fat=pega_fatura(upload)
  with st.form(key='my_form'):
    try:
      num_select = st.selectbox('Qual número deseja consultar?', fat.EQPTO_ORIG.unique())
      submit_button = st.form_submit_button(label='Aplicar')
    except:
      num_select = st.selectbox('Qual número deseja consultar?', fat.Ass_B.unique())
      submit_button = st.form_submit_button(label='Aplicar')
    if submit_button :
      try:
        fat_val=pd.DataFrame(fat.loc[fat.EQPTO_ORIG == num_select],columns=['DESC_ITEM','QTDE_MEDIDA','VALOR_COM_IMP','VALOR_SEM_IMP'])
        fat_val.columns=['Plano','Minutos','Valor com imposto','Valor sem imposto']
        fat_val['Tarifa com imposto']=fat_val['Valor com imposto']/fat_val.Minutos.values
        fat_val['Tarifa sem imposto']=fat_val['Valor sem imposto']/fat_val.Minutos.values
        tax=pd.DataFrame(fat_val,columns=['Plano','Tarifa com imposto','Tarifa sem imposto'])
        st.dataframe(fat_val.style.set_precision(2))
        st.write(" *Tarifa por plano* ")
        st.dataframe(tax.groupby(['Plano']).mean().style.set_precision(2))
        st.write(" *Total de minutos* ")
        st.dataframe(fat_val.groupby(['Plano']).agg({'Minutos':'sum','Valor com imposto':'sum','Valor sem imposto':'sum','Tarifa com imposto':'mean','Tarifa sem imposto':'mean'}).style.set_precision(2))
        st.write(" *Valor médio por minuto* ")
        st.dataframe(fat_val.groupby(['Plano']).mean().style.set_precision(2))
      except:
        fat_val=pd.DataFrame(fat.loc[fat.Ass_B == num_select],columns=['Unnamed: 12','Min','Val_S_Imp'])
        fat_val.columns=['Plano','Minutos','Valor'] 
        fat_val['Tarifa']=fat_val.Valor/fat_val.Minutos.values
        tax=pd.DataFrame(fat_val,columns=['Plano','Tarifa'])
        st.dataframe(fat_val.style.set_precision(2))
        st.write(" *Tarifa por plano* ")
        st.dataframe(tax.groupby(['Plano']).mean().style.set_precision(2))
        st.write(" *Total de minutos* ")
        st.dataframe(fat_val.groupby(['Plano']).agg({'Minutos':'sum','Valor':'sum','Tarifa':'mean'}).style.set_precision(2))
        st.write(" *Valor médio por minuto* ")
        st.dataframe(fat_val.groupby(['Plano']).mean().style.set_precision(2))
else :
  st.write(" *Insira sua fatura* ")
