
# coding: utf-8

# In[17]:


import numpy as np
import cv2
import random

path_embedded_0 = 'output_earth_embed_0.mp4'
path_embedded_1 = 'output_earth_embed_1.mp4'


cap0 = cv2.VideoCapture(path_embedded_0)
length = int(cap0.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )

ret, frame0 = cap0.read()
cap0.release()
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('earth_user_copy.mp4',fourcc, 25.0, (int(frame0.shape[1]),int(frame0.shape[0])))


cap0 = cv2.VideoCapture(path_embedded_0)
cap1 = cv2.VideoCapture(path_embedded_1)



#Generate transaction ID
transaction_id = random.randint(0,255)
print ("transaction id int: ", str(transaction_id))
transaction_id_str = '{0:08b}'.format(transaction_id)
print ("transaction id bits: ",transaction_id_str)

count = 1
i= 0 
while(True):
    if count > length:
        break
    ret, frame0 = cap0.read()
    ret, frame1 = cap1.read()
    try:	
        img_lum0 = cv2.cvtColor(frame0 , cv2.COLOR_BGR2YCR_CB)
        img_lum1 = cv2.cvtColor(frame1 , cv2.COLOR_BGR2YCR_CB)
    except:
        print ('Count= ',str(count),'\n','End of Video')
        break
#print(img_lum)
    channels0 = cv2.split(img_lum0)
    channels1 = cv2.split(img_lum1)

    y0 = channels0[0]
    y1 = channels1[0]

    avg_0=np.sum(y0)/(y0.shape[0]*y0.shape[1])
    avg_1=np.sum(y1)/(y1.shape[0]*y1.shape[1])
    
    print("Transaction id now:", transaction_id_str[i])
    
    if transaction_id_str[i] == '0':
        out.write(frame0)
        print ('0 embedded','\t',str(avg_0) ,'\t',str(count))

    elif transaction_id_str[i] == '1':
        out.write(frame1)
        print ('1 embedded','\t',str(avg_1) ,'\t',str(count))

    else:
        out.write(frame_org)
        print("Nonsense ho raha hai.")
    
    i=i+1
    if i==len(transaction_id_str):
        i=0
    count = count + 1

# When everything done, release the capture
cap0.release()
cap1.release()
out.release()

cv2.destroyAllWindows()
print ("Video Compiling Complete ...")
#######################################################################################

'''

path_original_copy = 'earth.mp4'
path_user_copy = 'earth_user_copy.mp4'

count=1

cap1 = cv2.VideoCapture(path_user_copy)
cap0 = cv2.VideoCapture(path_original_copy)

length0 = int(cap0.get(cv2.CAP_PROP_FRAME_COUNT))
length1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
if length0 == length1:
    print( "No. of Frames: ",length0 )


#transaction_id = random.randint(0,255)
#print ("transaction id int: ", str(transaction_id))
#transaction_id_str = '{0:08b}'.format(transaction_id)
#print ("transaction id bits: ",transaction_id_str)



list_tran_id = list()
transaction_id = ''

while(True):
    ret, frame0 = cap0.read()
    ret, frame1 = cap1.read()
    try:	
        img_lum0 = cv2.cvtColor(frame0 , cv2.COLOR_BGR2YCR_CB)
        img_lum1 = cv2.cvtColor(frame1 , cv2.COLOR_BGR2YCR_CB)
    except:
        print ('Count= ',str(count),'\n','End of Video')
        break
#print(img_lum)
    channels0 = cv2.split(img_lum0)
    channels1 = cv2.split(img_lum1)

    y0 = channels0[0]
    y1 = channels1[0]

    avg_og=np.sum(y0)/(y0.shape[0]*y0.shape[1])
    avg_user=np.sum(y1)/(y1.shape[0]*y1.shape[1])
    if avg_og > avg_user :
        #print("0")
        transaction_id = transaction_id + '0'
    elif avg_og < avg_user :
        #print("1")
        transaction_id = transaction_id + '1'
    else:
        print("@%#%^&^a!")
    print (str(avg_og) ,'\t',str(avg_user) ,'\t',str(count))
    count = count + 1
    
# When everything done, release the capture
cap0.release()
cap1.release()


cv2.destroyAllWindows()
print ('\nTransaction id of pirate:\n',str(transaction_id))

'''

