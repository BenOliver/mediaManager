import sys
import os
import fnmatch
import random
import urllib.request
import json
import time
import re
import pickle
import sqlite3
from moviepy.video.io.VideoFileClip import VideoFileClip
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QIcon


def setup():
    global jsonFilePath
    global dataDict
    global databasePath
    global conn
    global c
    databasePath = os.path.normpath("D://Files/Google Drive/assetDatabase.db")
    jsonFilePath = os.path.normpath("D://Files/Google Drive/fileData.json")
    conn = sqlite3.connect(databasePath)
    c= conn.cursor()
    if os.path.isfile(jsonFilePath):
        with open(jsonFilePath, "r") as f:
            dataDict = json.load(f)
    else:
        dataDict = {"test": 1}


def teardown():
    with open(jsonFilePath, "w") as f:
        json.dump(dataDict, f)

    conn.close()


#

#
# fileList = []
# showList = []
# showDict = {}
#
# with open("showList.txt", "r") as f:  # import list of shows to name and assign wildcards
#     showList = f.read().split("\n")
#     showList.remove("")
# for v in showList:
#     showDict["*" + v.replace(" ", "?") + "*"] = v


# print(showDict)


class vid(object):
    '''object representing tv episode/movie'''
    stringClear = {" ": "bluray 1080p 720p 1080 720 dvdscr dvd x264 x265 _ [ ] ( ) xvid ac3 3d .".split()}
    approvedExts = ['.'+i for i in 'mp4 mkv avi'.split()]
    excludedExts = ['.'+i for i in 'txt nfo'.split()]

    def __init__(self, originPath):

        #original full pathname
        self.originPath = originPath
        #         self.originRoot=os.path.dirname(self.originPath)
        #         self.originName=self.originPath.rsplit("\\",1)[-1].rsplit(".",1)[0]
        #         self.ext=os.path.splitext(self.originPath)[-1]#self.originPath.rsplit('.',1)[-1]
        #original directory of file directory of file, filename
        self.originRoot, self.originName = os.path.split(self.originPath)
        #filename (without Ext), extension
        self.originName, self.ext = os.path.splitext(self.originName)

        self.root = self.originRoot
        self.name = self.originName
        self.path = self.originPath
        self.match = False
        self.type = ""
        self.show = ""
        self.showPath = ""
        self.season = ""
        self.seasonPath = ""
        self.episode = ""
        self.episodePath = ""
        self.length = ""
        self.year = ""
        self.queryString = self.originName.lower()
        #         self.fileRuntime=VideoFileClip(self.path).duration
        self.metaDic = {}

        self.cleanQuery()

    #         self.getData()
    #
    #         print(self.originRoot)
    #         print(self.originName)
    #         print(self.ext)
    #         print(os.path.join(self.originRoot,self.originName)+self.ext)
    #         print(self.originName)
    #         print(self.queryString)
    #         print("Year: "+self.year)
    #         self.getSeasonEpisode()
    #         print("initialised")
    def getSeasonEpisode(self):
        for i in range(len(self.originName) - 6): # TODO replace with regex
            if fnmatch.fnmatch(self.originName[i:i + 6], "S[0-9][0-9]E[0-9][0-9]"):
                self.season = self.originName[i + 1:i + 3]
                self.episode = self.originName[i + 4:i + 6]
                break

    def getShow(self):
        for i in showDict:
            if fnmatch.fnmatch(self.originName, i):
                self.show = showDict[i]
                break

    def getpath(self):
        if (self.season != "") & (self.episode != "") & (self.show != ""):
            self.showPath = os.path.join(sP, self.show)
            self.seasonPath = os.path.join(self.showPath, "Season " + self.season)
            #             print(self.seasonPath)
            self.episodePath = os.path.join(self.seasonPath,
                                            self.show + " S" + self.season + "E" + self.episode + "." + self.ext)
            #             print(self.showPath)
            if not os.path.isdir(self.showPath):
                #                 print("making show&season")
                os.mkdir(self.showPath)
                os.mkdir(self.seasonPath)
            elif not os.path.isdir(self.seasonPath):
                #                 print("making season")
                os.mkdir(self.seasonPath)
                #             elif os.path.isfile(self.episodePath):

    def moveFile(self):
        if self.episodePath != "":
            # if a target path exists

            if not os.path.isfile(self.episodePath):
                # target file doesn't exist
                os.rename(self.originPath, self.episodePath)
            else:
                # target file already exists, compare with md5?
                # delete if identical
                # keep better quality file if different
                # possibly check if x264 or x265 and keep x265
                pass

    def autoFix(self):
        self.getSeasonEpisode()
        self.getShow()
        self.getpath()

    def cleanQuery(self):
        for k in self.stringClear:  # replace dictionary values (v) with its key (k)
            for v in self.stringClear[k]:
                self.queryString = self.queryString.replace(v, k)
        while "  " in self.queryString:  # remove extra whitespace
            self.queryString = self.queryString.replace("  ", " ")
        self.queryString = self.queryString.strip()
        if fnmatch.fnmatch(self.queryString, "*[1,2][8,9,0][0-9][0-9]*"):  # check for year
            #             print("year found")
            for i in range(len(self.queryString) - 3):
                #                 print(self.queryString[i:i+4])
                if fnmatch.fnmatch(self.queryString[i:i + 4], "*[1,2][8,9,0][0-9][0-9]*"):  # find year index
                    #                     print("index found")
                    self.year = self.queryString[i:i + 4]
                    self.queryString = self.queryString[:i].rstrip()
                    break

    def getData(self):
        print("getting Data")
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11;Linux i686)"
        queryDic = {}
        queryDic["t"] = self.queryString
        #         queryDic["tomatoes"]="True"
        queryDic["y"] = self.year

        url = "http://www.omdbapi.com/?"
        data = urllib.parse.urlencode(queryDic)
        fullUrl = url + data

        print(fullUrl)
        setT = time.time()
        req = urllib.request.Request(fullUrl)
        endT = time.time() - setT
        print("request time: ", "{0:.2f}".format(endT * 1000), "ms")
        #         print("response")
        resp = urllib.request.urlopen(req)
        resp_data = resp.read()
        resp_data_str = resp_data.decode("utf-8")
        self.metaDic = json.loads(resp_data_str)

        #         print(self.metaDic["Runtime"],self.metaDic["RuntimeNumeric"])
        if self.metaDic["Response"] == "True":
            print("True Response")

            if self.queryString.lower() == self.metaDic["Title"].lower():
                # exact match
                if self.year == "":
                    # no year data - compare runtimes
                    #                     print("Comparing times")
                    print("getting runtimes")
                    s = re.sub("[^0-9]", "", self.metaDic["Runtime"])
                    self.metaDic["RuntimeNumeric"] = int(s) if s else 0
                    del s
                    #                     with VideoFileClip(self.path) as clip:
                    #                         self.fileRuntime=clip.duration
                    self.clip = VideoFileClip(self.path)
                    self.fileRuntime = self.clip.duration
                    del self.clip
                    print(self.metaDic["Runtime"], " vs ", self.fileRuntime / 60)
                    if abs(self.metaDic["RuntimeNumeric"] - self.fileRuntime / 60) < 10:
                        #                         print("runtimes close")
                        self.assignMetaData()
                    del self.fileRuntime

                elif (self.year == self.metaDic["Year"]):
                    # year match
                    self.assignMetaData()
            else:
                print("Match not exact -program is not developed here")
        else:
            print("No Match")
            pass

    def assignMetaData(self):
        print("Match Found")
        self.match = True
        self.year = self.metaDic["Year"]
        self.name = self.metaDic["Title"] + "_" + self.year
        self.path = os.path.join(self.root, self.name) + self.ext

    #         print(self.originName)
    #         print(self.name)

    def renameVid(self):
        if self.originPath != self.path:
            print("Renaming")
            print(self.originPath, "  --->  ", self.path)
            if (not os.path.isfile(self.path)) | (os.path.samefile(self.originPath, self.path)):
                try:
                    os.rename(self.originPath, self.path)
                except Exception as e:
                    print("Renaming Error: %s" % str(e))
            else:
                # file exists
                print("File already exists: ", self.path)
        else:
            pass  # print("Paths are the same")


