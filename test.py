from operator import itemgetter


# REF: [i for i, j in enumerate(a) if j == max(a)]

# list = [1, 2, 7, 4, 5, 2, 6, 2, 2, 1, 7, 3]  # 2,10
#
# result = []
# for i, j in enumerate(list):
#     if j == max(list):
#         result.append(i)
# print(result)


list = [(0, 5), (1, 10), (2, 10)]  # (1,10),(2,10)

result = []
for i, j in enumerate(list):
    # print j[1]
    print(max(list, key=itemgetter(1)))
    if j[1] == max(list, key=itemgetter(1))[1]:
        result.append(j)
print(result)
