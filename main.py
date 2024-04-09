import face_recognition
import os, sys
import cv2 
import numpy as np
import math
FOLDER="faces"
def face_confidence(face_distance,face_match_threhold=0.6):
	range=(1.0-face_match_threhold)
	linear_val=(1.0-face_distance)/(range*2.0)
	if face_distance> face_match_threhold:
		return str(round(linear_val*100,2))+"%"
	else:
		value=(linear_val+((1.0-linear_val*math.pow(linear_val-0.5)*2,0.2)))*100
		return str(round(value*100,2))+"%"

class Face_recognition:
	face_locations=[]
	face_encodings=[]
	face_names=[]
	know_faces_encodngs=[]
	know_face_names=[]
	process_current_frame=1
	def __init__(self):
		pass
	def encode_faces(self):
		for image in os.lisdir(FOLDER):
			face_image=face_recognition.load_image_file(f"{FOLDER}/{image}")
			face_encoding=face_recognition.face_encodings(face_imag)[0]

			self.know_faces_encodngs.append(face_encoding)
			self.know_face_names.append(image)
		print(self.know_face_names)

	def run_recognition(self):
		video_capture=cv2.VideoCapture(0)

		if not video_capture.isOpened():
			sys.exit("video source not found...")

		while True:
			ret, frame = video_capture.read()

			if  self.process_current_frame:
				small_frame=cv2.rezise(frame,(0,0),fx=0.25,fy=0.25)
				rgb_small_frame=small_frame[:,:,::-1]

				self.face_locations= face_recognition.face_locattions(rgb_small_frame)
				self.face_encodings= face_recognition.face_encodings(rgb_small_frame,self.face_locations)

				self.faces_names=[]
				for face_encoding in self.face_encodings:
					matches= face_recognition.compare_faces(self.know_faces_encodngs,faces_encoding)
					name="Unknown"
					confidence="Unknown"
					face_distances=face_recognition.face_distance(self.know_faces_encodngs,faces_encoding)
					best_match_index=np.argmin(face_distances)
					if matches[best_match_index]:
						name=self.know_face_names[best_match_index]
						confidence=face_confidence(face_distances[best_match_index])
					self.face_names.append(f'{name} ){confidence})')
			self.process_current_frame= not self.process_current_frame
		for (top,right,bottom,left),name in zip(self.face_locations,self.face_names):
			top*=4
			right*=4
			bottom*=4
			left*=4

			cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
			cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),-1)
			cv2.putText(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
			cv2.imshow('Face Recognition',frame)
			if cv2.waitKey(1)==ord('q'):
				break

		video_capture.relase()
		cv2.destroyAllWindows()
if __name__=='__main__'	:
	fr=Face_recognition()
	fr.run_recognition()	