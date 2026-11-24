# Fazer um histórico de atendimentos 
O cliente terá uma nova opção chamada "Meu histórico", na qual poderá consultar todos os atendimentos anteriores, com informações como:
- Nome do serviço;
- Data do atendimento;
- Profissional responsável;
- Valor pago.
Implementação: criar uma tela simples que consulta os atendimentos já registrados para aquele cliente.

# Passo a passo para implementar:
Analisando a estrutura do projeto, a implementação pode aproveitar as
classes e funções que já existem. Não será necessário criar uma nova
entidade, um novo DAO ou um arquivo JSON. A funcionalidade utilizará a
classe `Atendimento`, que já armazena os registros dos atendimentos, e a
relação dela com `Horario`.

## 1. Entendendo como a funcionalidade vai funcionar

Atualmente, o projeto possui esta relação:

-   **Cliente:** possui horários agendados.
-   **Horario:** armazena informações como `id_cliente`, `id_servico` e
    `id_profissional`.
-   **Atendimento:** armazena informações como `id_horario`, data,
    avaliação e prescrição.

A ideia é utilizar essas relações para encontrar os atendimentos de
determinado cliente:

1.  O cliente entra no sistema.
2.  O sistema identifica seu `usuario_id`.
3.  O Service procura os atendimentos cadastrados.
4.  Para cada atendimento, consulta seu horário correspondente.
5.  Verifica se o `id_cliente` desse horário corresponde ao cliente
    logado.
6.  Exibe os atendimentos encontrados.

Assim, cada cliente visualizará somente seu próprio histórico.

## 2. Passo a passo da implementação

### Etapa 1 --- Criar uma função no Service

**Arquivo existente:** `projeto/service.py`

Essa será a principal alteração da funcionalidade.

O arquivo já possui funções relacionadas a atendimentos, como:

-   `atendimento_inserir()`
-   `atendimento_listar()`
-   `atendimento_listar_id()`
-   `horario_visualizar_meus_servicos()`

Adicione uma nova função chamada
`atendimento_visualizar_historico_cliente()`, próxima das outras funções
relacionadas a atendimentos.

``` python
    @staticmethod
    def atendimento_visualizar_historico_cliente(id_cliente):
        r = []

        for atendimento in Service.atendimento_listar():
            horario = Service.horario_listar_id(
                atendimento.get_id_horario()
            )

            if horario != None and horario.get_id_cliente() == id_cliente:
                r.append(atendimento)

        r.sort(key = lambda obj : obj.get_data())
        return r
```

**O que esse código faz?**

-   Recebe o ID do cliente.
-   Percorre os atendimentos cadastrados.
-   Localiza o horário relacionado a cada atendimento.
-   Verifica se o horário pertence ao cliente.
-   Adiciona os atendimentos correspondentes à lista.
-   Organiza os resultados pela data.

Não é necessário alterar `atendimento.py` nem `atendimentodao.py`, pois
eles já armazenam e recuperam os dados necessários.

### Etapa 2 --- Criar a interface do histórico

**Arquivo novo:** `projeto/templates/historicoatendimentosui.py`

Agora será criada a tela apresentada ao cliente.

O projeto utiliza Streamlit e costuma apresentar os registros com
`pandas.DataFrame`. A nova tela seguirá esse padrão, semelhante ao
arquivo `vizualizarmeusservicosui.py`.

Crie o arquivo `historicoatendimentosui.py` dentro da pasta `templates`.

**Código completo:**

``` python
import streamlit as st
import pandas as pd
from service import Service

class HistoricoAtendimentosUI:
    def main():
        st.header("Histórico de Atendimentos")

        atendimentos = Service.atendimento_visualizar_historico_cliente(
            st.session_state["usuario_id"]
        )

        if len(atendimentos) == 0:
            st.write("Nenhum atendimento realizado")

        else:
            dic = []

            for obj in atendimentos:
                horario = Service.horario_listar_id(
                    obj.get_id_horario()
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

                dic.append({
                    "data": obj.get_data(),
                    "serviço": servico,
                    "profissional": profissional,
                    "queixa principal": obj.get_queixa_principal(),
                    "avaliação": obj.get_avaliacao(),
                    "prescrição": obj.get_prescricao()
                })

            df = pd.DataFrame(dic)

            st.dataframe(df)
```

