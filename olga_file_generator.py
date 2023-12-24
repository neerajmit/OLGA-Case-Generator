import pandas as pd
import numpy as np
import re

def vlookup_nearest(df, key, key_column, value_column):
    #print(list(df2.values))
    if key in df[key_column].values:
        return df[df[key_column] == key][value_column].values[0]
    else:
        nearest_key = min(df[key_column], key=lambda x: abs(x - key))
        return df[df[key_column] == nearest_key][value_column].values[0]
    
def perform_text_replacements(text,pattern,replacements):
    #print(text)
    modified_text = re.sub(pattern, lambda match: str(replacements.get(match.group(0), match.group(0))) if type(replacements.get(match.group(0), match.group(0)))!=str else replacements.get(match.group(0), match.group(0)), text, flags=re.IGNORECASE)
    #print(modified_text)
    return modified_text

mmscmd_to_kg=8.01567999968288
df1=pd.DataFrame({
    'A': [5, 10],
    'B': [2, 3]
})
df2=pd.DataFrame({
    'C': [3, 5],
    'D': [1.05920849398568, 1.07543823345383],
    'E': [1.09407237876912, 1.11030211823728]
  })
df3=pd.DataFrame({
    'F': [1, 12],
    'G': [2, 0.117],
    'H':[3,0],
    'I':[0.5,0],
    'J':[5,0.328]
  })
df4=pd.DataFrame({
    'K': [1, 12],
    'L': [3797.7, 810],
    'M':[3314.7,1200],
    'N':[3414.7,2000],
    'O':[2514.7,800]
  })
df5=pd.DataFrame({
    'P': [1, 12],
    'Q': [89, 89],
    'R':[79,79],
    'S':[98,98],
    'T':[85,85]
  })
df6=pd.DataFrame({
    'U': [1, 12],
    'V': [0.005, 0.1],
    'W':[0.005,0],
    'X':[0.005,0],
    'Y':[0.005,0]
  })

def process_data(file, year, diameter, wgr, cgr, neq):
    base_df=pd.read_csv(file, delimiter='\t')

    year=float(year)
    diameter=float(diameter)
    wgr=float(wgr)
    cgr=float(cgr)
    neq=float(neq)

    #keyname="wc"+str(wgr)+"cgr"+str(cgr)+"y"+str(year)+"d"+str(diameter)+".inp"
    ZCASE="WGR="+str(wgr)+";CGR"+str(cgr)+";D"+str(diameter)+";Y="+str(year)
    ZDIAM=diameter
    ZEQUIPIPE=neq

    D_or_E='D' if vlookup_nearest(df1,cgr,'A','B')==2 else 'E'
    ZEGT=round(vlookup_nearest(df3,year,'F','G')*vlookup_nearest(df2,wgr,'C', D_or_E)*mmscmd_to_kg,4)
    ZDGT=round(vlookup_nearest(df3,year,'F','H')*vlookup_nearest(df2,wgr,'C', D_or_E)*mmscmd_to_kg,4)
    ZNGT=round(vlookup_nearest(df3,year,'F','I')*vlookup_nearest(df2,wgr,'C', D_or_E)*mmscmd_to_kg,4)
    ZGGT=round(vlookup_nearest(df3,year,'F','J')*vlookup_nearest(df2,wgr,'C', D_or_E)*mmscmd_to_kg,4)

    ZERP=vlookup_nearest(df4,year,'K','L')
    ZDRP=vlookup_nearest(df4,year,'K','M')
    ZNRP=vlookup_nearest(df4,year,'K','N')
    ZGRP=vlookup_nearest(df4,year,'K','O')

    ZERT=vlookup_nearest(df5,year,'P','Q')
    ZDRT=vlookup_nearest(df5,year,'P','R')
    ZNRT=vlookup_nearest(df5,year,'P','S')
    ZGRT=vlookup_nearest(df5,year,'P','T')

    ZEBIAS=vlookup_nearest(df6,year,'U','V')
    ZDBIAS=vlookup_nearest(df6,year,'U','W')
    ZNBIAS=vlookup_nearest(df6,year,'U','X')
    ZGBIAS=vlookup_nearest(df6,year,'U','Y')

    ZTHERMO='wc'+str(wgr)+'cgr'+str(cgr)
    ZRESTART="wc"+str(wgr)+"cgr"+str(cgr)+"y"+str(year)+"d"+str(diameter)

    ZDOPEN=1
    ZNOPEN=1
    ZEOPEN=1
    ZGOPEN=1


    replacements={
        'ZCASE':ZCASE,
        'ZDIAM':ZDIAM,
        'ZEQUIPIPE':ZEQUIPIPE,
        'ZEGT':ZEGT,
        'ZDGT':ZDGT,
        'ZNGT':ZNGT,
        'ZGGT':ZGGT,
        'ZERP':ZERP,
        'ZDRP':ZDRP,
        'ZNRP':ZNRP,
        'ZGRP':ZGRP,
        'ZERT':ZERT,
        'ZDRT':ZDRT,
        'ZNRT':ZNRT,
        'ZGRT':ZGRT,
        'ZEBIAS':ZEBIAS,
        'ZDBIAS':ZDBIAS,
        'ZNBIAS':ZNBIAS,
        'ZGBIAS':ZGBIAS,
        'ZTHERMO':ZTHERMO,
        'ZRESTART':ZRESTART,
        'ZDOPEN':ZDOPEN,
        'ZNOPEN':ZNOPEN,
        'ZEOPEN':ZEOPEN,
        'ZGOPEN':ZGOPEN

    }


    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in replacements.keys()) + r')\b'

    text_list=[]

    for i in range(1, base_df.shape[0]+1):
        text1 = base_df.iloc[i - 1, 0] 
        if text1!="" and not base_df.isna().iloc[i - 1, 0]: 
          text1 = perform_text_replacements(text1,pattern=pattern,replacements=replacements)
          text_list.append(text1)

    new_case = pd.DataFrame(text_list, columns=[0], index=None)

    return new_case