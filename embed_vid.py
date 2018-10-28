
# coding: utf-8

# In[4]:


import numpy as np
import cv2
import random

path = 'earth.mp4'
v_max = 10
mu_min = 4
S = 0.1
count=1


cap = cv2.VideoCapture(path)

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )

ret, frame = cap.read()
cap.release()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_embedded1 = cv2.VideoWriter('output_earth_embed_1.mp4',fourcc, 25.0, (int(frame.shape[1]),int(frame.shape[0])))
out_embedded0 = cv2.VideoWriter('output_earth_embed_0.mp4',fourcc, 25.0, (int(frame.shape[1]),int(frame.shape[0])))

'''
transaction_id = random.randint(0,255)
print ("transaction id int: ", str(transaction_id))
transaction_id_str = '{0:08b}'.format(transaction_id)
print ("transaction id bits: ",transaction_id_str)
'''

cap = cv2.VideoCapture(path)

ret, prev_frame = cap.read()
img_lum = cv2.cvtColor(prev_frame , cv2.COLOR_BGR2YCR_CB)
channels=cv2.split(img_lum)
prev_y = channels[0]
out_embedded1.write(prev_frame)   #to ensure first frame is not lost
out_embedded0.write(prev_frame)   #to ensure first frame is not lost

v=np.zeros((prev_frame.shape[0],prev_frame.shape[1]))

list_y = list()
list_0 = list()
list_1 = list()

while(True):
	ret, frame = cap.read()
	try:	
		img_lum = cv2.cvtColor(frame , cv2.COLOR_BGR2YCR_CB)
	except:
		print ('Count= ',str(count),'\n','End of Video')
		break
#	print(img_lum)
	channels=cv2.split(img_lum)
	y = channels[0]
	cb = channels[1]
	cr = channels[2]
	hpf_mask = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
	img_hpf = cv2.filter2D(y, -1, hpf_mask)
	lambda_img =np.uint8( S* abs(img_hpf))
    
	mu_frame=y-prev_y
	mu_img=abs(mu_frame)+mu_min
	mini1=np.uint8(np.minimum(lambda_img,mu_img))
		
	prev_y=y
    
	avg=np.sum(y)/(y.shape[0]*y.shape[1])
	list_y.append(avg)

#	print('Horaha hai mai')
	
	for i in range(0,mini1.shape[0]):
		for j in range(0,mini1.shape[1]):	
			if(mini1[i,j]<v_max):
				v[i,j]=mini1[i,j]
			else:
				v[i,j]=v_max
	

	#img_res = cv2.cvtColor(img_lum, cv2.COLOR_YCR_CB2BGR)
#	print(v)
	embedded_1=np.uint8(y+np.uint8(v))
	embedded_0=np.uint8(y-np.uint8(v))

	needed_multi_channel_img_1 = np.uint8(np.zeros((embedded_1.shape[0], embedded_1.shape[1], 3)))

	"""Add the channels to the needed image one by one"""
	needed_multi_channel_img_1 [:,:,0] = embedded_1
	needed_multi_channel_img_1 [:,:,1] = cb
	needed_multi_channel_img_1 [:,:,2] = cr
#	print(needed_multi_channel_img)
	converted_img_1=cv2.cvtColor(needed_multi_channel_img_1 , cv2.COLOR_YCR_CB2BGR)


	needed_multi_channel_img_0 = np.uint8(np.zeros((embedded_0.shape[0], embedded_0.shape[1], 3)))

	"""Add the channels to the needed image one by one"""
	needed_multi_channel_img_0 [:,:,0] = embedded_0
	needed_multi_channel_img_0 [:,:,1] = cb
	needed_multi_channel_img_0 [:,:,2] = cr
#	print(needed_multi_channel_img)
	converted_img_0=cv2.cvtColor(needed_multi_channel_img_0 , cv2.COLOR_YCR_CB2BGR)

	out_embedded1.write(converted_img_1)
	out_embedded0.write(converted_img_0)
#	embedded_1_merge=cv2.merge([embedded_1, cb, cr])
#	embedded_0_merge=cv2.merge([embedded_0, cb, cr])
#	print(embedded_1)
#	frame_size = (500,300)
#	y=cv2.resize(y,frame_size)
#	lambda_img=cv2.resize(lambda_img,frame_size)
#	mu_img=cv2.resize(mu_img,frame_size)
#	mini1=cv2.resize(mini1,frame_size)
#	v=cv2.resize(v,frame_size)
#	embedded_0=cv2.resize(embedded_0,frame_size)
#	embedded_1=cv2.resize(embedded_1,frame_size)
	avg_1=np.sum(embedded_1)/(y.shape[0]*y.shape[1])
	list_1.append(avg_1)
	avg_0=np.sum(embedded_0)/(y.shape[0]*y.shape[1])
	list_0.append(avg_0)
	print (str(avg) ,'\t',str(avg_0) ,'\t',str(avg_1) ,'\t',str(count))
	count = count + 1

#	cv2.imshow('original_image',frame)
#	cv2.imshow('lambda_image',lambda_img)
#	cv2.imshow('mu_image',mu_img)
#	cv2.imshow('min_lam_mu_image',mini1)
#	cv2.imshow('change',v)
#	cv2.imshow('1_em',embedded_1)
#	cv2.imshow('0_em',embedded_0)
#	cv2.imshow('merged_img',needed_multi_channel_img)
#	cv2.imshow('converted_img_1_embedded',converted_img_1)
#	cv2.imshow('converted_img_0_embedded',converted_img_0)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
# When everything done, release the capture
cap.release()

out_embedded0.release()
out_embedded1.release()

cv2.destroyAllWindows()
print ('List of y\n',str(list_y))
print ('List of 1\n',str(list_1))
print ('List of 0\n',str(list_0))

