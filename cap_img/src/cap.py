#!/usr/bin/env python3
#-*- coding: utf-8 -*

import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import rospy
import numpy as np
import os
import re


#画像サイズ
#yolov8の場合画像の最大サイズは640(pixel)
WIDTH = 640
HEIGHT = 480

class Cap_Img():
    def __init__(self):
        rospy.init_node('cap_img',anonymous=True)
        self.bridge = CvBridge()



        ##任意で変更する部分1/2#################################################

        self.save_directory = '/home/ayu/cap_date/'     #保存先
        self.fail_name = 'paper_bag'        #アイテムの名前

        ####################################################################


        files_file = [f for f in os.listdir(self.save_directory) if os.path.isfile(os.path.join(self.save_directory, f))]       #ファイル名をリストで取得
        
        if files_file == []:
            self.c = 0

        else:
            files_file.sort(reverse=True)      #数字(大<->小)にソート
            result = int(re.sub(r"\D","",files_file[0]))      #数字の取得
            self.c = result + 1

        print("Next nuber is {}".format(self.c))
        print("Push Enter key")

        ##任意で変更する部分2/2#######################################################################################
            
        rospy.Subscriber('/camera/color/image_raw',Image,self.img_listener)    #realsenseの場合(realsense2_camera)
        #rospy.Subscriber('/usb_cam/image_raw',Image,self.img_listener)          #webカメラの場合(usb_cam)

        ##############################################################################################################


    #カラー画像を処理
    def img_listener(self,data):
        try:
            color_data = self.bridge.imgmsg_to_cv2(data,"bgr8")
            self.img = np.copy(color_data)
            self.img = cv2.resize(self.img,(WIDTH,HEIGHT))

            cv2.imshow('cap_img',self.img)
            k = cv2.waitKey(1)
            if k == 13:                 #Enterで撮影&保存
                fail_full_name = self.fail_name + '_' + str(self.c).zfill(4) + '.png'
                cv2.imwrite(self.save_directory + fail_full_name, self.img)
                print('Photo saved\nimg nuber is ->\t{}'.format(fail_full_name))
                self.c += 1

        except CvBridgeError as e:
            print("img_listener:",e)

if __name__ == '__main__':
    try:
        Cap_Img()
        rospy.spin()
    except rospy.ROSInitException:
        print('Shutting down')
        cv2.destroyAllWindows()
