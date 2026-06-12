# Sistema de Auditoria e Registro de Ocorrências (Mídias de Transmissão)

Este projeto é uma aplicação desktop desenvolvida em Python com Tkinter, projetada para centralizar, gerenciar e auditar falhas, interrupções ou anomalias técnicas (ocorrências) em transmissões de vídeo.

---

## Para que serve o projeto?

Em ambientes de exibição e transmissão de grande escala, é crítico registrar com precisão qualquer falha técnica (como queda de sinal, áudio cortado ou artefatos na imagem). 

Este sistema serve para:

* Centralizar Logs Técnicos: Unificar o registro de falhas em um formato de tabela estruturado.
* Automatizar a Coleta de Metadados: O sistema lê o arquivo de vídeo selecionado diretamente do sistema operacional e extrai o nome do arquivo e a data de modificação de forma automatizada.
* Auditoria Visual Rápida: Permitir que operadores revisem o trecho exato do erro com apenas dois cliques, agilizando a tomada de decisão e a geração de relatórios de conformidade.

---

## O que é a Interface e como ela é dividida?

A interface gráfica foi construída focando em usabilidade e organização visual, utilizando um tema escuro para evitar a fadiga visual dos operadores que trabalham em salas de controle de longa jornada.

A tela é dividida estrategicamente em 3 componentes principais:

1. Painel Superior (Cabeçalho)
   * Identidade Visual: Exibe o título e o logotipo da aplicação.
   * Ações Globais: Contém os botões principais "ENVIAR CLIP OCORRÊNCIA" (para upload e catalogação automatizada) e "IMPRIMIR RELATÓRIO" (para simular a exportação física dos logs).

2. Menu Lateral (Sidebar)
   * Localizado à esquerda, serve como o centro de navegação da aplicação.
   * Permite alternar dinamicamente o conteúdo da tela principal entre a Página Principal, a tela de Ocorrências (Grid de dados), geração de Relatórios e consulta à Documentação técnica do sistema.

3. Área de Conteúdo Central (Grid de Ocorrências)
   * O coração da interface. Quando a aba "Ocorrências" está ativa, exibe uma tabela contendo a Data da Ocorrência, Tipo/Severidade, Tempo de duração do clipe e o Link do Corte.
   * Interação Avançada: Possui um gatilho de evento de clique duplo. Ao clicar duas vezes em qualquer linha, a interface abre o reprodutor de vídeo padrão do sistema operacional para exibir a mídia selecionada.

---

## Como Rodar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências executando no seu terminal:
   pip install requests pillow ttkthemes
3. Execute a aplicação:
   python gui_app.py

---

Desenvolvido por Glaucio Rodrigues
![image URL] (https://github.com/Glaucio-Rodrigues/Projeto-globo-ocorrencias/blob/main/projeto-globo-ocorrencias.png?raw=true)