# print(resp_data)

#
#
# pkPath = "listPickle.pk"
#
# if os.path.isfile(pkPath):
#     "pickleFound"
#     with open(pkPath, "rb") as f:
#         fileList = pickle.load(f)
# else:
#     "noPickle"
#     fileList = []
#
# for root, dirs, files in os.walk(mP, topdown=False):
#     #     print("main")
#     for name in files:
#         p = os.path.join(root, name)
#         #         print("files")
#         #         t=name.rsplit(".",1)[-1]
#         t = os.path.splitext(p)[-1]
#         if t in approvedExts:
#             if any(x.path == p for x in fileList):
#                 #                 print("fileAlready there")
#                 pass
#             else:
#                 print("Adding %s to list" % p)
#                 fileList.append(vid(p))
#
#                 #             fileList[-1].renameVid()
#
# for v in fileList:
#     if v.match == False:
#         print("no match")
#         v.getData()
#         print("+" * 20)
#
# for v in fileList:
#     v.renameVid()
# # print("-"*20)
#
# with open(pkPath, "wb") as f:
#     pickle.dump(fileList, f)

# fileList[-1].autoFix()
#             fileList[-1].moveFile()
#     for name in dirs:
#         try:
#             os.rmdir(os.path.join(root,name))   #delete empty folders
#         except Exception:
#             pass
#         print(root)

