"""
The length of the longest possible sequence such that all age, height, and weight are in decreasing order
"""

"""
(80, 200, 90)
(55, 170, 70)
(18, 160, 50)
"""

# P = [(22, 180, 80), (18, 160, 50), (80, 200, 90), (55, 170, 70), (22, 180, 80)]
P = [(22, 180, 80), (18, 160, 50)]

def longest_sequence(P):
    P.sort()
    print(P)
    LIS = [1] * len(P)
    for i in range(1, len(P)):
        for j in range(i):
            if P[i][0] > P[j][0] and P[i][1] > P[j][1] and P[i][2] > P[j][2]:
                LIS[i] = max(LIS[i], 1 + LIS[j])

    return max(LIS)


print(longest_sequence(P))