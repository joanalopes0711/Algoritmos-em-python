
import pprint
from typing import Callable


# A função dist calcula a distância entre duas sequências s1 e s2 contando o número de caracteres diferentes. Utiliza a função zip para percorrer simultaneamente os caracteres de ambas as sequências.
def dist(s1: str, s2: str) -> int:  
    return sum(1 for x1, x2 in zip(s1, s2) if x1 != x2)


# A função mat_dist_seqs cria uma matriz de distância entre todas as sequências fornecidas. Utiliza um dicionário para armazenar as distâncias entre cada par de sequências.
def mat_dist_seqs(seqs: list[str], fun_dist: Callable[[str, str], int]) -> dict[str, dict[str, int]]:
    res = {seq1: {seq2: fun_dist(seq1, seq2) for seq2 in seqs} for seq1 in seqs}
    return res

#A função mat_dist cria uma matriz de distância mais compacta, armazenando apenas as distâncias únicas entre pares de sequências. Usa dicionários aninhados para representar a matriz.
def mat_dist(seqs: list[str], fun_dist: Callable[[str, str], int]) -> dict[int, dict[int, int]]:
    res = {str(idx1): {str(idx2): fun_dist(seq1, seq2) for idx2, seq2 in enumerate(seqs) if idx2 > idx1} for idx1, seq1 in enumerate(seqs)}
    return res

# A função seqs_mais_prox encontra o par mais próximo na matriz de distância, iterando sobre todos os elementos da matriz
def seqs_mais_prox(dist: dict[int, dict[int, int]]) -> tuple[int, int]:
    menor = float('inf')
    par = None
    for idx1, D in dist.items():
        for idx2, val in D.items():
            if val < menor:
                menor = val
                par = idx1, idx2
    return par

# A função qdist retorna a distância entre dois índices em uma matriz de distância. Lida com a possibilidade de o índice não existir.
def qdist(D, idx1, idx2):
    try:
        if idx1 in D and idx2 in D[idx1]:
            return D[idx1][idx2]
        return D[idx2][idx1]
    except Exception as e:
        print(D, idx1, idx2)
        exit()

# A função nova_matriz cria uma nova matriz de distância após a fusão de dois índices (ou sequências) próximos. Remove as linhas e colunas correspondentes aos índices fundidos.
def nova_matriz(dist: dict[int, dict[int, int]], idx1: str, idx2: str) -> dict[int, dict[int, int]]:
    novo = {}
    nchave = f"{idx1}+{idx2}"
    for chave, valor in dist.items():
        if chave != idx1 and chave != idx2:
            d1 = dist[idx1][chave]
            d2 = dist[idx2][chave]
            novo[chave] = {nchave: (d1 + d2) / 2}
            for k, v in valor.items():
                if k != idx1 and k != idx2:
                    novo[chave][k] = v
    novo[nchave] = {}
    return novo

seqs = 'aatc aacc AGTT aagc agtc acgc'.upper().split()
D0 = mat_dist(seqs, dist)
I1, I2 = seqs_mais_prox(D0)
D1 = nova_matriz(D0, str(I1), str(I2))
print(I1, I2)
print(D1)

I1, I2 = seqs_mais_prox(D1)
D2 = nova_matriz(D1, str(I1), str(I2))
print(I1, I2)
print(D2)

I1, I2 = seqs_mais_prox(D2)
D3 = nova_matriz(D2, str(I1), str(I2))
print(I1, I2)
print(D3)

#deste modo aplicamos o algoritmo UPGMA em que criamos uma lista de sequências, calculamos a matriz de distância inicial (D0), encontramos pares mais próximos e criamos novas matrizes de distância até que reste apenas uma sequência. 
# Por fim, imprime os resultados de cada iteração.
