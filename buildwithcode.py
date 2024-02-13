import pickle
with open('./map/rooftop.pkl', 'rb') as f:
    rooftop = pickle.load(f)

# for j in range(248, 281):
#     map_data[247][j] = [(102, k) for k in range(30)]
#     map_data[252][j] = []
#     map_data[352][j] = [(102, k) for k in range(30)]
# for i in range(247, 353):
#     map_data[i][248] = [(102, k) for k in range(30)]
#     map_data[i][280] = [(102, k) for k in range(30)]
# for i in range(248, 352):
#     for j in range(249, 280):
#         map_data[i][j] = [(102, 29)]

# for j in range(249+2, 351-2+1):
    # rooftop[326][j] = [(102, k) for k in range(13)]
#     rooftop[326][j].clear()

for j in range(249+2, 351-2+1):
    for i in range(274, 326+1):
        # rooftop[i][j].clear()
        num = 39 - abs(i-300)
        rooftop[i][j] = [(102, 0), (102, num-1)]

# for j in [249, 250, 350, 351]:
#     for i in range(274, 326+1):
#         # rooftop[i][j].clear()
#         num = 39 - abs(i-300)
#         rooftop[i][j] = [(102, k) for k in range(num)]

# for j in [298, 299, 300, 301, 302]:
#     for i in range(274, 326+1):
#         # # rooftop[i][j].clear()
#         # num = 39 - abs(i-300)
#         # rooftop[i][j] = [(102, k) for k in range(num)]
#         rooftop[i][j] = [(102, k) for k in range(1)]

# for j in range(298, 302+1):
#     for i in range(274, 326+1):
#         # rooftop[i][j].clear()
#         num = 39 - abs(i-300)
#         rooftop[i][j] = [(102, k) for k in range(num)]

# for j in range(298, 302+1):
#     for i in range(274, 326+1):
#         # rooftop[i][j].pop(0)
#         rooftop[i][j].insert(0, (102, 0))

# for j in range(298, 302+1):
#     for i in range(274, 326+1):
#         rooftop[i][j] = rooftop[i][j][8:]

        
with open('./map/rooftop.pkl', 'wb') as f:
    pickle.dump(rooftop, f, protocol=pickle.HIGHEST_PROTOCOL)

# [249, 250, 350, 351]