# -*- coding: cp936 -*-

import os
import re
import codecs
import sys
import NLPIRPY2016.NLPIR as NLPIR#关联文件的目录
from os.path import dirname
try:
    __file__
    path=dirname(__file__)
except:
    path=os.getcwd()
    print path
default_encoding='GBK'
class Seg:
    def __init__(self,code='GBK', posmap=2):
        global default_encoding
        dataurl = os.path.join(path+r'/NLPIRPY2016')
        #(os.getcwd()+'\NLPIRPY')#关联文件的目录
        #print dataurl
        default_encoding=code
        self.rep=re.compile(u'/[a-z]+$')
        if code=='GBK':
            NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.GBK_CODE)
        elif code=='UTF-8':
            NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.UTF8_CODE)
        elif code=='BIG5':
            NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.BIG5_CODE)
        elif code=='GBK_FANTI':
            NLPIR.NLPIR_Init(dataurl,NLPIR.ENCODING.GBK_FANTI_CODE)
        else:
            print 'NLPIR 初始化失败'
        # 设置默认的词性标注集
        NLPIR.SetPOSmap(posmap)
        #print NLPIR.POS_SIZE
###############
        dict_pwd=path+r'/NLPIRPY2016/Data/'
        self._punctuation=[line.strip().decode('gb18030') for line in
                           file(dict_pwd+"punctuation2.txt")]#punctuation
        self._punctuation.extend([u' ',u'\t',u'\n',u''])
        self._punctuation=list(set(self._punctuation))

        self._stopwords=[line.strip().decode('gb18030').lower() for line in
                         file(dict_pwd+"stopwords_new.txt")]#stopwords
        self._stopwords=list(set(self._stopwords))

        self._userdict=dict_pwd+'tiananmen_ner.txt'
        
        self._usefulflags=['h','b','j','i','k','l','n','ng','nr','ns','nt',\
                            'nx','nz','t','tg','v','vn','vd','un','eng',\
                            'nrt','nrfg','vg','vi','vq','c','cc','nv',\
                            'nr1','nr2','nrj','nrf','vshi','vyou','vf',\
                            'vi','vd','an','ry','ryt','rys','ryv','a','mq',\
                            'ude','ude1','ude2','p','rydj','f']
        #nv :vshi,vyou,rydj,mq
        self._duoji=re.compile(u'\u591a/m|\u51e0/m')
        self._duoshao=re.compile(u'\u591a\u5c11/ry')
###############

    def seg(self,str,islist=False):#in gbk;out unicode
        """
        分词
        """
        if not islist:
            print NLPIR.ParagraphProcess(str,0)
        else:
            result=NLPIR.ParagraphProcess(str,0)
            reslist=result.decode(default_encoding).strip().split(u' ')
            return reslist

    def tag(self,str,islist=False):#in gbk;out unicode
        """
        词性标注
        """
        ##
        #self.importUserDict(self._userdict)
        ##
        if not islist:
            print NLPIR.ParagraphProcess(str,1)
        else:
            result=NLPIR.ParagraphProcess(str,1)
            reslist=self.get_list(result.decode(default_encoding))
            return reslist
#########
    def tag2(self,sentence):
        """
        词性标注,无标点
        """
        sen=self.tag(sentence,True)
        words=[w for w in sen if w.word not in self._punctuation]

        return words
    def tag3(self,sentence):
        """
        词性标注,无标点
        """
        sen=self.tag(sentence,True)
        words=[w for w in sen]

        return words
    def change_pos(self,words):
        '''
        change some pos
        '''
        ws=str(words).decode(default_encoding)
        fry=ws.count('/ry')
        #self._duoshao
        if fry==1 and self._duoshao.search(ws):
            for x in words:
                if x.word==u'\u591a\u5c11':#多少
                    x.flag='ryds'
        elif fry==0 and self._duoji.search(ws):
            for x in words:
                if x.word==u'\u591a' or x.word==u'\u51e0':#多几多少
                    x.flag='rydj'
        ######
        i=0
        while i+1<len(words):#几m个q=>几个ry
            if (words[i].flag,words[i+1].flag[0]) in [('rydj','q'),('rydj','a'),('ryds','q'),('ryds','n')]:
                new=words[:i+1]
                new[i].word+=words[i+1].word
                new[i].flag='rydsj'
                new+=words[i+2:]
                words=new
                i=0
                continue
            i+=1
        ######
        return words
    def vshiyou(self,words):
        """
        change pos before vshi,vyou
        此时是一个主语
        """
        ######
        if 6>len(words)>1 and words[0].flag[0]!='n' and words[0].flag[:2]!='ry' and\
           words[1].flag in ['vshi','vyou']:
            words[0].flag='nv'
                    
        ######
        return words        
    def delete_stopwords(self,words):
        """
        去除停用词,无用标注词
        """
        words[0].word
        words=self.change_pos(words)
        #print words
        words=self.vshiyou(words)
        #print words
        words=[w for w in words if w.word not in self._stopwords or
               w.flag in self._usefulflags]


        return words
