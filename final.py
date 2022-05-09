# 欠損点補間・データ削減・地面建物判定

"""
欠損点補完の説明

真ん中を欠損点として
2     2      2
19 13→19   20
20   21    20

欠損点を除く平均は106/8=13
13と四方の19 20 21 2を比べる
差の絶対値が一番小さい19で補完する


"""


print("開くファイルを入力:", end=" ")
f = open(input(), "r")
points = f.readlines()   # 各行がリストへ格納

for i,v in enumerate(points):
	points[i] = v.replace("\n", "")   # 改行を削除
	points[i]= list(map(float,(points[i].split())))   # スペースで区切られたデータをsplitで分けて型変換、リスト化

f.close()
"""
print(points[0])
print(points[0][0])
print(points.index([-7542.0, -36050.0, 23.56]))

[-7542.0, -36050.0, 23.56]
-7542.0
0
"""
#######################################################################

import time
start = time.time()

for i in range(len(points)):
	if points[i][2] == -9999.99:
		cx=points[i][0]
		cy=points[i][1]
		z1=-1
		z2=-1
		z3=-1
		z4=-1
		z5=-1
		z6=-1
		z7=-1
		z8=-1
		kcount=0

		for j in range(len(points)):
			if points[j][0]==cx-1:
				if points[j][1]==cy-1:
					if points[j][2]!= -9999.99:
						z7=points[j][2]
					else:
						z7=0
						kcount=kcount+1
				if points[j][1]==cy:
					if points[j][2]!= -9999.99:
						z8=points[j][2]
					else:
						z8=0
						kcount=kcount+1
				if points[j][1]==cy+1:
					if points[j][2]!= -9999.99:
						z1=points[j][2]
					else:
						z1=0
						kcount=kcount+1
			if points[j][0]==cx:
				if points[j][1]==cy-1:
					if points[j][2]!= -9999.99:
						z6=points[j][2]
					else:
						z6=0
						kcount=kcount+1
				if points[j][1]==cy+1:
					if points[j][2]!= -9999.99:
						z2=points[j][2]
					else:
						z2=0
						kcount=kcount+1
			if points[j][0]==cx+1:
				if points[j][1]==cy-1:
					if points[j][2]!= -9999.99:
						z5=points[j][2]
					else:
						z5=0
						kcount=kcount+1
				if points[j][1]==cy:
					if points[j][2]!= -9999.99:
						z4=points[j][2]
					else:
						z4=0
						kcount=kcount+1
				if points[j][1]==cy+1:
					if points[j][2]!= -9999.99:
						z3=points[j][2]
					else:
						z3=0
						kcount=kcount+1
			if z1!=-1 and  z2!=-1 and  z3!=-1 and  z4!=-1 and  z5!=-1 and  z6!=-1 and  z7!=-1 and  z8!=-1:
				break
		
		points[i][2]=0
		points[i][2]=points[i][2]+z1
		points[i][2]=points[i][2]+z2
		points[i][2]=points[i][2]+z3
		points[i][2]=points[i][2]+z4
		points[i][2]=points[i][2]+z5
		points[i][2]=points[i][2]+z6
		points[i][2]=points[i][2]+z7
		points[i][2]=points[i][2]+z8
		if kcount!=8:
			points[i][2]=points[i][2]/(8-kcount)  #平均化
		
		
		min=abs(points[i][2]-z2)
		idx=2
		if min>abs(points[i][2]-z4):
			min=abs(points[i][2]-z4)
			idx=4
		if min>abs(points[i][2]-z6):
			min=abs(points[i][2]-z6)
			idx=6
		if min>abs(points[i][2]-z8):
			min=abs(points[i][2]-z8)
			idx=8
			
		
		if idx==2:
			points[i][2]=z2
		elif idx==4:
			points[i][2]=z4
		elif idx==6:
			points[i][2]=z6
		elif idx==8:
			points[i][2]=z8

"""
kesson_index = []
for i in range(len(points)):
	if points[i][2] == -9999.99:
		kesson_index.append(i + 1)

print(kesson_index) #欠損点がないかどうか確かめる
"""

