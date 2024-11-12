def max_chain_length(A, B, C, D):
    common_pairs = min(B, C)
    remaining_B = B - common_pairs
    remaining_C = C - common_pairs
    max_chain = 2 * common_pairs + A + D
    if remaining_B > 0:
        max_chain += 1
    if remaining_C > 0:
        max_chain += 1
    return max_chain

A = int(input())
B = int(input())
C = int(input())
D = int(input())

print(max_chain_length(A, B, C, D))
