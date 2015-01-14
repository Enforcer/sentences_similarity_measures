
def lcseq(s1, s2):
    m, n = len(s1), len(s2)
    L = [[0] * (n + 1), [0] * (n + 1)]
    Imax = 0
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                L[1][j + 1] = 1 + L[0][j]
                if L[1][j + 1] > Imax:
                    Imax = L[1][j + 1]
                    p1 = i - Imax + 1
                    p2 = j - Imax + 1
            else:
                L[1][j + 1] = 0
        for j in range(n + 1):
            L[0][j] = L[1][j]

    return (s1[p1:p1+Imax])


def lcs(s1, s2):
    """
    Najdłuższy wspólny (niekoniecznie spójny!) podciąg
    """
    m, n = len(s1), len(s2)
    L = [[0] * (n + 1)] + [[0] + [None] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                L[i + 1][j + 1] = 1 + L[i][j]
            else:
                L[i + 1][j + 1] = max(L[i + 1][j], L[i][j + 1])

    slcs = []
    i, j = m - 1, n - 1
    while i >= 0 and j >= 0:
        if s1[i] == s2[j]:
            slcs.append(s1[i])
            i -= 1
            j -= 1
        else:
            if L[i + 1][j] > L[i][j + 1]:
                j -= 1
            else:
                i -= 1
    slcs.reverse()
    return slcs

print(lcs('ALIBABA', 'KALIMALBA'))

s1 = ['al', 'ko', 'atrakcyjn', 'głos']
s2 = ['michalina', 'atrakcyjn', 'głos', 'psa']

s1 = ['radoś', 'wyb', 'górs', 'wyciecz']
s2 = ['radoś', 'byśmy', 'wyb', 'górs', 'wyciecz']

print('LCS: ', lcs(s1, s2), len(lcs(s1, s2)) / len(s2))

#print(lcs('abce', 'fbcfesee'))

#print(lcseq('AAABBA', 'ABAABBAAA'))
print('LCSEQ: ', lcseq(s1, s2), len(lcseq(s1, s2)) / len(s2))
#print(lcseq('ALIBABA', 'KALIMALBA'))
