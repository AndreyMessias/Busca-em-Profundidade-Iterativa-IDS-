"""Implementação e comparação de algoritmos de busca: DFS, DLS e IDS.

Este módulo fornece implementações eficientes dos algoritmos Depth-First Search (DFS),
Depth-Limited Search (DLS), e Iterative Deepening Search (IDS). Ele também
inclui um exemplo prático que demonstra a vantagem do IDS sobre o DFS em
um grafo com ramos de profundidade desigual.
"""

from typing import List, Dict, Optional, Tuple, Set, TypeAlias

# Type Alias para representar a estrutura do grafo, melhorando a legibilidade.
Graph: TypeAlias = Dict[str, List[str]]

def depth_first_search(
    graph: Graph,
    start_node: str,
    goal_node: str
) -> Tuple[Optional[List[str]], List[str]]:
    """Executa uma Busca em Profundidade (DFS) em um grafo.

    Esta implementação utiliza recursão com backtracking explícito (append/pop)
    e um conjunto de nós visitados para evitar ciclos e garantir o término
    da busca em grafos cíclicos.

    Args:
        graph: Um dicionário representando a lista de adjacência do grafo.
        start_node: O nó inicial da busca.
        goal_node: O nó objetivo a ser encontrado.

    Returns:
        Uma tupla contendo:
        - Uma lista de strings representando o caminho do início ao fim, ou None
          se nenhum caminho for encontrado.
        - Uma lista de strings com a ordem completa dos nós visitados.
    """
    path = []
    exploration_order = []
    visited: Set[str] = set()

    def _dfs_recursive(current_node: str) -> bool:
        """Função auxiliar recursiva que modifica 'path' e 'visited'."""
        path.append(current_node)
        visited.add(current_node)
        exploration_order.append(current_node)

        if current_node == goal_node:
            return True

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                if _dfs_recursive(neighbor):
                    return True
        
        # BACKTRACK: remove o nó do caminho ao retroceder de um ramo sem saída.
        path.pop()
        return False

    found = _dfs_recursive(start_node)
    return path if found else None, exploration_order


def _dls_recursive(
    graph: Graph,
    goal_node: str,
    path: List[str],
    limit: int,
    exploration_order: List[str]
) -> bool:
    """Função auxiliar recursiva para a Busca em Profundidade Limitada (DLS).

    Opera modificando a lista 'path' compartilhada. A busca é cortada se a
    profundidade atual exceder o limite estabelecido.

    Args:
        graph: O grafo da busca.
        goal_node: O nó objetivo.
        path: A lista representando o caminho atual (modificada in-place).
        limit: A profundidade máxima permitida para a busca.
        exploration_order: Lista para registrar a ordem de visitação dos nós.

    Returns:
        True se o objetivo for encontrado dentro do limite, False caso contrário.
    """
    current_node = path[-1]
    exploration_order.append(current_node)

    if current_node == goal_node:
        return True

    # A profundidade corresponde ao número de arestas, que é len(path) - 1.
    if len(path) - 1 >= limit:
        return False

    for neighbor in graph.get(current_node, []):
        # Evita ciclos no caminho atual, garantindo o progresso da busca.
        if neighbor not in path:
            path.append(neighbor)
            if _dls_recursive(graph, goal_node, path, limit, exploration_order):
                return True
            # BACKTRACK: desfaz o passo para explorar outras possibilidades.
            path.pop()

    return False

def iterative_deepening_search(
    graph: Graph,
    start_node: str,
    goal_node: str,
    max_depth: int = 20
) -> Tuple[Optional[List[str]], int, List[str]]:
    """Executa uma Busca em Profundidade Iterativa (IDS) em um grafo.

    Este método combina a eficiência de espaço da DFS com a otimalidade da BFS
    (em grafos com custos de aresta uniformes) ao realizar sucessivas buscas
    em profundidade limitada com limites crescentes.

    Args:
        graph: O grafo da busca.
        start_node: O nó inicial.
        goal_node: O nó objetivo.
        max_depth: A profundidade máxima que o algoritmo irá explorar.

    Returns:
        Uma tupla contendo:
        - O caminho encontrado, ou None se não for encontrado até a 'max_depth'.
        - A profundidade em que a solução foi encontrada (-1 se não encontrada).
        - A ordem total de exploração, concatenada de todas as iterações.
    """
    total_exploration_order = []
    # Itera sobre os limites de profundidade, de 0 até max_depth.
    for depth_limit in range(max_depth + 1):
        path = [start_node]
        order_this_iteration = []
        
        found = _dls_recursive(graph, goal_node, path, depth_limit, order_this_iteration)
        
        total_exploration_order.extend(order_this_iteration)

        if found:
            return path, depth_limit, total_exploration_order
    
    return None, -1, total_exploration_order


if __name__ == "__main__":
    # --- Bloco de Execução Principal ---
    
    # 1. Configuração do Grafo de Exemplo
    # Este grafo é desenhado para destacar a fraqueza da DFS: um ramo muito
    # profundo (A -> X1 -> ...) é explorado antes de um ramo raso (A -> B -> E).
    graph_example: Graph = {}
    
    depth_chain_len = 15
    chain_nodes = [f"X{i}" for i in range(1, depth_chain_len + 1)]
    for i in range(len(chain_nodes)):
        if i < len(chain_nodes) - 1:
            graph_example[chain_nodes[i]] = [chain_nodes[i+1]]

    graph_example["A"] = [chain_nodes[0], "B"]
    graph_example["B"] = ["C", "E"]
    graph_example["C"] = ["D"]
    
    all_nodes = ["A", "B", "C", "D", "E"] + chain_nodes
    for node in all_nodes:
        graph_example.setdefault(node, [])

    # 2. Definição dos Nós de Início e Fim
    start = "A"
    goal = "E"
    print(f"PONTO INICIAL: {start}, OBJETIVO: {goal}\n")
    
    # 3. Execução e Análise da DFS
    print("----- Executando DFS -----")
    path_dfs, order_dfs = depth_first_search(graph_example, start, goal)
    if path_dfs:
        print(f"Caminho final da DFS: {' -> '.join(path_dfs)}")
    else:
        print("DFS não encontrou o objetivo.")
    print("\nTrilha completa de exploração da DFS (nós visitados na sequência):")
    print(' -> '.join(order_dfs))
    print(f"\nTotal de nós explorados pela DFS: {len(order_dfs)}\n")

    # 4. Execução e Análise da IDS
    print("----- Executando IDS -----")
    path_ids, depth_found, order_ids = iterative_deepening_search(graph_example, start, goal, max_depth=10)
    if path_ids:
        print(f"IDS encontrou o objetivo '{goal}' na profundidade L={depth_found}")
        print(f"Caminho final do IDS: {' -> '.join(path_ids)}")
    else:
        print("IDS não encontrou o objetivo até o limite máximo.")
    print("\nTrilha completa de exploração do IDS (concatenação das iterações L=0, L=1...):")
    print(' -> '.join(order_ids))
    print(f"\nTotal de nós (com repetições) nas iterações IDS: {len(order_ids)}\n")

    # 5. Comparação Final
    print("--- Comparação ---")
    print(f"Nós explorados (DFS): {len(order_dfs)}")
    print(f"Nós explorados (IDS com repetições): {len(order_ids)}")
