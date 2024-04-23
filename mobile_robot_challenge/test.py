# # from jetcam.csi_camera import CSICamera

# # import numpy as np
# # import cv2
# # import ipywidgets
# # from IPython.display import display
# # from jetcam.utils import bgr8_to_jpeg

# # from PIL import Image



# # image_widget = ipywidgets.Image(format='jpeg')
# # camera = CSICamera(width=300, height=300)

# # print('1')



# # def get_maxcontour(contours):
# #     max_area = 0.0
# #     max_contour = []
# #     for contour in contours:
# #         # x,y,w,h = cv2.boundingRect(contour)
# #         # cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
# #         #         print(max(max_area,cv2.contourArea(contour)))
# #         if max_area != max(max_area,cv2.contourArea(contour)):
# #             max_contour = contour
# #             max_area =cv2.contourArea(contour)

# #     return max_contour

# # tl = (100, 50)
# # bl = (0, 300)
# # tr = (200, 50)
# # br = (300, 300)

# # pts1 = np.float32([tl, bl, tr, br])
# # pts2 = np.float32([[0,0], [0,300], [300,0], [300,300] ])

# # matrix = cv2.getPerspectiveTransform(pts1, pts2)
# # camera.running = False
# # calib_image=camera.read()
# # calib_image = cv2.cvtColor(calib_image, cv2.COLOR_BGR2HSV)
# # avg_background = cv2.mean(calib_image)[:3]
# # range = 10
# # offset = np.ones_like(avg_background)*range

# # kernel = np.ones((3,3),np.uint8)

# # print(avg_background-offset,avg_background+offset)


# # print('2')

# # def update_image(change):
# # #     print('4')
# # #     image = change['new']
# # #     # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # #     image = cv2.warpPerspective(image, matrix, (300, 300))
# # #     mask = cv2.inRange(image,(avg_background[0]-40,0,avg_background[2]-50),(avg_background[0]+40,255,avg_background[2]+50))
# # #     mask = cv2.bitwise_not(mask)
# # #     masked = cv2.bitwise_and(image, image, mask=mask)
# # #     gray = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
# # #     gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
# # #     _,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

# # #     dilate = cv2.dilate(thresh, kernel, iterations = 10)
# # #     erosion = cv2.erode(dilate,kernel,iterations = 10)
# # #     contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# # #     max_contour = get_maxcontour(contours)
# # #     x,y,w,h = cv2.boundingRect(max_contour)
# # #     cv2.drawContours(image, [max_contour], -1, (0,255,0), 3)
# # #     cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
    
# # #     print('5')
# # #     test = bgr8_to_jpeg(image)
# # #     #print(test)
    
    
# # #     print(camera.value.shape)

# #     test = np.array(camera.value)
# #     rgb = test[..., ::-1]
    
# #     image = Image.fromarray(rgb.astype('uint8')).convert('RGB')
# #     image.save('hoi.jpg')

# #     # 
# # # display(image_widget)

# # print('3')
# # #
# # camera.running = True
# # camera.observe(update_image, names='value')
# # camera.running= False
# # #camera.unobserve(update_image, names='value')

# from jetcam.csi_camera import CSICamera

# import numpy as np
# import cv2
# import ipywidgets
# from IPython.display import display
# from jetcam.utils import bgr8_to_jpeg

# from PIL import Image



# image_widget = ipywidgets.Image(format='jpeg')
# camera = CSICamera(width=300, height=300)

# print('1')



# def get_maxcontour(contours):
#     max_area = 0.0
#     max_contour = []
#     for contour in contours:
#         # x,y,w,h = cv2.boundingRect(contour)
#         # cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
#         #         print(max(max_area,cv2.contourArea(contour)))
#         if max_area != max(max_area,cv2.contourArea(contour)):
#             max_contour = contour
#             max_area =cv2.contourArea(contour)

#     return max_contour

# tl = (100, 50)
# bl = (0, 300)
# tr = (200, 50)
# br = (300, 300)

# pts1 = np.float32([tl, bl, tr, br])
# pts2 = np.float32([[0,0], [0,300], [300,0], [300,300] ])

# matrix = cv2.getPerspectiveTransform(pts1, pts2)
# camera.running = False
# calib_image=camera.read()
# calib_image = cv2.cvtColor(calib_image, cv2.COLOR_BGR2HSV)
# avg_background = cv2.mean(calib_image)[:3]
# range = 10
# offset = np.ones_like(avg_background)*range

# kernel = np.ones((3,3),np.uint8)

# print(avg_background-offset,avg_background+offset)


# print('2')

# def update_image(change):
# #     print('4')
# #     image = change['new']
# #     # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #     image = cv2.warpPerspective(image, matrix, (300, 300))
# #     mask = cv2.inRange(image,(avg_background[0]-40,0,avg_background[2]-50),(avg_background[0]+40,255,avg_background[2]+50))
# #     mask = cv2.bitwise_not(mask)
# #     masked = cv2.bitwise_and(image, image, mask=mask)
# #     gray = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
# #     gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
# #     _,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

# #     dilate = cv2.dilate(thresh, kernel, iterations = 10)
# #     erosion = cv2.erode(dilate,kernel,iterations = 10)
# #     contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# #     max_contour = get_maxcontour(contours)
# #     x,y,w,h = cv2.boundingRect(max_contour)
# #     cv2.drawContours(image, [max_contour], -1, (0,255,0), 3)
# #     cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
    
# #     print('5')
# #     test = bgr8_to_jpeg(image)
# #     #print(test)
    
    
# #     print(camera.value.shape)

#     test = np.array(camera.value)
#     rgb = test[..., ::-1]
    
#     image = Image.fromarray(rgb.astype('uint8')).convert('RGB')
#     image.save('hoi.jpg')

#     # 
# # display(image_widget)

# print('3')
# #
# camera.running = True
# camera.observe(update_image, names='value')
# camera.running= False
# #camera.unobserve(update_image, names='value')






import cv2
import numpy as np


cap = cv2.VideoCapture("Arrow Moving Right to Left Green Screen -Copyright Free.mp4")
frames = []
counter = 0

if(cap.isOpened() == False):
    print("Error opening video file")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow("Frame", frame)

        frameGrayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frameGrayScale)
        counter += 1        

        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else: 
        break

cap.release()
cv2.destroyAllWindows()

print("frames:", frames)

for (index, frame) in enumerate(frames):
    if(index > 0):
        flow = cv2.calcOpticalFlowFarneback(frames[index - 1], frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
          # Convert the optical flow to polar coordinates
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mag_scaled = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        print(flow)

        # Convert the angle to hue
        ang_degrees = ang * 180 / np.pi / 2
        ang_scaled = cv2.normalize(ang_degrees, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the hue and magnitude to an RGB image
        hsv = np.zeros_like(frame)
        hsv[..., 0] = ang_scaled
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.convertScaleAbs(mag_scaled)

        # Convert the HSV image to BGR
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Display the optical flow
        cv2.imshow('Optical Flow', bgr)

        # Wait for a key press
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Set the current frame as the previous frame for the next iteration
        # prvs = next.copy()

    # else:
        # ????




# try to print matrix
# for (ri, row) in enumerate(frames[0]):
    # print(row)
#     row_text = ""
    # for (ci, col) in enumerate(row):
        # print(col)
#         row_text += str(col)
        
#     print(row_text)

