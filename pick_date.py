# -*- coding: utf-8 -*-

import MeCab
import re

tagger = MeCab.Tagger()
body = "復興庁は28日、東日本大震災による全国の避難者は22日現在で34万4345人と発表した。仮設住宅などへの入居者の把握が進み、前回調査（8日現在）より55人増えた。(時事通信)"
pubdate = "2012/3/28"
pubdateDict = {}
chasen = []
date = []
rowDate = []


def through_mecab():
    chasenList = tagger.parse(body)
    chasenList = chasenList.split("\n")
    # print len(chasenList)
    for i in range(len(chasenList)):
        chasen.append(re.split(r'\t|,|', chasenList[i]))
        # print len(chasen[i])
        # EOSをdelした後に参照するとIndexErrorがでる
        if len(chasen[i]) < 2:
            del chasen[i]
            break
        # 形態素の読みはいらないため削除
        else:
            del chasen[i][7:10]
            # for j in range(len(chasen[i])):
            #     print len(chasen[i])


def pick_date():
    global rowDate
    for i in range(len(chasen)):
        # 数とその後ろの助数詞を抽出したのちリスト化
        if chasen[i][2] == "数":
            rowDate.append(chasen[i][0])
            rowDate.append(chasen[i+1][0])
            date.append(rowDate)
            rowDate = []

    # for i in range(len(date)):
    #     print date[i]


def assumption_date():
    splitPubdate = pubdate.split("/")
    pubdateDict["year"], pubdateDict["month"], pubdateDict["day"] = (
        splitPubdate[0], splitPubdate[1], splitPubdate[2])
    for i in range(len(date)):
        if date[i][1] in "年":
            pass
        elif date[i][1] in "月":
            print(pubdateDict["year"]+"年"
                + date[i][0]+date[i][1]
                + pubdateDict["day"])
        elif date[i][1] in "日":
            print(pubdateDict["year"]+"年"
                + pubdateDict["month"]+"月"
                + date[i][0]+date[i][1])


through_mecab()
pick_date()
assumption_date()