p=[]
p.append(points[0])
s=1
for i in range(1,len(points)-1):
	cz=points[i][2]
	if abs(points[i-1][2]-cz)>=0.5 or abs(points[i+1][2]-cz)>=0.5:
		p.append(points[i])
		s=s+1

p.append(points[len(points)-1])


from operator import itemgetter
sorted_p = sorted(p, key=itemgetter(2))   # pのz座標(p[i][2])について昇順にソート
sum = 0
cnt = 0
for i in range(100000):
    sum += sorted_p[i][2]
    cnt += 1

stan_G_lv = sum/cnt   # 基準の地面の標高
print("10万個の平均", stan_G_lv)

jimen = []
tatemono = []
GorB = []   # 建物の時1、地面の時0を格納
for i in range(len(p)):
    if i == 0 or p[i][1] == p[i - 1][1] + 1:   # i==0またはp[i]が折り返した直後の点だった時
        if p[i][2] - stan_G_lv >= 4.0:
            tatemono.append(p[i])
            GorB.append(1)
        else:
            jimen.append(p[i])
            GorB.append(0)
    else:
        if p[i][2] - stan_G_lv < 4.0:
            jimen.append(p[i])
            GorB.append(0)
        else:
            if GorB[i - 1] == 1:   # 自分の一つ前(左隣)の点が建物の時
                if p[i][2] - p[i - 1][2] >= -4.0:
                    tatemono.append(p[i])
                    GorB.append(1)
                else:
                    if p[i][2] - stan_G_lv >= 15:
                        tatemono.append(p[i])
                        GorB.append(1)
                    else:
                        jimen.append(p[i])
                        tatemono.append([p[i][0], p[i][1], 0])
                        GorB.append(0)
            else:   # 自分の一つ前(左隣)の点が地面の時
                if p[i][2] - p[i - 1][2] >= 3.5:   # 自分の方が3.5m以上高い時
                    tatemono.append([p[i - 1][0], p[i - 1][1], 0])
                    tatemono.append(p[i])
                    GorB.append(1)
                else:
                    jimen.append(p[i])
                    tatemono.append([p[i][0], p[i][1], 0])
                    GorB.append(0)



# 外周を囲う為の点(建物と扱う)
haji_t_1 = []
haji_t_2 = []
haji_t_3 = []
haji_t_4 = []
tatemono_2 = sorted(tatemono, key=itemgetter(1))
last_y = tatemono_2[len(tatemono_2) - 1][1]
idx = 0
for i in range(len(tatemono)):
	if tatemono[i][1] == tatemono[0][1]:
		haji_t_1.append(tatemono[i])
	else:
		idx = i
		break

for i in range(idx, len(tatemono)):                             #  ________4_________
    if i == idx:                                                #  |                 |
        haji_t_2.append(tatemono[i])                            #  |                 |
    else:                                                       # 2|                 |3
        if tatemono[i][1] != tatemono[i - 1][1]:                #  |                 |
            haji_t_3.append(tatemono[i - 1])                    #  |_________________|
            if tatemono[i][1] == last_y:                        #          1
                idx = i
                break
            else:
                haji_t_2.append(tatemono[i])

for i in range(idx, len(tatemono)):
    if tatemono[i][1] == tatemono[idx][1]:
        haji_t_4.append(tatemono[i])

end = time.time()
print("欠損点補間・点削減・地面建物判定に要した時間:", end - start)
print("判定完了")

# ファイルへの書き込みをする準備。まずは地面
for i in range(len(jimen)):
    jimen[i] = str(jimen[i]).strip("[]")   # 要素の先頭と末尾から見て、""内の文字がどれか一つでもあったら削除。そうでない文字に当たると見るのをやめる
    jimen[i] = str(jimen[i]).replace(",", " ")   # 要素にある""内の文字を全て右側の""内の文字に置き換える
												 # 今回は半角スペース。何も書かない場合は削除という扱いになる
    jimen[i] = str(jimen[i]).replace("'", "")   # stripやreplaceを使う時はstr(文字列と扱う)と書かないと駄目らしい

