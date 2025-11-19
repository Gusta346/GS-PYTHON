# Otimização de Portfólio de Projetos (Knapsack 0/1)

## Integrantes
Gustavo Oliveira Ribeiro - RM - 559163  
Augusto Douglas -   
Gabriel Vasquez -  

## Descrição
Este projeto implementa quatro abordagens para resolver o problema de seleção ótima de projetos com capacidade limitada de Horas-Especialista. É um mapeamento direto do Problema da Mochila 0/1 (0/1 Knapsack Problem).

### Objetivo
Dada uma lista de projetos (valor e horas requeridas) e uma capacidade máxima de horas, escolher o subconjunto que maximiza o valor total sem exceder a capacidade.

## Abordagens Implementadas
1. Greedy (`greedy_knapsack`): Ordena por razão Valor/Horas (não garante ótimo).
2. Recursiva Pura (`recursive_knapsack`): Explora todas as combinações (exponencial).
3. Recursiva com Memoização (`memoized_knapsack`): Top-Down armazenando subproblemas.
4. Bottom-Up Iterativa (`bottom_up_knapsack`): Tabela dinâmica para construir solução ótima.

Cada função retorna `(valor_maximo, lista_de_projetos_selecionados)`.

## Complexidades
| Abordagem | Tempo | Espaço | Observação |
|-----------|-------|--------|------------|
| Greedy | O(n log n) | O(n) | Não garante ótimo |
| Recursiva Pura | O(2^n) | O(n) | Redundância alta |
| Memoização | O(n * C) | O(n * C) | Elimina recomputações |
| Bottom-Up | O(n * C) | O(n * C) | Pode reduzir para O(C) se só valor |

## Caso onde Greedy falha
Capacidade 50; itens: (60,10), (100,20), (120,30). Greedy pega 60+100=160. Ótimo é 100+120=220.

## Requisitos Atendidos
- Quatro funções separadas e documentadas.
- Comentários com lógica e complexidade.
- Demonstração de falha do método Guloso.
- Testes automáticos embutidos (5 cenários) incluindo caso de falha.

## Execução
Pré-requisito: Python 3.10+ (qualquer versão recente deve funcionar).

Para executar:
```bash
python gspython.py
```
O script rodará os casos de teste e exibirá os resultados de cada abordagem.

## Estrutura
```
GS/
 ├─ gspython.py   # Código principal com quatro abordagens e testes
 └─ README.md     # Este arquivo de documentação
```




