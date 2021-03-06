from operator import truediv
import traceback
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from selenium import webdriver
from random import randint
import random
import time
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

#UI파일 연결
base_dir = os.path.dirname(os.path.abspath(__file__))
form_class = uic.loadUiType(base_dir + "//insta.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        global random_message_lst
        random_message_lst = []

        super().__init__()
        self.setupUi(self)
        global textBrowser
        textBrowser = self.textBrowser

        self.setWindowTitle('Instagram Bot v1.0.2')

        self.start_pushButton.clicked.connect(self.main)
        self.pushButton_add.clicked.connect(self.appendList)
        self.pushButton_del.clicked.connect(self.delList)
        
        self.pushButton_add.setEnabled(False)
        self.pushButton_del.setEnabled(False)
        self.lineEdit_message.setEnabled(False)


        self.checkBox_comment.stateChanged.connect(self.buttonStat)
        self.checkBox_like.stateChanged.connect(self.buttonStat)
        self.checkBox_follow.stateChanged.connect(self.buttonStat)
        self.checkBox_comment.stateChanged.connect(self.buttonStat)       
                    
    def main(self):
        global instagram_id
        global instagram_pwd
        global search_tag
        global start_time
        global delay_time
        global repeat_cnt

##################################################
        instagram_id = self.lineEdit_id.text()
        instagram_pwd = self.lineEdit_pw.text()
        search_tag = self.lineEdit_tag.text()
        delay_time = self.lineEdit_delay.text()
        repeat_cnt = self.lineEdit_delay.text()
        print(instagram_id)
        print(instagram_pwd)
        print(search_tag)
        print(repeat_cnt)
##################################################

        start_time = time.time() # 시작시간
        WindowClass.login(self)
        WindowClass.search(self)

        global i_cnt
        for i_cnt in range(int(repeat_cnt)):
            try:
                follow_text = driver.find_element_by_css_selector("._aar2 ._aade").text
                if follow_text == "팔로우":
                    WindowClass.checkCnt(self)
                    WindowClass.likeEnable(self)
                    WindowClass.commentEnable(self)
                    WindowClass.followEnable(self)
                    # 다음 버튼 누르기
                    driver.find_element_by_css_selector("._aaqg ._abl-").click()
                    print('[' + time.strftime('%H:%M:%S') + ']' ,"다음 게시물 이동 중..\n =======================================")
                    print("======= 총 경과시간 =======")
                    print(WindowClass.elapsedTime(self))
                    driver.implicitly_wait(30)
                    time.sleep(random.uniform(3,6))

                else:
                    print('[' + time.strftime('%H:%M:%S') + ']' ,"[이미 팔로우한 유저입니다]\n{0}번째 작업 건너뛰기".format(i_cnt+1))
                    time.sleep(random.uniform(3,6))
                    driver.find_element_by_css_selector("._aaqg ._abl-").click()
                    print('[' + time.strftime('%H:%M:%S') + ']' ,"다음 게시물 이동 중..\n =======================================")
                    print("======= 총 경과시간 =======")
                    print(WindowClass.elapsedTime(self))            
                    driver.implicitly_wait(30)
                    time.sleep(random.uniform(3,6))

            except Exception as e:
                time.sleep(random.uniform(3,6))
                driver.find_element_by_css_selector("._aaqg ._abl-").click()
                print('[' + time.strftime('%H:%M:%S') + ']' ,"로딩 오류 발생, 다음 게시물 이동 중..\n =======================================")
                print("[오류 메시지]", traceback.format_excf())
                driver.implicitly_wait(30)   

                #####
                time.sleep(random.uniform(60,80))
                #####

    def appendList(self):
        random_message_lst.append(self.lineEdit_message.text())
        self.listWidget.addItem(self.lineEdit_message.text())
        self.lineEdit_message.clear()
        print(random_message_lst)

    def delList(self):
        del_index = self.listWidget.currentRow()
        del random_message_lst[del_index]
        self.listWidget.takeItem(del_index)
        print(random_message_lst)

    def buttonStat(self):
        if self.checkBox_comment.isChecked():
            self.pushButton_add.setEnabled(True)
            self.pushButton_del.setEnabled(True)
            self.lineEdit_message.setEnabled(True)
        else:
            self.pushButton_add.setEnabled(False)
            self.pushButton_del.setEnabled(False)
            self.lineEdit_message.setEnabled(False)

    def likeEnable(self):
        if self.checkBox_like.isChecked():
            WindowClass.like(self)
            
    def commentEnable(self):
        if self.checkBox_comment.isChecked():
            WindowClass.comment(self)

    def followEnable(self):
        if self.checkBox_follow.isChecked():
            WindowClass.follow(self)
    
    def checkCnt(self):
        global likeStat
        global commentStat
        global followStat
        likeStat = 0
        commentStat = 0
        followStat = 0
        
        if self.checkBox_like.isChecked() & self.checkBox_comment.isChecked() & self.checkBox_follow.isChecked():
            likeStat = 1
            commentStat = 1
            followStat = 1
        elif self.checkBox_like.isChecked() & self.checkBox_comment.isChecked():
            likeStat = 1
            commentStat = 1
        elif self.checkBox_like.isChecked() & self.checkBox_follow.isChecked():
            likeStat = 1
            followStat = 1
        elif self.checkBox_comment.isChecked() & self.checkBox_follow.isChecked():
            commentStat = 1
            followStat = 1           
        elif self.checkBox_like.isChecked():
            likeStat = 1
        elif self.checkBox_comment.isChecked():
            commentStat = 1
        elif self.checkBox_follow.isChecked():
            followStat = 1
        
    def logMsg(self, msg):
        print(msg)
        self.textBrowser.append(msg)
        QApplication.processEvents()

    def login(self):
        global driver
        if getattr(sys, 'frozen', False):
            chromedriver_path = os.path.join(sys._MEIPASS, "./chromedriver")
            driver = webdriver.Chrome(chromedriver_path)
        else:
            driver = webdriver.Chrome('./chromedriver')

        url = 'https://www.instagram.com/accounts/login/'   
        driver.get(url)
        driver.implicitly_wait(15)
        print(WindowClass.elapsedTime(self))

        driver.find_element_by_css_selector(".-MzZI:nth-child(1) .zyHYP").send_keys(instagram_id)

        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "id 입력 완료")
        # QApplication.processEvents()

        time.sleep(random.uniform(10,15))
        driver.find_element_by_css_selector(".-MzZI+ .-MzZI .zyHYP").send_keys(instagram_pwd)

        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "password 입력 완료")

        time.sleep(random.uniform(5,10))
        driver.find_element_by_css_selector(".-MzZI+ .DhRcB").click()
        driver.implicitly_wait(15)
        time.sleep(5)

        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "로그인 성공")
        QApplication.processEvents()

        print("== 경과시간 ==")
        print(WindowClass.elapsedTime(self))
    
    def search(self):
        url = 'https://www.instagram.com/explore/tags/' + search_tag
        driver.get(url)
        driver.implicitly_wait(15)
        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "해시태그 검색 중..")
        time.sleep(10)

        pic_list = driver.find_elements_by_css_selector("._aagw , ._aanf:nth-child(1) ._a6hd")
        pic_list = list(pic_list)
        driver.implicitly_wait(15)
        time.sleep(5)
        pic_list[0].click()
        driver.implicitly_wait(15)
        time.sleep(5)

        # 인기게시물 건너뛰기
        for i in range(9):
            driver.find_element_by_css_selector("._aaqg ._abl-").click()
            WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "{0}번째 인기 게시물 건너뛰기".format(i+1))
            driver.implicitly_wait(15)
            time.sleep(5)

    def like(self):
        WindowClass.delayTime(self)
        driver.find_element_by_css_selector("._aamw ._abl-").click() # 좋아요 누르기
        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "{}번째 좋아요".format(i_cnt+1))
        time.sleep(random.uniform(3,6))

    def comment(self):
        driver.find_element_by_css_selector("._aaoc").click()
        time.sleep(random.uniform(5,10))

        random_message = WindowClass.randomMessage(self) # 랜덤메시지 함수 리턴값 가져오기

        driver.find_element_by_css_selector("._aaoc").send_keys(random_message)

        WindowClass.delayTime(self)

        driver.find_element_by_css_selector("._aad0").click()
        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "{0}번째 댓글입력: {1}".format(i_cnt+1, random_message))
        driver.implicitly_wait(15)
        time.sleep(random.uniform(4,6))

    def follow(self):
        WindowClass.delayTime(self)
        driver.find_element_by_css_selector("._aar2 ._aade").click()
        WindowClass.logMsg(self, '[' + time.strftime('%H:%M:%S') + '] ' + "{0}번째 팔로우".format(i_cnt+1))
        time.sleep(random.uniform(7,12))

    def randomMessage(self):
        if len(random_message_lst) == 1:
            random_message = random_message_lst[0]
        else:
            random_message = random_message_lst[randint(0,len(random_message_lst)-1)]
        return random_message

    def delayTime(self):
        print(likeStat)
        print(commentStat)
        print(followStat)
        if likeStat + commentStat + followStat == 3:
            print("3개 체크")
            time.sleep(random.uniform(int(delay_time) / 3, int(delay_time) / 3 + 30))
        elif likeStat + commentStat + followStat == 2:
            print("2개 체크")      
            time.sleep(random.uniform(int(delay_time) / 2, int(delay_time) / 2 + 30))
        else:
            print("1개 체크")
            time.sleep(random.uniform(int(delay_time), int(delay_time) + 30))

    def elapsedTime(self): # 경과시간 정보 함수
        elapsed_time = time.time() - start_time
        m, s = divmod(elapsed_time, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if d > 0:
            dtime = str(int(d)) + "일 "
        else: 
            dtime = ""
        if h > 0:
            htime = str(int(h)) + "시간 "
        else:
            htime = ""
        if m > 0:
            mtime = str(int(m)) + "분 "
        else:
            mtime = ""     
        strTime = dtime + htime + mtime + str(int(s)) + "초"    
        return strTime 

if __name__ == "__main__" :        
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
