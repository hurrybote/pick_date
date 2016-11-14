# -*- coding: utf-8 -*-

import MeCab
import re

tagger = MeCab.Tagger()
body = "復興庁は28日、東日本大震災による全国の避難者は22日現在で34万4345人と発表した。仮設住宅などへの入居者の把握が進み、前回調査（8日現在）より55人増えた。(時事通信)"
# body = "【AFP＝時事】世界保健機構（World Health Organization、WHO）は9日、エボラ出血熱が猛威をふるう西アフリカのギニア、シエラレオネ、リベリアの3国で、安全性が確認されたワクチン2種について、効果を確かめるため人体への試験的投与を数週間以内にも開始すると発表した。(ＡＦＰ＝時事)"
pubdate = "2012/3/28"
# pubdate = "2015/1/10"
pubdateDict = {}
chasen = []
date = []
dateDict = {}
rowDate = []
metaDate = []

splitPubdate = pubdate.split("/")


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


# 日付を辞書型で格納。その日付が指定されていない場合は0を格納。リストー辞書ー日付
def pick_date():
    global rowDate

    for i in range(len(chasen)):
        # 数とその後ろの助数詞を抽出したのちリスト化
        # print chasen[i][0]
        do_assumpte_date(i)


# 推定のためのfor文を関数化
def do_assumpte_date(i):
    global rowDate
    if chasen[i][2] == "数" and chasen[i+1][0] == "日":
        if chasen[i-2][2] == "数" and chasen[i-1][0] == "月":
            if chasen[i-4][2] == "数" and chasen[i-3][0] == "年":
                rowDate.append(chasen[i-4][0])
                rowDate.append(chasen[i-3][0])
                dateDict["year"] = rowDate
                rowDate = []
            else:
                dateDict["year"] = assumption_date_year()

            rowDate.append(chasen[i-2][0])
            rowDate.append(chasen[i-1][0])
            dateDict["month"] = rowDate
            rowDate = []
        else:
            dateDict["month"] = assumption_date_month()
            dateDict["year"] = assumption_date_year()

        rowDate.append(chasen[i][0])
        rowDate.append(chasen[i+1][0])
        dateDict["day"] = rowDate
        rowDate = []
        # print "if文が実行されました"

        date.append(dateDict.copy())


def assumption_date_year():
    row = [splitPubdate[0], "年"]
    return row


def assumption_date_month():
    row = [splitPubdate[1], "月"]
    return row


def print_date():
    print len(date)
    for i in range(len(date)):
        print(date[i]["year"][0]+date[i]["year"][1]
            + date[i]["month"][0]+date[i]["month"][1]
            + date[i]["day"][0]+date[i]["day"][1])


through_mecab()
pick_date()
print_date()
