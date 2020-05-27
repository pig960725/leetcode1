# import random
# import pprint
#
# def soultion(n:dict):
#     max_color = max(n, key=n.get)
#     max_number = n[max_color]
#     n[max_color] = 0
#     ballon_list = []
#     for k in n.keys():
#         color_list = [k for i in range(n[k])]
#         ballon_list.extend(color_list)
#     if max_number> (len(ballon_list)+max_number)//2 +1:
#         raise Exception('bad')
#     random.shuffle(ballon_list)
#     for index in range(len(ballon_list)-1):
#         if ballon_list[index] == ballon_list[index+1]:
#             ballon_list[index+1] = max_color
#             max_number -= 1
#     pprint.pprint(ballon_list)

# n = {'a':10, 'b': 20, 'c': 30, 'd': 70}





