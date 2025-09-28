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
- `dfs_limitado(no, limite)` → realiza busca em profundidade com limite.  
- `ids(raiz, objetivo)` → chama repetidamente `dfs_limitado` com limites crescentes até encontrar a solução.  

---

## 📊 Resultados

### Saída da DFS (pura)
