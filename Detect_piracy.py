
# coding: utf-8

# In[14]:


import numpy as np
import cv2
import random

path_original_copy = 'earth.mp4'
path_user_copy = 'earth_user_copy.mp4'

v_max = 10
mu_min = 4
S = 0.1
count=1

cap0 = cv2.VideoCapture(path_original_copy)
cap1 = cv2.VideoCapture(path_user_copy)

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
        print("kya pata kya hua!")
    print (str(avg_og) ,'\t',str(avg_user) ,'\t',str(count))
    count = count + 1
    
# When everything done, release the capture
cap0.release()
cap1.release()


cv2.destroyAllWindows()
print ('\nTransaction id of pirate:\n',str(transaction_id))

