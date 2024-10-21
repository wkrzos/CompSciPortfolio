def smith_waterman(seq1, seq2, match_score, mismatch_penalty, gap_penalty):
    # Initialize the scoring matrix
    matrix = [[0] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]
    
    # Fill the scoring matrix
    max_score = 0
    max_pos = (0, 0)
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            delete = matrix[i - 1][j] + gap_penalty
            insert = matrix[i][j - 1] + gap_penalty
            matrix[i][j] = max(0, match, delete, insert)
            
            # Track the position of the maximum score
            if matrix[i][j] > max_score:
                max_score = matrix[i][j]
                max_pos = (i, j)
    
    # Traceback to find the alignment
    align1 = ""
    align2 = ""
    i, j = max_pos
    while matrix[i][j] != 0:
        if matrix[i][j] == matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty):
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif matrix[i][j] == matrix[i - 1][j] + gap_penalty:
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1
    
    return align1, align2, max_score

# Example usage
seq1 = "ACGTACGATCATGCAGTCA"
seq2 = "ACGACGTCAGGTTTCCGGG"
match_score = 1
mismatch_penalty = -1
gap_penalty = -2

alignment = smith_waterman(seq1, seq2, match_score, mismatch_penalty, gap_penalty)
align1, align2, score = alignment

print("Alignment:")
print(align1)
print(align2)
print("Score:", score)
