import pickle

with open('./idtime.pkl', 'rb') as f:
    idtime = pickle.load(f)

# idtime.clear()

with open('./idtime.pkl', 'wb') as f:
    pickle.dump(idtime, f, protocol=pickle.HIGHEST_PROTOCOL)