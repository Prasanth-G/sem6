import numpy
import collections

arr = numpy.array([ [5, 0, 3, 0, 0, 2],
                    [1, 5, 0, 2, 0, 2],
                    [0, 0, 0, 2, 3, 4],
                    [1, 4, 0, 0, 1, 2]])

rating = arr.copy()
m, n = arr.shape
k = 3


similarity_matrix = arr.T.dot(arr)

for i in range(similarity_matrix.shape[0]):
    similarity_matrix[i][i] = 0

for user in range(m):
    for item in range(n):
        if arr[user][item] == 0:
            # max n similarity of item
            index = collections.defaultdict(lambda : [])
            for i in range(len(similarity_matrix[item])):
                each = similarity_matrix[item][i]
                index[each].append(i)
            temp_sm = sorted(similarity_matrix[item], reverse=True)[0:k]
            numerator_sum = 0
            denominator_sum = 0
            for each in temp_sm:
                i = index[each].pop()
                numerator_sum  = numerator_sum + ( arr[user][i] * each )
                denominator_sum = denominator_sum + each
            #print(numerator_sum, denominator_sum)
            rating[user][item] = numerator_sum/ denominator_sum
            #print(user, item, arr[user].dot(similarity_matrix[item]), sum(similarity_matrix[item]), sum(arr[user]))
            #rating[user][item] = numpy.dot( arr[user], similarity_matrix[item]) / sum(similarity_matrix[item])


print(rating)