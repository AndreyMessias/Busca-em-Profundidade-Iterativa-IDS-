# Busca em Profundidade Iterativa (IDS)

Este repositório contém uma implementação simples da **Busca em Profundidade Iterativa (IDS)** e uma comparação com a **Busca em Profundidade (DFS)** em um cenário problemático.

---

## 🚀 Introdução

- **DFS (Depth-First Search):**  
  Explora profundamente primeiro, usa pouca memória, mas pode se perder em caminhos muito longos ou até infinitos.  

- **IDS (Iterative Deepening Search):**  
  Executa várias buscas em profundidade limitada (DLS), aumentando o limite a cada vez.  
  Combina a **eficiência de memória do DFS** com a **garantia de otimalidade do BFS**.  

---

## 🧩 Cenário do Problema

Criamos uma árvore simples onde:
- A DFS se perde em um caminho profundo sem encontrar a solução.  
- A IDS, ao aumentar gradualmente a profundidade, encontra a **solução ótima** (mais rasa).  

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
---

## 💻 Código

A implementação está no arquivo:  
`ids.py`  

Principais funções:

dfs_recursive(start, goal, graph)
Implementa uma DFS recursiva simples, sem proteção contra ciclos.

Retorna uma tupla com:
o caminho encontrado (ou None se não achar),
a ordem de exploração dos nós.

dls_trace(node, goal, graph, limit, ...)
Implementa a busca em profundidade limitada (DLS).
Guarda a ordem de nós visitados e devolve o caminho caso o objetivo seja encontrado dentro do limite.

ids(start, goal, graph, max_depth=20)
Implementa a Busca em Profundidade Iterativa (IDS).
Roda o dls_trace com limites crescentes até encontrar a solução.

Retorna:
o caminho encontrado,
o limite em que a solução foi descoberta,
a ordem completa dos nós visitados em todas as iterações.

---

## 📊 Resultados

### Saída do Terminal
      Grafo de exemplo (resumo):
      A -> ['X1', 'B']
      B -> ['C', 'E']
      Ramo profundo: X1 -> ... -> X15 (len = 15)

      --- Executando DFS (recursiva) ---
      DFS encontrou caminho: ['A', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'B', 'C', 'D', 'E']
      DFS ordem explorada (primeiros 50 nós): ['A', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'B', 'C', 'D',       'E']
      Total de nós explorados pela DFS: 20

      --- Executando IDS ---
      IDS encontrou o objetivo 'E' no limite L=2
      Caminho IDS: ['A', 'B', 'E']
      IDS ordem (concatenação das iterações): ['A', 'A', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'D', 'E']
      Total de nós (com repetições) nas iterações IDS: 11
      
      --- Comparação simples ---
      DFS explorou (nós): 20
      IDS explorou (nós com repetições): 11
      
      Observação: A DFS explorou primeiro o ramo profundo, visitando muitos nós X1..Xn antes de voltar e encontrar B->E. A IDS localizou E em profundidade pequena       (2), sem explorar toda a cadeia profunda.
