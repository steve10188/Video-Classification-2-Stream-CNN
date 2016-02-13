import cv2
import numpy as np

def getOpticalFlow(filename,label):
    cap = cv2.VideoCapture(filename)
    ret, frame1 = cap.read()
    frame1 = cv2.resize(frame1, (256,256))
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255

    fx = []
    fy = []
    count=0
    firstTime=1
    while(1):
        ret, frame2 = cap.read()

        if frame2==None:
          break
        
        frame2 = cv2.resize(frame2, (256,256))
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        fx.append(flow[:,:,0])
        fy.append(flow[:,:,1])
        count+=1
        if count == 10:
            flowX = np.dstack((fx[0],fx[1],fx[2],fx[3],fx[4],fx[5],fx[6],fx[7],fx[8],fx[9]))
            flowY = np.dstack((fy[0],fy[1],fy[2],fy[3],fy[4],fy[5],fy[6],fy[7],fy[8],fy[9]))
            inp = np.dstack((flowX,flowY))
            inp = np.expand_dims(inp, axis=0)
            if not firstTime:
                inputVec = np.concatenate((inputVec,inp))
            else:
                inputVec = inp
                firstTime = 0

            count = 0
            fx = []
            fy = []


        # print flow[:,:,0].shape
        # print '\n\n'
        # print flow[:,:,1].shape

        # # mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        # # hsv[...,0] = ang*180/np.pi/2
        # # hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        # # bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        
        print count

        # cv2.imshow('frame2',bgr)
        # k = cv2.waitKey(5) & 0xff
        # if k == 27:
        #     break
        prvs = next

    cap.release()
    cv2.destroyAllWindows()
    inputVec=np.rollaxis(inputVec,3,1)
    print inputVec.shape



f='./sample_videos/b.mp4'
getOpticalFlow(f,1)