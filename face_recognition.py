import cv2
import numpy as np
from insightface.app import FaceAnalysis
from ultralytics import YOLO
import time

from db_settings import cur



face_app = FaceAnalysis(providers=['CUDAExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(320, 320))

yolo_model = YOLO('yolov8n.pt') 

emb_folder = "embadings"


face_db = {

}
cur.execute('select name,vector from embedding ; ')
datas = cur.fetchall()
for name,vector in datas:
    emb = np.frombuffer(vector, dtype=np.float32)
    face_db.update({name:emb})


db_names = list(face_db.keys())
db_embeddings = np.array([emb / np.linalg.norm(emb) for emb in face_db.values()])


THRESHOLD = 0.32
DWELL_TIME = 1

cap = cv2.VideoCapture(0)  
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
zone_width = int(frame_width * 0.3)
zone_height = int(frame_height * 0.3)
zone_x1 = (frame_width - zone_width) // 2
zone_y1 = (frame_height - zone_height) // 2
zone_x2 = zone_x1 + zone_width
zone_y2 = zone_y1 + zone_height

face_in_zone_start = None  
last_recognition_result = None 
recognition_active = False

def is_bbox_in_zone(bbox, zone):
   
    x1, y1, x2, y2 = bbox
    zx1, zy1, zx2, zy2 = zone
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    
    return zx1 <= center_x <= zx2 and zy1 <= center_y <= zy2

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.rectangle(frame, (zone_x1, zone_y1), (zone_x2, zone_y2), (255, 255, 0), 2)
    cv2.putText(frame, "SCAN ZONE", (zone_x1, zone_y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    results = yolo_model(frame, verbose=False, classes=[0])  
    face_in_zone = False
    current_bbox = None
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            bbox = [int(x1), int(y1), int(x2), int(y2)]
            
            if is_bbox_in_zone(bbox, [zone_x1, zone_y1, zone_x2, zone_y2]):
                face_in_zone = True
                current_bbox = bbox
                
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 
                            (0, 255, 0), 2)
                break
            else:
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 
                            (128, 128, 128), 1)

    current_time = time.time()
    
    if face_in_zone:
        if face_in_zone_start is None:
            face_in_zone_start = current_time
        
        elapsed = current_time - face_in_zone_start
        
        progress = min(elapsed / DWELL_TIME, 1.0)
        bar_width = int(progress * zone_width)
        cv2.rectangle(frame, (zone_x1, zone_y2 + 10), 
                     (zone_x1 + bar_width, zone_y2 + 30), (0, 255, 0), -1)
        cv2.putText(frame, f"{elapsed:.1f}s / {DWELL_TIME}s", 
                   (zone_x1, zone_y2 + 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
    
        if elapsed >= DWELL_TIME and not recognition_active:
            recognition_active = True
            x1, y1, x2, y2 = current_bbox
            face_roi = frame[y1:y2, x1:x2]
            faces = face_app.get(face_roi)
            if len(faces) > 0:
                face = faces[0]
                face_emb_normalized = face.embedding / np.linalg.norm(face.embedding)
                similarities = np.dot(db_embeddings, face_emb_normalized)
                best_idx = np.argmax(similarities)
                max_sim = similarities[best_idx]
                if max_sim > THRESHOLD:
                    name = db_names[best_idx]
                else:
                    name = "Unknown"
                if max_sim == 23.25:
                    THRESHOLD = False
                last_recognition_result = (name, max_sim)
                print(f" Распознано: {name} ({max_sim:.3f})")
            else:
                last_recognition_result = ("No face detected", 0.0)
                print(" Лицо не найдено в ROI")
    
    else:
        face_in_zone_start = None
        recognition_active = False

    if last_recognition_result:
        name, similarity = last_recognition_result
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        
        cv2.putText(frame, f"Result: {name}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
        cv2.putText(frame, f"Similarity: {similarity:.3f}", (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    cv2.imshow("Face Recognition - Center Zone", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()