**Como será apresentada a tela?**

O cliente verá uma tabela semelhante a esta:

  Data         Serviço    Profissional
  ------------ ---------- --------------
  08/12/2026   Consulta   Ana
  10/12/2026   Retorno    Carlos

Além dessas informações, a tabela também apresentará a queixa principal,
a avaliação e a prescrição registradas no atendimento. Os dados da
tabela são apenas ilustrativos.

### Etapa 3 --- Adicionar a opção ao menu do cliente

**Arquivo existente:** `projeto/index.py`

Agora será necessário permitir que o cliente acesse a nova tela.

Localize a função `menu_cliente()`. Atualmente, ela está assim:

``` python
def menu_cliente():
    op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços"])
    if op == "Meus Dados": PerfilClienteUI.main()
    if op == "Agendar Serviço": AgendarServicoUI.main()
    if op == "Meus Serviços": VisualizarMeusServicosUI.main()
```

Primeiro, adicione o import no início do arquivo:

``` python
from templates.historicoatendimentosui import HistoricoAtendimentosUI
```

Depois, substitua a função `menu_cliente()` por:

``` python
def menu_cliente():
    op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços", "Histórico de Atendimentos"])
    if op == "Meus Dados": PerfilClienteUI.main()
    if op == "Agendar Serviço": AgendarServicoUI.main()
    if op == "Meus Serviços": VisualizarMeusServicosUI.main()
    if op == "Histórico de Atendimentos": HistoricoAtendimentosUI.main()
```

Pronto! A nova opção aparecerá no menu lateral do cliente, sem modificar
os menus do administrador ou do profissional.

### Etapa 4 --- Testar a funcionalidade

Depois de implementar os códigos, faça os seguintes testes:

-   [ ] Entrar no sistema com uma conta de cliente.
-   [ ] Verificar se a opção **Histórico de Atendimentos** aparece no
    menu.
-   [ ] Acessar o histórico sem possuir atendimentos registrados.
-   [ ] Cadastrar um atendimento associado a um horário do cliente.
-   [ ] Verificar se o atendimento aparece no histórico.
-   [ ] Entrar com outro cliente e verificar se ele não consegue
    visualizar os atendimentos do primeiro.

**Observação importante sobre o projeto:** foi identificado um possível
erro de digitação no import de `ProfissionalDAO` em `service.py`:

``` python
from cd prdao_json.profissionaldao import ProfissionalDAO
```

O caminho esperado pela estrutura das pastas é:

``` python
from dao_json.profissionaldao import ProfissionalDAO
```

Corrija isso antes de executar o projeto, caso essa linha esteja
exatamente assim no seu arquivo.

## 3. Quais arquivos serão modificados?

  Arquivo                                  Alteração
  ---------------------------------------- ----------------------------------
  `service.py`                             Adicionar uma função
  `templates/historicoatendimentosui.py`   Criar arquivo novo
  `index.py`                               Adicionar import e opção no menu

Não será necessário criar:

-   Nova classe em `models`;
-   Novo DAO;
-   Novo arquivo JSON;
-   Novas tabelas no banco de dados;
-   Alterações na classe `Atendimento`.

## 4. Atualização do diagrama de caso de uso

Como o projeto também possui um diagrama de caso de uso, será necessário
acrescentar somente uma funcionalidade:

**Ator:** Cliente

**Novo caso de uso:** Visualizar histórico de atendimentos

O novo caso de uso deverá ser associado ao ator **Cliente**, pois é ele
quem acessará os registros dos próprios atendimentos.

## 5. Recomendação

Façam primeiro as três alterações de código e testem a funcionalidade
antes de atualizar os diagramas. Dessa forma, será possível demonstrar
uma implementação pequena, funcional e coerente com a arquitetura que já
existe no projeto.

