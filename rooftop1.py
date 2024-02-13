import pickle
with open('./rooftop.pkl', 'rb') as f:
    rooftop = pickle.load(f)

for i in range(149, 451+1):
    for j in range(249, 351+1):
        num = 3 if (i in [149, 150, 450, 451] or j in [249, 250, 350, 351]) else 1
        rooftop[i][j] = [(102, k) for k in range(num)]

with open('./rooftop.pkl', 'wb') as f:
    pickle.dump(rooftop, f, protocol=pickle.HIGHEST_PROTOCOL)