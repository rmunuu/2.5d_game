import pickle

with open('./id-time.pkl', 'wb') as f:
    pickle.dump([], f, protocol=pickle.HIGHEST_PROTOCOL)

import pickle

with open('./idtime.pkl', 'rb') as f:
    idtime = pickle.load(f)