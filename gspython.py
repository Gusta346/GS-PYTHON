"""
Otimização de Portfólio de Projetos (Problema da Mochila 0/1)
============================================================

Este arquivo implementa quatro abordagens distintas para resolver o problema
de seleção ótima de projetos dada uma capacidade máxima de Horas-Especialista.

Fases / Funções:
1. greedy_knapsack       -> Estratégia Gulosa por maior razão Valor/Horas (não garante ótimo)
2. recursive_knapsack    -> Recursão pura (explora todas as combinações) O(2^n)
3. memoized_knapsack     -> Recursão Top-Down com Memoização O(n*C)
4. bottom_up_knapsack    -> Programação Dinâmica Iterativa (Bottom-Up) O(n*C)

Cada função retorna: (valor_maximo, lista_de_projetos_escolhidos)

Complexidades Teóricas:
-----------------------
1. Greedy (razão V/E):
   Tempo: O(n log n) devido à ordenação (ou O(n) se usar seleção linear aproximada)
   Espaço: O(n) para lista ordenada.
   Observação: Não garante solução ótima no Knapsack 0/1.

2. Recursiva Pura:
   Tempo: O(2^n) (cada item pode ser incluído ou não; alta redundância de subproblemas)
   Espaço: O(n) profundidade de pilha.

3. Recursiva com Memoização (Top-Down):
   Tempo: O(n * C) onde n = número de projetos, C = capacidade.
		  Cada subproblema (i, capacidade_restante) é resolvido uma única vez.
   Espaço: O(n * C) para dicionário/matriz + O(n) de pilha.

4. Bottom-Up Iterativa:
   Tempo: O(n * C)
   Espaço: O(n * C) para a tabela. (Pode ser reduzido para O(C) apenas para valor máximo,
		  mas aqui mantemos a tabela completa para fins educacionais e reconstrução de solução.)

Critério de Falha da Abordagem Gulosa:
-------------------------------------
Caso clássico onde Guloso falha (por razão V/E):
Capacidade = 50
Itens:
  X1: valor=60, horas=10 (razão 6.0)
  X2: valor=100, horas=20 (razão 5.0)
  X3: valor=120, horas=30 (razão 4.0)
Guloso pega X1, X2 -> valor=160, mas ótimo é X2 + X3 = 220.

"""

from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class Project:
	name: str
	value: int  # Valor (lucro / impacto)
	hours: int  # Horas-Especialista requeridas (custo)


def greedy_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[Project]]:
	"""Estratégia Gulosa por maior razão valor/horas.

	NÃO garante a solução ótima para o problema 0/1 Knapsack.

	Critério: ordenar projetos por (valor / horas) desc e incluir enquanto couber.

	Args:
		projects: Lista de projetos.
		capacity: Capacidade total de horas especialista.
	Returns:
		(valor_total, lista_de_projetos_selecionados)
	Complexidade:
		Tempo: O(n log n) pela ordenação.
		Espaço: O(n) para lista ordenada.
	"""
	if capacity <= 0 or not projects:
		return 0, []

	sorted_projects = sorted(projects, key=lambda p: p.value / p.hours, reverse=True)
	total_value = 0
	chosen: List[Project] = []
	remaining = capacity
	for p in sorted_projects:
		if p.hours <= remaining:
			chosen.append(p)
			total_value += p.value
			remaining -= p.hours
	return total_value, chosen


def recursive_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[Project]]:
	"""Recursão pura explorando todas as combinações (sem memoização).

	Args:
		projects: Lista de projetos.
		capacity: Capacidade disponível.
	Returns:
		(valor_maximo, lista_de_projetos)
	Complexidade:
		Tempo: O(2^n)
		Espaço: O(n) profundidade de pilha.
	"""
	n = len(projects)

	def solve(i: int, remaining: int) -> Tuple[int, List[Project]]:
		# Caso base: sem itens ou sem capacidade.
		if i == n or remaining <= 0:
			return 0, []

		# Opção 1: não incluir projeto atual.
		value_without, list_without = solve(i + 1, remaining)

		# Opção 2: incluir se couber.
		project = projects[i]
		value_with = -1
		list_with: List[Project] = []
		if project.hours <= remaining:
			sub_value, sub_list = solve(i + 1, remaining - project.hours)
			value_with = sub_value + project.value
			list_with = [project] + sub_list

		# Escolher melhor.
		if value_with > value_without:
			return value_with, list_with
		else:
			return value_without, list_without

	return solve(0, capacity)


def memoized_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[Project]]:
	"""Recursão Top-Down com Memoização.

	Usa dicionário para armazenar subproblemas: chave (i, remaining) -> (value, list)

	Args:
		projects: Lista de projetos.
		capacity: Capacidade disponível.
	Returns:
		(valor_maximo, lista_de_projetos)
	Complexidade:
		Tempo: O(n * C)
		Espaço: O(n * C)
	"""
	n = len(projects)
	memo: Dict[Tuple[int, int], Tuple[int, List[Project]]] = {}

	def solve(i: int, remaining: int) -> Tuple[int, List[Project]]:
		if i == n or remaining <= 0:
			return 0, []
		key = (i, remaining)
		if key in memo:
			return memo[key]

		# Não incluir
		value_without, list_without = solve(i + 1, remaining)

		# Incluir se couber
		project = projects[i]
		value_with = -1
		list_with: List[Project] = []
		if project.hours <= remaining:
			sub_value, sub_list = solve(i + 1, remaining - project.hours)
			value_with = sub_value + project.value
			list_with = [project] + sub_list

		best = (value_with, list_with) if value_with > value_without else (value_without, list_without)
		memo[key] = best
		return best

	return solve(0, capacity)


