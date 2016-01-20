# -*- coding: cp936 -*-

import NLPIR
import os

class Seg:
        def __init__(self,code='GBK'):
                dataurl = os.path.join('')#当前目录

                if code=='GBK':
                        NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.GBK_CODE)
                elif code=='UTF-8':
                        NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.UTF8_CODE)
                elif code=='BIG5':
                        NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.BIG5_CODE)
                elif code=='GBK_FANTI':
                        NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.GBK_FANTI_CODE)
                else:print "code wrong!"
        def seg(self,str):
                """
                分词
                """
                return NLPIR.ParagraphProcess(str,0)

        def tag(self,str):
                """
                词性标注
                """
                return NLPIR.ParagraphProcess(str,1)

        def fileSeg(self,sourceFile,targetFile):
                """
                文件分词
                """
                return NLPIR.FileProcess(sourceFile,targetFile,0)

        def fileTag(self,sourceFile,targetFile):
                """
                文件词性标注
                """
                return NLPIR.FileProcess(sourceFile,targetFile,1)
        def importUserDict(self,userDictFile):
                """
                导入用户词典，返回导入成功词个数
                """
                return NLPIR.ImportUserDict(userDictFile)
        def addUserWord(self,word):
                "return 0 or 1"
                return NLPIR.AddUserWord(word)
                
        def saveTheUserDict(self):
                "return 1 true or 2 false"
                return NLPIR.SaveTheUsrDic()
        def delUserWord(self,word):
                """Returns    :
                -1,the word not exist in the user dictionary;
                else, the handle of the word deleted
                """
                return NLPIR.DelUsrWord(word)

        def exit(self):
                return NLPIR.Exit()

        
        
