from fuzzywuzzy import fuzz
import fuzzy
import numpy as np

context_char=[['J', 'Z'], ['W', 'O', 'U'], ['E', 'I'] ]

def name_matching(name1, name2):
    soundex_list=[]
    name1_l = name1.split()
    name2_l = name2.split()
    fuzz_matrix=get_fuzzy_matrix(name1_l,name2_l)
    print(fuzz_matrix)
    print(fuzz_matrix.shape)
    if(fuzz_matrix.shape[0]>fuzz_matrix.shape[1]):
        maxInColumns = np.amax(fuzz_matrix, axis=0)
        print(maxInColumns)
        row_index=fuzz_matrix.argmax(axis=0)
        print(row_index)
        avg_ratio= np.sum(maxInColumns)/ fuzz_matrix.shape[1]
        print(avg_ratio)
        for i in range(len(row_index)):
            soundex_list.append({name1_l[row_index[i]]+ ' vs ' + name2_l[i]:soundex_matching(name1_l[row_index[i]], name2_l[i])})

    else:
        maxInRows = np.amax(fuzz_matrix, axis=1)
        print(maxInRows)
        col_index = fuzz_matrix.argmax(axis=1)
        print(col_index)
        avg_ratio = np.sum(maxInRows) / fuzz_matrix.shape[0]
        print(avg_ratio)
        for i in range(len(col_index)):
            soundex_list.append({name1_l[i]+ ' vs ' + name2_l[col_index[i]]: soundex_matching(name1_l[i], name2_l[col_index[i]])})
    # print(soundex_list, avg_ratio)
    return avg_ratio, soundex_list



def fuzzy_matching(str1,str2):
    return fuzz.ratio(str1.lower(),str2.lower())

def get_fuzzy_matrix(name1, name2):
    ratio_matrix = []
    print(name1, name2)
    for i in range(len(name1)):
        temp=[]
        for j in range(len(name2)):
            temp.append(fuzzy_matching(name1[i], name2[j]))
        ratio_matrix.append(temp)
    ratio_matrix = np.array(ratio_matrix)
    return ratio_matrix

def soundex_matching(name1, name2):
    print(name1, name2)
    soundex1 = fuzzy.nysiis(name1)
    soundex2=fuzzy.nysiis(name2)
    # print(soundex1, soundex2)
    lev_distance=levenshtein(soundex1,soundex2)
    print(soundex1, soundex2, lev_distance)
    if(lev_distance==0):
        return True
    elif(lev_distance==1 and check_context_char(soundex1[0],soundex2[0])):
        return True
    else:
        return False

def check_context_char(char1, char2):
    for context in context_char:
        if(char1 in context and char2 in context):
            return True
    return False

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

if __name__ == '__main__':
    str1="md Jahid Hossain"
    str2="Md Gahid Hossen"
    avg_ratio, context = name_matching(str1, str2)
    print("Avg matching ration between '"+ str1 + "' and '" +str2 + "' : ", avg_ratio)
    print(context)


