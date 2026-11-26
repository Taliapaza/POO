import streamlit as st
from service import Service
import time

class PerfilClienteUI:
    def main():
        st.header("Meus Dados")

        op = Service.cliente_listar_id(st.session_state["usuario_id"])


        # Dados do cliente
        st.image(op.get_imagem(), width=150)
        nome = st.text_input("Informe o novo nome", op.get_nome())
        email = st.text_input("Informe o novo e-mail", op.get_email())
        fone = st.text_input("Informe o novo fone", op.get_fone())
        senha = st.text_input("Informe a nova senha", op.get_senha(), type="password")

        # Manter a foto atual caso não escolha outra
        foto =  st.file_uploader( "Escolha sua foto de perfil",type=["png", "jpg", "jpeg"])
        imagem = foto.getvalue() if foto else None



        # Atualizar dados
        if st.button("Atualizar"):
            try:
                id = op.get_id()

                Service.cliente_atualizar(
                    id, nome, email, fone, senha, imagem
                )

                st.success("Cliente atualizado com sucesso")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(str(erro))