def bottom_up_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[Project]]:
	"""Programação Dinâmica Iterativa (Bottom-Up).

	Constrói tabela T de dimensões (n+1) x (capacity+1), onde:
		T[i][c] = valor máximo usando os primeiros i projetos com capacidade c.

	Args:
		projects: Lista de projetos.
		capacity: Capacidade total disponível.
	Returns:
		(valor_maximo, lista_de_projetos)
	Complexidade:
		Tempo: O(n * C)
		Espaço: O(n * C)
	"""
	n = len(projects)
	# Tabela de valores
	T = [[0] * (capacity + 1) for _ in range(n + 1)]

	for i in range(1, n + 1):
		p = projects[i - 1]
		for c in range(0, capacity + 1):
			# Não incluir
			best = T[i - 1][c]
			# Incluir se couber
			if p.hours <= c:
				cand = T[i - 1][c - p.hours] + p.value
				if cand > best:
					best = cand
			T[i][c] = best

	# Reconstrução da solução ótima
	chosen: List[Project] = []
	c = capacity
	for i in range(n, 0, -1):
		if T[i][c] != T[i - 1][c]:  # item i-1 foi usado
			p = projects[i - 1]
			chosen.append(p)
			c -= p.hours
	chosen.reverse()
	return T[n][capacity], chosen


def _format_solution(title: str, result: Tuple[int, List[Project]]) -> str:
	value, chosen = result
	names = [p.name for p in chosen]
	return f"{title}: valor={value}, projetos={names}"


def run_tests():
	"""Executa múltiplos casos de teste para validar as abordagens.

	Inclui caso onde Greedy falha.
	"""
	# Caso exemplo fornecido
	projects_example = [
		Project("A", 12, 4),
		Project("B", 10, 3),
		Project("C", 7, 2),
		Project("D", 4, 3),
	]
	cap_example = 10
	optimal_value_example = 29  # A+B+C

	# Caso onde greedy falha
	projects_fail = [
		Project("X1", 60, 10),
		Project("X2", 100, 20),
		Project("X3", 120, 30),
	]
	cap_fail = 50
	optimal_value_fail = 220  # X2 + X3

	# Caso vazio
	projects_empty: List[Project] = []
	cap_empty = 10
	optimal_value_empty = 0

	# Capacidade menor que qualquer projeto
	projects_small = [Project("P1", 5, 4), Project("P2", 6, 5)]
	cap_too_small = 3
	optimal_value_small = 0

	# Outro caso adicional
	projects_extra = [Project("P1", 6, 4), Project("P2", 5, 3), Project("P3", 4, 2)]
	cap_extra = 5
	optimal_value_extra = 9  # P2 + P3

	test_scenarios = [
		("Exemplo Aula", projects_example, cap_example, optimal_value_example),
		("Greedy Falha", projects_fail, cap_fail, optimal_value_fail),
		("Lista Vazia", projects_empty, cap_empty, optimal_value_empty),
		("Capacidade Insuficiente", projects_small, cap_too_small, optimal_value_small),
		("Caso Extra", projects_extra, cap_extra, optimal_value_extra),
	]

	for label, proj_list, cap, expected in test_scenarios:
		greedy_val, _ = greedy_knapsack(proj_list, cap)
		rec_val, _ = recursive_knapsack(proj_list, cap)
		memo_val, _ = memoized_knapsack(proj_list, cap)
		bottom_val, _ = bottom_up_knapsack(proj_list, cap)

		print(f"===== {label} =====")
		print(f"Capacidade={cap}, Esperado Ótimo={expected}")
		print(_format_solution("Greedy", greedy_knapsack(proj_list, cap)))
		print(_format_solution("Recursivo", recursive_knapsack(proj_list, cap)))
		print(_format_solution("Memoizado", memoized_knapsack(proj_list, cap)))
		print(_format_solution("Bottom-Up", bottom_up_knapsack(proj_list, cap)))
		# Valida ótimos para abordagens DP/recursão
		assert rec_val == expected, f"Recursivo falhou em {label}"
		assert memo_val == expected, f"Memoizado falhou em {label}"
		assert bottom_val == expected, f"Bottom-Up falhou em {label}"
		# Greedy pode falhar somente no caso 'Greedy Falha'
		if label != "Greedy Falha":
			assert greedy_val == expected, f"Greedy deveria acertar neste caso: {label}"
		else:
			assert greedy_val != expected, "Greedy deveria falhar neste caso de teste."  # demonstra falha
		print("OK\n")


def main():
	print("Executando testes das quatro abordagens de Otimização de Portfólio...\n")
	run_tests()
	print("Todos os testes concluídos com sucesso.")


if __name__ == "__main__":
	main()