#     for name in dirs:
#         print("dirs")
#         print(os.path.join(root,name))
# len(files)


# a = fileList[1]
# print(a.originName)
# print(VideoFileClip(a.path).duration)


# a.getData()

# a=fileList[1]
# print(a.originName)
# print(a.queryString)
# a.cleanQuery()
# print(a.queryString)
# a.getData()
# a=fileList[20]
# print(a.season=="")
# print(a.originName)
# print(fileList[1].originName)
# a.getSeasonEpisode()
# print(a.season)
# print(a.episode)
# a.getShow()
# print("getting Show")
# print(a.show)
# a.getpath()
# print(a.episodePath)
# os.rename(a.originPath,a.episodePath)
# for i in fileList:
#     i.getSeasonEpisode()
#     i.getShow()
#     i.getpath()
#     i.moveFile()


# print(fnmatch.fnmatch(a.originName,"*Game?of?Thrones*"))
#
# fileExtensions=['mp4','mkv','avi','m4v']
# paths=["G://Files/Local/Data"]
# if 0:
#     for path in paths:
#         for i in os.walk(os.path.normpath(path)):
#             if i[-1] is not []:
#                 for j in i[-1]:
#                     if j.split('.')[-1].lower() in fileExtensions:
#                         print(os.path.join(i[0],j))
# print("this is a test")
# print(os.getcwd())
# print('test .abc .def'.split())


class myWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(300,300,300,220)
        self.setWindowTitle('Ben\'s Application')
        self.setWindowIcon(QIcon('web.png'))

        self.show()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    w=myWidget()
    sys.exit(app.exec_())
    print("one")
    while w:
        print("test")
        time.sleep(1)

    # mP = "D:\\Media\\Videos\\TV"  # raw media Path
    # sP = "D:\\Media\\Videos\\TV"  # structured media path
    # mP = "E:\Media\TV"  # raw media Path
    # sP = "E:\Media\TV"  # structured media path
    # mP = "E:\Media\Films"  # raw media Path
    # sP = "E:\Media\Films"  # structured media path
    # paths=["G:\Files\Local\Data\Videos"]
    #
    # setup()
    # c.execute('DROP TABLE test')
    # c.execute('''CREATE TABLE IF NOT EXISTS test (filename text, directory text, size int, md5 text)''')
    # fileExtensions=['mp4','mkv','avi','m4v']
    # for path in paths:
    #     for direc in os.walk(os.path.normpath(path)):
    #         if direc[-1] is not []:
    #             for fname in direc[-1]:
    #                 if fname.split('.')[-1].lower() in fileExtensions:
    #                     stat=os.stat(os.path.join(direc[0],fname))
    #                     str(stat.st_size)
    #                     cleanDir=os.path.normpath(direc[0])
    #                     # print("statSIZE")
    #                     sqlString='INSERT INTO test VALUES( ?, ?, ?, ? )'
    #                     c.execute(sqlString,(fname,cleanDir,stat.st_size,'-'))
    #
    # # c.execute("INSERT INTO test VALUES ('file1','C://Files/test/helloWorld', '10GB', 'ksdjflaskdjf')")
    # conn.commit()
    # for row in c.execute("SELECT * FROM test WHERE size = 1615629444"):
    #     print(row)
    # teardown()
