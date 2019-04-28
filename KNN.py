import pandas as pd
import numpy as np
from math import sqrt

dosya_adi = "Iris"

ham_veri = pd.read_csv(dosya_adi + ".csv")
veri = ham_veri.copy()

#girdiler
sutun_indexi = 5
k = 4
sinif_belirleme = 1
class_index = sutun_indexi

girdi = [0, 4.9, 3, 1.4, 0.2]

def min_max_norm(sutun, adi):
    ek = min(sutun)
    eb = max(sutun)
    yeni_degerler = []
    yeni_dic = {}
    for i in sutun:
        yeni_degerler.append((i - ek) / float(eb - ek))

    yeni_dic[adi] = yeni_degerler

    return pd.DataFrame(yeni_dic)

def normalizasyon(veri, sutun_indexi):
    sutun_adlari = veri.columns
    veri = veri.drop(sutun_adlari[sutun_indexi], axis=1)
    yeni_sutunlar = []

    for i in range(len(sutun_adlari) - 1):
        yeni_sutunlar.append(min_max_norm(veri.iloc[:, i], sutun_adlari[i]))

    yeni_frame = yeni_sutunlar[0]
    for i in range(1, len(yeni_sutunlar)):
        yeni_frame = pd.concat([yeni_frame, yeni_sutunlar[i]], axis=1)

    return yeni_frame

#normalizasyon
sutunlar=veri.columns.tolist()
sutunlar.remove(sutunlar[sutun_indexi])

a={}
m=0
for i in sutunlar:
    a[i] = [girdi[m]]
    m += 1

a[veri.columns.tolist()[sutun_indexi]] = "Nan"
a = pd.DataFrame(a)

sahte_veri = veri.append(a,sort=False)
veri_norm = normalizasyon(sahte_veri, sutun_indexi)
yeni_min_uygulanmis = veri_norm.iloc[-1,:]
veri_norm = veri_norm.iloc[:-1,:]

yeni_uzakliklar = []

#oklid uygulaniyor
for i in range(veri_norm.shape[0]):
    t = 0.0
    for j in range(veri_norm.shape[1]):
        t += (yeni_min_uygulanmis.iloc[j] - veri_norm.iloc[i, j]) ** 2
    yeni_uzakliklar.append(sqrt(t))

min_uzakliklar = []  # [degeri,indexi]
indexler = []
yeni_uzakliklar_yedek = yeni_uzakliklar[:]

#en kisa k tane uzaklik bulunuyor
for i in range(k):
    indexler.append(yeni_uzakliklar_yedek.index(min(yeni_uzakliklar)))
    yeni_uzakliklar.remove(yeni_uzakliklar_yedek[indexler[i]])

#k tane kisanin nitelikleri aliniyor
nitelikler = []
for i in indexler:
    nitelikler.append(veri.iloc[i, sutun_indexi])

#sinif sutununun nitelikleri
nitelik_adlari = veri.groupby(veri.columns[sutun_indexi])[veri.columns[sutun_indexi]].count().keys().tolist()
sayilar = np.zeros((len(nitelik_adlari,)))

#sinif belirleme

#en cok tekrarlanan
if sinif_belirleme == 1:
    #hangi nitelikten kac tane var sayiliyor
    for i in range(len(nitelikler)):
        for j in range(len(nitelik_adlari)):
            if nitelikler[i] == nitelik_adlari[j]:
                sayilar[j] += 1
                break

    #en cok tekrarlanan
    for i in range(len(sayilar)):
        if sayilar[i] == np.max(sayilar):
            print "\n"+str(girdi[:])
            print str(nitelik_adlari[i])+" sinifina aittir."
            break

#agirlikli
else:
    #agirliklar hesaplaniyor
    for i in range(k):
        for j in range(len(nitelik_adlari)):
            if nitelikler[i] == nitelik_adlari[j]:
                a = round(yeni_uzakliklar_yedek[indexler[i]],2)
                b = a * a
                c = round(1/(b),2)
                sayilar[j] += c
                break

    #en buyuk bulunuyor
    eb=0
    for i in range(len(sayilar)):
        if sayilar[i] > eb:
            eb=i

    print "\n" + str(girdi[:])
print str(nitelik_adlari[eb]) + " sinifina aittir."
