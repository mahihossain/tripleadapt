"""
Returns the longest common subsequence of two strings
"""


def lcs(str1, str2):
    """
            Returns the longest common subsequence of two strings

            Parameters
            ----------
            str1: string list
            str2: string list


            Returns
            -------
            string
                the longest common string


            """
    a = len(str1)
    b = len(str2)
    string_matrix = [[0 for _ in range(b + 1)] for _ in range(a + 1)]
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            if str1[i - 1] == str2[j - 1]:
                string_matrix[i][j] = 1 + string_matrix[i - 1][j - 1]
            else:
                string_matrix[i][j] = max(string_matrix[i - 1][j], string_matrix[i][j - 1])
    index = string_matrix[a][b]
    res = [""] * index
    i = a
    j = b
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            res[index - 1] = str1[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif string_matrix[i - 1][j] > string_matrix[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return res
