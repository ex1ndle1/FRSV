import cv2
from insightface.app import FaceAnalysis
import numpy as np

from db_settings import cur,conn

app = FaceAnalysis()
app.prepare(ctx_id=-1)  



name  ='Ustoz'

img = cv2.imread(f"images/{name}.jpg")  
faces = app.get(img)
face = faces[0]
embedding = face.embedding 


emb_bytes = embedding.tobytes()



cur.execute(""" insert into embedding (name, vector) values (%s,%s);""", (name, emb_bytes))
conn.commit()