import cv2
import time

print('Starting the Calibration. Press and maintain the space bar to exit the script\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')

id_image=0

# termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Call the two cameras
CamR= cv2.VideoCapture(1)   # 0 -> Right Camera
CamL= cv2.VideoCapture(0)   # 2 -> Left Camera
CamR.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
CamR.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

CamL.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
CamL.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


while True:
    retR, frameRight= CamR.read()
    retL, frameLeft= CamL.read()
    frameR=cv2.resize(frameRight,(320,240))
    frameL=cv2.resize(frameLeft,(320,240))
    grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
    grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    retR, cornersR = cv2.findChessboardCorners(grayR,(9,6),None)  # Define the number of chess corners (here 9 by 6) we are looking for with the right Camera
    retL, cornersL = cv2.findChessboardCorners(grayL,(9,6),None)  # Same with the left camera
    cv2.imshow('imgR',frameR)
    cv2.imshow('imgL',frameL)
    cv2.imshow('Normal', np.hstack([frameL, frameR]))
    # If found, add object points, image points (after refining them)
    if (retR == True) & (retL == True):
        corners2R= cv2.cornerSubPix(grayR,cornersR,(11,11),(-1,-1),criteria)    # Refining the Position
        corners2L= cv2.cornerSubPix(grayL,cornersL,(11,11),(-1,-1),criteria)

        # Draw and display the corners
        cv2.drawChessboardCorners(grayR,(9,6),corners2R,retR)
        cv2.drawChessboardCorners(grayL,(9,6),corners2L,retL)
        cv2.imshow('VideoR',grayR)
        cv2.imshow('VideoL',grayL)
        time.sleep(4)
        str_id_image = str(id_image)

        if cv2.waitKey(0) & 0xFF == ord('s'):
         cv2.imwrite('./stereopi-tutorial-master/pairs/chessboard-R' + str_id_image + '.png',frameR)  # Save the image in the file where this Programm is located
         cv2.imwrite('./stereopi-tutorial-master/pairs/chessboard-L' + str_id_image + '.png', frameL)
         id_image = id_image + 1
         print('Измерение №', id_image, 'проведено')

    #else:
     #  if cv2.waitKey(0) & 0xFF == ord('s'):
     #       str_id_image= str(id_image)
      #      cv2.imwrite('sceneR'+str_id_image+'.png',frameR)
      #      cv2.imwrite('sceneL'+str_id_image+'.png',frameL)
       #     id_image=id_image+1

        #    print('Images not saved')

    # End
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# Release
CamR.release()
CamL.release()
cv2.destroyAllWindows()    