jimen = "\n".join(jimen)   # 要素ごとに""内の文字で区切る。この場合は改行で区切る

# ファイルへ書き込む
print("地面の点データを書き込むファイルを入力:", end=" ")
F_jimen = open(input(), "w")   # 入力したファイルに上書き。ファイルがない場合は自動的につくる
F_jimen.write(str(jimen))

# ファイルへの書き込みをする準備。次に建物
for i in range(len(tatemono)):
    tatemono[i] = str(tatemono[i]).strip("[]")   # 要素の先頭と末尾から見て、""内の文字がどれか一つでもあったら削除。そうでない文字にぶち当たると見るのをやめる
    tatemono[i] = str(tatemono[i]).replace(",", " ")   # 要素にある""内の文字を全て右側の""内の文字に置き換える
													   # 今回は半角スペース。何も書かない場合は削除という扱いになる
    tatemono[i] = str(tatemono[i]).replace("'", "")   # stripやreplaceを使う時はstr(文字列と扱う)と書かないと駄目らしい

tatemono = "\n".join(tatemono)   # 要素ごとに""内の文字で区切る。この場合は改行で区切る

# ファイルへ書き込む
print("建物の点データを書き込むファイルを入力:", end=" ")
F_tatemono = open(input(), "w")   # 入力したファイルに上書き。ファイルがない場合は自動的につくる
F_tatemono.write(str(tatemono))

# haji_t_1を書き込む
for i in range(len(haji_t_1)):
    haji_t_1[i] = str(haji_t_1[i]).strip("[]")
    haji_t_1[i] = str(haji_t_1[i]).replace(",", " ")
    haji_t_1[i] = str(haji_t_1[i]).replace("'", "")
haji_t_1 = "\n".join(haji_t_1)
print("haji_t_1を書き込むファイルを入力:", end=" ")
F_1 = open(input(), "w")
F_1.write(str(haji_t_1))

# haji_t_2を書き込む
for i in range(len(haji_t_2)):
    haji_t_2[i] = str(haji_t_2[i]).strip("[]")
    haji_t_2[i] = str(haji_t_2[i]).replace(",", " ")
    haji_t_2[i] = str(haji_t_2[i]).replace("'", "")
haji_t_2 = "\n".join(haji_t_2)
print("haji_t_2を書き込むファイルを入力:", end=" ")
F_2 = open(input(), "w")
F_2.write(str(haji_t_2))

# haji_t_3を書き込む
for i in range(len(haji_t_3)):
    haji_t_3[i] = str(haji_t_3[i]).strip("[]")
    haji_t_3[i] = str(haji_t_3[i]).replace(",", " ")
    haji_t_3[i] = str(haji_t_3[i]).replace("'", "")
haji_t_3 = "\n".join(haji_t_3)
print("haji_t_3を書き込むファイルを入力:", end=" ")
F_3 = open(input(), "w")
F_3.write(str(haji_t_3))

# haji_t_4を書き込む
for i in range(len(haji_t_4)):
    haji_t_4[i] = str(haji_t_4[i]).strip("[]")
    haji_t_4[i] = str(haji_t_4[i]).replace(",", " ")
    haji_t_4[i] = str(haji_t_4[i]).replace("'", "")
haji_t_4 = "\n".join(haji_t_4)
print("haji_t_4を書き込むファイルを入力:", end=" ")
F_4 = open(input(), "w")
F_4.write(str(haji_t_4))

"""
プログラムの実行と入力例

★ターミナルで「python final.py」を実行

開くファイルを入力: 53394640_dsm_1m.dat
10万個の平均 7.443545300000119
欠損点補間・点削減・地面建物判定に要した時間: 22.195932865142822
判定完了
地面の点データを書き込むファイルを入力: jimen_40_final.dat
建物の点データを書き込むファイルを入力: tatemono_40_final.dat
haji_t_1を書き込むファイルを入力: haji_t_1.dat
haji_t_2を書き込むファイルを入力: haji_t_2.dat
haji_t_3を書き込むファイルを入力: haji_t_3.dat
haji_t_4を書き込むファイルを入力: haji_t_4.dat
"""
