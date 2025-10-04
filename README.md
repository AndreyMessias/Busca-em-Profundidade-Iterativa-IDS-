# Busca em Profundidade Iterativa (IDS) vs. DFS

> Um projeto simples em Python para implementar e comparar visualmente os algoritmos de busca DFS e IDS, demonstrando a superioridade do IDS em grafos com ramos de profundidade variada.

---

## 📖 Sobre o Projeto

Este repositório contém uma implementação desenvolvida como parte das atividades do **Núcleo de Estudos em Inteligência Artificial e Dados (NIAD)**, da **Universidade Federal de Lavras (UFLA)**. 
O objetivo é oferecer uma implementação simples e clara dos algoritmos **Busca em Profundidade (DFS)** e **Busca em Profundidade Iterativa (IDS)**. O objetivo é demonstrar, através de um exemplo prático, as vantagens e desvantagens de cada abordagem.

-   **DFS (Depth-First Search):** Explora um ramo do grafo até o seu final antes de retroceder (backtracking). É eficiente em termos de memória, mas pode ser ineficiente em tempo se a solução estiver em um ramo raso e a busca começar por um ramo muito profundo.

-   **IDS (Iterative Deepening Search):** Combina a eficiência de memória da DFS com a garantia de encontrar a solução mais rasa da BFS (Busca em Largura). Para isso, executa sucessivas buscas em profundidade com um limite que aumenta a cada iteração.

---

### 🧩 O Cenário de Demonstração

O grafo utilizado no exemplo foi projetado para expor a principal fraqueza da DFS:


          A (início)
         / \
        X1  B
        |   |\
        X2  C E (objetivo!)
        |   |
        X3  D
        |
       ...
        |
       X15


Neste cenário, a DFS primeiro explorará o longo e improdutivo caminho `A -> X1 -> ... -> X15` antes de encontrar o caminho ideal e curto `A -> B -> E`. A IDS, por outro lado, encontrará a solução rapidamente ao testar as profundidades 0, 1 e 2.

---

## 🚀 Como Usar

### Pré-requisitos

-   Python 3.x

### Execução

Para executar a demonstração e ver a comparação, clone o repositório e execute o script principal no seu terminal:

```bash
python3 ids.py
```

O script irá imprimir a análise completa, incluindo o caminho encontrado, a trilha de exploração e a contagem de nós visitados para cada algoritmo.

---

## 💻 Estrutura do Código

A implementação está no arquivo:  
`ids.py`  

Principais funções:

- depth_first_search(graph, start_node, goal_node)
-           Implementa a DFS usando uma abordagem recursiva eficiente com backtracking (append/pop). Inclui proteção contra ciclos para garantir o término da busca.

- iterative_deepening_search(graph, start_node, goal_node, max_depth=20)
-           Implementa a IDS. Orquestra múltiplas chamadas a uma busca em profundidade limitada (_dls_recursive interna) com limites de profundidade crescentes, de 0 até max_depth.

---

## 📊 Resultados

A execução do script produz a seguinte saída, que detalha o comportamento de cada algoritmo:

### Saída do Terminal
    PONTO INICIAL: A, OBJETIVO: E

    --- Executando DFS (eficiente com backtracking) ---
    Caminho final da DFS: A -> B -> E
    
    Trilha completa de exploração da DFS (nós visitados na sequência):
    A -> X1 -> X2 -> X3 -> X4 -> X5 -> X6 -> X7 -> X8 -> X9 -> X10 -> X11 -> X12 -> X13 -> X14 -> X15 -> B -> C -> D -> E
    
    Total de nós explorados pela DFS: 20
    
    --- Executando IDS (eficiente) ---
    IDS encontrou o objetivo 'E' na profundidade L=2
    Caminho final do IDS: A -> B -> E
    
    Trilha completa de exploração do IDS (concatenação das iterações L=0, L=1...):
    A -> A -> X1 -> B -> A -> X1 -> X2 -> B -> C -> E
    
    Total de nós (com repetições) nas iterações IDS: 10
    
    --- Comparação ---
    Nós explorados (DFS): 20
    Nós explorados (IDS com repetições): 10
      
  ---
    
## 📊 Análise Comparativa

A saída do terminal mostra a principal diferença entre os algoritmos:

- DFS explorou 20 nós. A "Trilha completa de exploração" mostra que o algoritmo primeiro desceu todo o ramo X1 até X15 (15 nós), para só então retroceder e explorar o ramo B, onde encontrou a solução.

- IDS explorou um total de 10 nós (contando as repetições). A trilha mostra claramente as iterações:

      L=0: Explora A (1 nó).
  
      L=1: Explora A -> X1 e A -> B (3 nós).
  
      L=2: Explora A -> X1 -> X2, A -> B -> C e A -> B -> E, encontrando a solução (6 nós).
  
      Total: 1 + 3 + 6 = 10 nós.

Esta demonstração evidencia que, embora a IDS realize trabalho repetido nos níveis superiores, esse custo é baixo em comparação com o custo de explorar um ramo profundo e improdutivo, como a DFS fez.s.








