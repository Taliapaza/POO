# Criar a página da funcionalidade 

#Primeiro importar:
import streamlit as st
import pandas as pd
from service import Service

class HistoricoAtendimentosUI:
    def main():
        st.header("Histórico de Atendimentos") #título

        atendimentos = Service.atendimento_visualizar_historico_cliente( 
            #achar a função no service que eu fiz (retorna  a lista de atendimentos q é o histórico)
            st.session_state["usuario_id"] #acessar os dados do cliente 
        )

        if len(atendimentos) == 0: #se não tiver atendimentos cadastrados 
            st.write("Nenhum atendimento realizado") 

        else:
            dic = [] #abre um dicionário 

            for obj in atendimentos: #varrer os atendimentos 
                horario = Service.horario_listar_id( #listar os id's de horário
                    obj.get_id_horario() #usar o id_horário para pegar cada atendimento
                )

                servico = Service.servico_listar_id( 
                    horario.get_id_servico()
                )

                profissional = Service.profissional_listar_id(
                    horario.get_id_profissional()
                )

                if servico != None:
                    servico = servico.get_descricao()

                if profissional != None:
                    profissional = profissional.get_nome()

                dic.append({ #adicionar todas as informações a um dicionário
                    "data": obj.get_data(),
                    "serviço": servico,
                    "profissional": profissional,
                    "queixa principal": obj.get_queixa_principal(),
                    "avaliação": obj.get_avaliacao(),
                    "prescrição": obj.get_prescricao()
                })

            df = pd.DataFrame(dic)

            st.dataframe(df)
