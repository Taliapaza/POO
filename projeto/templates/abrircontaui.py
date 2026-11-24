import streamlit as st
from service import Service
import time

class AbrirContaUI:
    def main():
        st.header("Abrir Conta no Sistema")
        foto =  st.file_uploader( "Escolha sua foto de perfil",type=["png", "jpg", "jpeg"])
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone")
        senha = st.text_input("Informe a senha", type="password")
        imagem = foto.getvalue() if foto else None


        if st.button("Inserir"):
            try:
                Service.cliente_inserir(nome, email, fone, senha, imagem)
                st.success("Conta criada com sucesso")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(str(erro))