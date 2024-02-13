# # floor_1

# import pickle
# with open('./floor_1.pkl', 'rb') as f:
#     floor_1 = pickle.load(f)

# for i in range(140, 461):
#     for j in range(240, 361):
#         if 271 < i <329:
#             continue
#         for k in range(len(floor_1[i][j])):
#             height = floor_1[i][j][k][1]
#             if height > 0: floor_1[i][j][k] = (104, height)
        

# with open('./floor_1.pkl', 'wb') as f:
#     pickle.dump(floor_1, f, protocol=pickle.HIGHEST_PROTOCOL)

# # floor_2

# import pickle
# with open('./floor_2.pkl', 'rb') as f:
#     floor_2 = pickle.load(f)

# for i in range(140, 461):
#     for j in range(240, 361):
#         if 271 < i <329 and 254 < j < 277:
#             continue
#         for k in range(len(floor_2[i][j])):
#             height = floor_2[i][j][k][1]
#             if height > 0: floor_2[i][j][k] = (4, height)
        

# with open('./floor_2.pkl', 'wb') as f:
#     pickle.dump(floor_2, f, protocol=pickle.HIGHEST_PROTOCOL)

# # floor_3

# import pickle
# with open('./floor_3.pkl', 'rb') as f:
#     floor_3 = pickle.load(f)

# for i in range(140, 461):
#     for j in range(240, 361):
#         if 273 < i <321 and 245 < j < 277:
#             continue
#         for k in range(len(floor_3[i][j])):
#             height = floor_3[i][j][k][1]
#             if height > 0: floor_3[i][j][k] = (105, height)
        

# with open('./floor_3.pkl', 'wb') as f:
#     pickle.dump(floor_3, f, protocol=pickle.HIGHEST_PROTOCOL)

# floor_4

import pickle
with open('./floor_4.pkl', 'rb') as f:
    floor_4 = pickle.load(f)

for i in range(140, 461):
    for j in range(240, 361):
        if 273 < i <321 and 245 < j < 277:
            continue
        for k in range(len(floor_4[i][j])):
            height = floor_4[i][j][k][1]
            if height > 0: floor_4[i][j][k] = (106, height)
        

with open('./floor_4.pkl', 'wb') as f:
    pickle.dump(floor_4, f, protocol=pickle.HIGHEST_PROTOCOL)