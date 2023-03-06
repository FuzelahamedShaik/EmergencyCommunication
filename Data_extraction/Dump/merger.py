import pandas as pd

suomi112_ap_en = pd.read_csv("112 Suomi apple store en.csv")
suomi112_ps_en = pd.read_csv('112 Suomi play store en.csv')
suomi112_ps_fi = pd.read_csv('112 Suomi play store fi.csv')

hjelp113_ap_en = pd.read_csv("Hjelp 113 apple store en.csv")
hjelp113_ps_en = pd.read_csv('Hjelp 113 play store en.csv')
hjelp113_ps_fi = pd.read_csv('Hjelp 113 play store fi.csv')

sos_ap_en = pd.read_csv("SOS Alarm apple store en.csv")
sos_ps_en = pd.read_csv('SOS Alarm play store en.csv')
sos_ps_fi = pd.read_csv('SOS Alarm play store fi.csv')

pd.concat([suomi112_ap_en,suomi112_ps_en,suomi112_ps_fi]).to_csv('..\suomi112.csv',index=False)
pd.concat([hjelp113_ap_en,hjelp113_ps_en,hjelp113_ps_fi]).to_csv('..\hjelp113.csv',index=False)
pd.concat([sos_ap_en,sos_ps_en,sos_ps_fi]).to_csv('..\sosalarm.csv',index=False)

print("All files created!!")