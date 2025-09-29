# ids.py
# Implementação simples de DLS e IDS + uma DFS para comparação
# Rode: python ids.py

from typing import List, Dict, Optional, Tuple

def dfs_recursive(start: str, goal: str, graph: Dict[str, List[str]]) -> Tuple[Optional[List[str]], List[str]]:
    """
    DFS recursiva simples (sem proteção contra ciclos).
    Retorna (caminho_encontrado ou None, ordem_explorada).
    Observação: nesta implementação assumimos um grafo sem ciclos problemáticos ou que
    a ordem dos filhos fará a DFS explorar primeiro o ramo profundo.
    """
    visited = set()
    order = []
    path = []

    def dfs(node: str) -> Optional[List[str]]:
        order.append(node)
        visited.add(node)
        path.append(node)
        if node == goal:
            return path.copy()
        for child in graph.get(node, []):
            if child not in visited:
                res = dfs(child)
                if res is not None:
                    return res
        path.pop()
        return None

    result = dfs(start)
    return result, order

def dls_trace(node: str, goal: str, graph: Dict[str, List[str]], limit: int,
              visited_in_path: Optional[set]=None, order: Optional[List[str]]=None, path: Optional[List[str]]=None) -> Optional[List[str]]:
    """
    Busca em Profundidade Limitada (DLS) que registra a ordem de nós visitados.
    visited_in_path: conjunto usado para evitar ciclos no caminho atual (entra/sai estilo).
    order: lista onde são adicionados os nós na ordem de visita.
    path: lista representando o caminho atual.
    """
    if visited_in_path is None:
        visited_in_path = set()
    if order is None:
        order = []
    if path is None:
        path = []

    order.append(node)
    if node == goal:
        return path + [node]
    if limit == 0:
        return None

    visited_in_path.add(node)
    for child in graph.get(node, []):
        if child in visited_in_path:
            continue
        path.append(node) if (not path or path[-1] != node) else None
        res = dls_trace(child, goal, graph, limit - 1, visited_in_path, order, path + [node])
        if res is not None:
            return res
    # remove o nó da marcação do caminho atual
    visited_in_path.remove(node)
    return None

def ids(start: str, goal: str, graph: Dict[str, List[str]], max_depth: int = 20) -> Tuple[Optional[List[str]], int, List[str]]:
    """
    Busca em Profundidade Iterativa (IDS).
    Retorna: (caminho, limite_em_que_encontrou, ordem_total_explorada_concat)
    ordem_total_explorada_concat é uma concatenação das ordens geradas por cada DLS (útil para visualização).
    """
    total_order = []
    for L in range(0, max_depth + 1):
        # cada DLS deve coletar sua própria ordem
        order_this_round: List[str] = []
        # Usamos um wrapper para capturar a ordem do dls_trace
        def dls_wrapper(node, goal, graph, limit):
            # usamos listas/conjuntos para capturar a ordem do dls_trace interno
            visited_set = set()
            order_local: List[str] = []
            res = dls_trace(node, goal, graph, limit, visited_set, order_local, [])
            return res, order_local

        res, order_this_round = dls_wrapper(start, goal, graph, L)
        # adiciona a ordem (mantemos como sequência, não removemos repetições)
        total_order.extend(order_this_round)
        if res is not None:
            # encontrou solução na profundidade L
            # reconstruir o caminho de forma limpa com um “parent” estilo BFS em uma DFS limitada seria complexo aqui;
            # mas o dls_trace retorna o caminho quando encontra (no wrapper o res já é a lista do caminho)
            return res, L, total_order
    return None, -1, total_order

if __name__ == "__main__":
    # Grafo de Exemplo:
    # A tem um ramo profundo (X1 -> X2 -> ... -> X15) e também um ramo raso via B -> E (objetivo)
    # A ordem dos filhos em A faz a DFS explorar primeiro o ramo profundo -> "gasta tempo"
    graph_example: Dict[str, List[str]] = {}

    # cria a cadeia profunda X1..X15
    depth_chain_len = 15
    chain_nodes = [f"X{i}" for i in range(1, depth_chain_len + 1)]
    for i in range(len(chain_nodes)):
        if i < len(chain_nodes) - 1:
            graph_example[chain_nodes[i]] = [chain_nodes[i+1]]
        else:
            graph_example[chain_nodes[i]] = []  # fim da cadeia

    # construindo a árvore principal
    graph_example["A"] = [chain_nodes[0], "B"]
    graph_example["B"] = ["C", "E"]  
    graph_example["C"] = ["D"]
    graph_example["D"] = []
    graph_example["E"] = []

    # garantir que todos os nós existam no dicionário
    for n in ["A", "B", "C", "D", "E"] + chain_nodes:
        graph_example.setdefault(n, [])

    start = "A"
    goal = "E"

    print("PONTO INICIAL DA ÁRVORE:", start)
    print("OBJETIVO (NÓ ALVO):", goal)
    print("\nGrafo de exemplo (resumo):")
    print("A ->", graph_example["A"])
    print("B ->", graph_example["B"])
    print(f"Ramo profundo: {chain_nodes[0]} -> ... -> {chain_nodes[-1]} (len = {depth_chain_len})")
    print("\n--- Executando DFS (recursiva) ---")
    path_dfs, order_dfs = dfs_recursive(start, goal, graph_example)
    if path_dfs:
        print("DFS encontrou caminho:", path_dfs)
    else:
        print("DFS não encontrou o objetivo (ou demorou demais).")
    print("Ordem explorada pela DFS (primeiros 50 nós):", order_dfs[:50])
    print(f"Total de nós explorados pela DFS: {len(order_dfs)}")

    print("\n--- Executando IDS ---")
    path_ids, depth_found, order_ids = ids(start, goal, graph_example, max_depth=10)
    if path_ids:
        print(f"IDS encontrou o objetivo '{goal}' no limite L={depth_found}")
        print("Caminho IDS:", path_ids)
    else:
        print("IDS não encontrou o objetivo até o limite máximo.")
    print("Ordem IDS (concatenação das iterações):", order_ids[:200])
    print(f"Total de nós (contando repetições) nas iterações IDS: {len(order_ids)}")

    print("\n--- Comparação simples ---")
    print("DFS explorou (nós):", len(order_dfs))
    print("IDS explorou (nós com repetições):", len(order_ids))
    print("\nObservação: A DFS explorou primeiro o ramo profundo, visitando muitos nós X1..Xn antes de voltar e encontrar B->E.")
    print("A IDS localizou E em L pequeno (2) sem explorar a cadeia profunda acima desse nível.")