#########
    def fileSeg(self,sourceFile,targetFile):
        """
        文件分词
        """
        return NLPIR.FileProcess(sourceFile,targetFile,0)
    def fileSeg2(self,sourceFile,targetFile):
        """
        文件分词,分行切分
        """
        def write_res(res):
            with open(targetFile,'a') as ff:
                ff.write('\n'.join(res).encode(default_encoding)+'\n')
        b=open(targetFile,'w')
        b.close()
        a=open(sourceFile,'r')
        res=[]
        i=0
        j=0
        for line in a:
            try:
                sen=line.strip('\r\n').replace('\t','').replace(' ','')
                res.append(' '.join(self.seg(sen,True)))
                i+=1
                if i%10000==0:
                    write_res(res)
                    res=[]
                    print 'seg done:',i
            except:
                j+=1
        print 'give up lines:',j
        write_res(res)
        a.close()
    def fileTag(self,sourceFile,targetFile):
        """
        文件词性标注
        """
        return NLPIR.FileProcess(sourceFile,targetFile,1)
    def fileTag2(self,sourceFile,targetFile):
        """
        文件词性标注
        """
        def write_res(res):
            with open(targetFile,'a') as ff:
                ff.write('\n'.join(res).encode(default_encoding)+'\n')
        b=open(targetFile,'w')
        b.close()
        a=open(sourceFile,'r')
        res=[]
        i=0
        j=0
        for line in a:
            try:
                sen=line.strip('\r\n').replace('\t','').replace(' ','')
                s=self.tag(sen,True)
                s=[x.word+'\\'+x.flag for x in s]
                res.append(' '.join(s))
                i+=1
                if i%10000==0:
                    write_res(res)
                    res=[]
                    print 'seg done:',i
            except:
                j+=1
        print 'give up lines:',j
        write_res(res)
        a.close()
        sens=[x.strip() for x in file(targetFile)]
        print len(sens)
        sens=[x for x in sens if len(x)>1]
        print len(sens)
        with open(targetFile,'w') as ff:
            ff.write('\n'.join(sens))
    def GetKeyWords(self,sen):###error
        """
        返回关键词
        """
        return NLPIR.GetKeyWords(sen,3,True)
    def importUserDict(self,userDictFile):
        """
        导入用户词典，返回导入成功词个数
        """
        return NLPIR.ImportUserDict(userDictFile,'')
    def addUserWord(self,word):
        "return 0 or 1"
        #'word\tpos'
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
    def get_list(self,res):
        l=res.strip().split(u' ')
        resl=[]
        for x in l:
            if x.count(u'/')==1:
                xx=x.split(u'/')
                resl.append(pair(xx[0],xx[1]))
            else:
                if self.rep.search(x):
                    ind=x.rindex(u'/')
                    resl.append(pair(x[:ind],x[ind+1:]))
        return resl
    def exit(self):
        return NLPIR.Exit()

class pair(object):
    def __init__(self,word,flag):
        self.word = word
        self.flag = flag

    def __unicode__(self):
        return self.word+u"/"+self.flag

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode(default_encoding)

    def encode(self,arg):
        return self.__unicode__().encode(arg)   
    
