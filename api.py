from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from mysql import connector
import pickle
import sys
import numpy as np
from config import *


def con_curr():
    con = connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    curr = con.cursor(buffered=True)
    return curr


def top_5(name, other_names):
    vect = pickle.load(open(vector_path, "rb"))
    name = vect.transform(name)
    other_names = [i[0] for i in other_names]
    other_names = vect.transform(other_names)
    cosine = cosine_similarity(name, other_names)
    ans[np.where(ans > 0.65)] = 0.
    idx = ans.argsort()[0][-5:][::-1]
    result = [other_names[i][0] for i in idx]
    return reult
    

if __name__ == '__main__':
    curr = con_curr()
    curr.execute('SELECT content FROM table where id={}'.format(sys.argv[1]))
    name = curr.fetchone()
    curr.execute('SELECT content FROM table')
    other_names = curr.fetchall()
  
    top_5(name, other_names)