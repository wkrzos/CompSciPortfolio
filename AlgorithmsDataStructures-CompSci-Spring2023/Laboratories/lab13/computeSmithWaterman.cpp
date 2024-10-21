#include <iostream>
#include <vector>

using namespace std;

// Function to calculate the maximum of three integers
int max3(int a, int b, int c) {
    return max(max(a, b), c);
}

// Function to perform the Mg Smith-Waterman algorithm
void mgSmithWaterman(const string& seq1, const string& seq2, int gapPenalty, int matchScore, int mismatchPenalty) {
    int m = seq1.length(); // Length of sequence 1
    int n = seq2.length(); // Length of sequence 2

    // Create and initialize the scoring matrix
    vector<vector<int>> score(m + 1, vector<int>(n + 1, 0));

    // Initialize variables to store the maximum score and its position
    int maxScore = 0;
    int maxI = 0;
    int maxJ = 0;

    // Calculate the scores
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (seq1[i - 1] == seq2[j - 1]) {
                // Match
                score[i][j] = max3(0, score[i - 1][j - 1] + matchScore, score[i - 1][j] + gapPenalty, score[i][j - 1] + gapPenalty);
            } else {
                // Mismatch
                score[i][j] = max3(0, score[i - 1][j - 1] + mismatchPenalty, score[i - 1][j] + gapPenalty, score[i][j - 1] + gapPenalty);
            }

            // Update the maximum score and its position
            if (score[i][j] > maxScore) {
                maxScore = score[i][j];
                maxI = i;
                maxJ = j;
            }
        }
    }

    // Traceback to find the alignment
    string alignmentSeq1, alignmentSeq2;
    int i = maxI;
    int j = maxJ;

    while (i > 0 && j > 0 && score[i][j] != 0) {
        if (seq1[i - 1] == seq2[j - 1]) {
            alignmentSeq1 = seq1[i - 1] + alignmentSeq1;
            alignmentSeq2 = seq2[j - 1] + alignmentSeq2;
            --i;
            --j;
        } else if (score[i][j] == score[i - 1][j - 1] + mismatchPenalty) {
            alignmentSeq1 = seq1[i - 1] + alignmentSeq1;
            alignmentSeq2 = seq2[j - 1] + alignmentSeq2;
            --i;
            --j;
        } else if (score[i][j] == score[i - 1][j] + gapPenalty) {
            alignmentSeq1 = seq1[i - 1] + alignmentSeq1;
            alignmentSeq2 = '-' + alignmentSeq2;
            --i;
        } else if (score[i][j] == score[i][j - 1] + gapPenalty) {
            alignmentSeq1 = '-' + alignmentSeq1;
            alignmentSeq2 = seq2[j - 1] + alignmentSeq2;
            --j;
        }
    }

    // Print the alignment
    cout << "Alignment:\n";
    cout << alignmentSeq1 << endl;
    cout << alignmentSeq2 << endl;

    // Print the maximum score
    cout << "Max Score: " << maxScore << endl;
}

int main() {
    string sequence1 = "AGTACGCA";
    string sequence2 = "TATGC";

    int gapPenalty = -2;
    int matchScore = 2;
    int mismatchPenalty = -1;

    mgSmithWaterman(sequence1, sequence2, gapPenalty, matchScore, mismatchPenalty);

    return 0;
}
