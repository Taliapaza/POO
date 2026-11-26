
#importar: 
import streamlit as st
import pandas as pd
from service import Service

class MostrarAgendaSemanaUI:

    def main():
        st.header("Agenda da Semana")

        #pega os horários dos próximos 7 dias (daquela função do service que fiz para pegar os da semana)
        horarios = Service.admin_visualizar_agenda_semana()

        # ver se tem horários 
        if len(horarios) == 0:
            st.write("Nenhum horário agendado para os próximos sete dias")

        else:
            list_dic = []

            #pega todos os horários 
            for obj in horarios:

                #buscar o cliente do horário 
                cliente = Service.cliente_listar_id(
                    obj.get_id_cliente()
                )

                #buscar o servico do horário
                servico = Service.servico_listar_id(
                    obj.get_id_servico()
                )

                # buscar o profissinal do horário
                profissional = Service.profissional_listar_id(
                    obj.get_id_profissional()
                )

                #pega o nome e a descrição 
                if cliente != None:
                    cliente = cliente.get_nome()

                if servico != None:
                    servico = servico.get_descricao()

                if profissional != None:
                    profissional = profissional.get_nome()

                #adicionar tudo a lista
                list_dic.append({
                    "id": obj.get_id(),
                    "data": obj.get_data(),
                    "cliente": cliente,
                    "serviço": servico,
                    "profissional": profissional
                })

            #transformar de dicionário para tabela 
            df = pd.DataFrame(list_dic)

            #mostrar a tabela 
            st.dataframe(df)
