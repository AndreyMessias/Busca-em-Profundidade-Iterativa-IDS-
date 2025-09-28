# ids.py
# Implementação simples de DLS e IDS + uma DFS de comparação
# Rode: python ids.py

from typing import List, Dict, Optional, Tuple

def dfs_recursive(start: str, goal: str, graph: Dict[str, List[str]]) -> Tuple[Optional[List[str]], List[str]]:
    """
    DFS recursiva simples (sem proteção contra ciclos).
    Retorna (caminho_encontrado or None, ordem_explorada).
    Note: nesta implementação assumimos grafo sem ciclos relevantes ou que
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
    Depth-Limited Search that records the order of nodes visited.
    visited_in_path: set used to avoid cycles on current path (enter/exit style).
    order: list appended with nodes in visitation order.
    path: current path list.
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
    # remove node from current path mark
    visited_in_path.remove(node)
    return None

def ids(start: str, goal: str, graph: Dict[str, List[str]], max_depth: int = 20) -> Tuple[Optional[List[str]], int, List[str]]:
    """
    Iterative Deepening Search.
    Retorna: (caminho, limite_em_que_achou, ordem_total_explorada_concat)
    ordem_total_explorada_concat é uma concatenação das ordens geradas por cada DLS (útil para visualização).
    """
    total_order = []
    for L in range(0, max_depth + 1):
        # each DLS should collect its own order
        order_this_round: List[str] = []
        # We'll use a wrapper to capture order from dls_trace
        def dls_wrapper(node, goal, graph, limit):
            # we use lists/sets to capture order from inner dls_trace
            visited_set = set()
            order_local: List[str] = []
            res = dls_trace(node, goal, graph, limit, visited_set, order_local, [])
            return res, order_local

        res, order_this_round = dls_wrapper(start, goal, graph, L)
        # append order (we keep them as sequence, not uniquified)
        total_order.extend(order_this_round)
        if res is not None:
            # found solution at depth L
            # reconstruct path cleanly using a simple BFS-like parent during a limited DFS would be complex here;
            # but dls_trace returns the path when finds (in our wrapper res is path list)
            return res, L, total_order
    return None, -1, total_order

if __name__ == "__main__":
    # Grafo de exemplo:
    # A tem um ramo profundo (X1 -> X2 -> ... -> X15) e também um ramo raso via B -> E (objetivo)
    # Ordem de filhos em A faz DFS explorar primeiro o ramo profundo -> "gasta tempo"
    graph_example: Dict[str, List[str]] = {}

    # cria cadeia profunda X1..X15
    depth_chain_len = 15
    chain_nodes = [f"X{i}" for i in range(1, depth_chain_len + 1)]
    for i in range(len(chain_nodes)):
        if i < len(chain_nodes) - 1:
            graph_example[chain_nodes[i]] = [chain_nodes[i+1]]
        else:
            graph_example[chain_nodes[i]] = []  # fim da cadeia

    # construindo árvore principal
    # A -> X1 (ramo profundo), B (ramo raso)
    graph_example["A"] = [chain_nodes[0], "B"]
    graph_example["B"] = ["C", "E"]   # E será o objetivo, em profundidade 2 via B
    graph_example["C"] = ["D"]
    graph_example["D"] = []
    graph_example["E"] = []  # objetivo

    # garantir que todos nós existam no dicionário
    for n in ["A", "B", "C", "D", "E"] + chain_nodes:
        graph_example.setdefault(n, [])

    start = "A"
    goal = "E"

    print("Grafo de exemplo (resumo):")
    print("A ->", graph_example["A"])
    print("B ->", graph_example["B"])
    print(f"Ramo profundo: {chain_nodes[0]} -> ... -> {chain_nodes[-1]} (len = {depth_chain_len})")
    print("\n--- Executando DFS (recursiva) ---")
    path_dfs, order_dfs = dfs_recursive(start, goal, graph_example)
    if path_dfs:
        print("DFS encontrou caminho:", path_dfs)
    else:
        print("DFS não encontrou o objetivo (ou demorou demais).")
    print("DFS ordem explorada (primeiros 50 nós):", order_dfs[:50])
    print(f"Total nós explorados pela DFS: {len(order_dfs)}")

    print("\n--- Executando IDS ---")
    path_ids, depth_found, order_ids = ids(start, goal, graph_example, max_depth=10)
    if path_ids:
        print(f"IDS encontrou o objetivo '{goal}' no limite L={depth_found}")
        print("Caminho IDS:", path_ids)
    else:
        print("IDS não encontrou o objetivo até o limite máximo.")
    print("IDS ordem (concat das iterações):", order_ids[:200])
    print(f"Total nós (contagem com repetições) nas iterações IDS: {len(order_ids)}")

    # Pequena comparação direta
    print("\n--- Comparação simples ---")
    print("DFS explorou (n nós):", len(order_dfs))
    print("IDS explorou (n nós com repetições):", len(order_ids))
    print("\nObservação: A DFS explorou primeiro o ramo profundo, visitando muitos nós X1..Xn antes de voltar e encontrar B->E.")
    print("A IDS localizou E em L pequeno (2) sem explorar a cadeia profunda acima desse nível.")
