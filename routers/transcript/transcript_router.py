from fastapi import APIRouter
from pythainlp import word_tokenize
from thefuzz import fuzz, process
import sqlite3


router=APIRouter(
    prefix="/transcript",
    tags=["transcript"]
)



@router.get("/{description}")
def getData(description: str):
    data=transcripts(description)
    return {"data":data}


def transcripts(description):   
    # try:
    conn=sqlite3.connect('TS.db')
    cursor=conn.cursor()
    sql="select id,code_couse,couse_thai,cuse_desc_thai from TRANSCRIPTS_COUSE"
    cursor.execute(sql)
    rows = cursor.fetchall()  
            

    listRows=[list(row) for row in rows ]
    
    data_desc=[word_tokenize(str(text[3]).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace(' ', ''), engine="newmm") for text in listRows ]
    # listData= [[" ".join(getData),count] for count ,getData in enumerate(data_desc) ] 
    listData= [" ".join(getData) for getData in data_desc]
    tokens =description
    data=word_tokenize(tokens.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace(' ', ''), engine="newmm")

    joinData = " ".join(data)
   
    showeData=process.extract(joinData,listData, limit=10,  scorer=fuzz.token_sort_ratio)
    

    

    items=[]

    status=1

    for item in showeData:
     
        dataInitem=item[0].replace(' ', '')
       

        

        if status==1:
            for ilen in range(len(listData)):
                strngChecker=str(item[0])
                subitem=[]
            
                if strngChecker==listData[ilen]:
                
                    subitem.append(listRows[ilen][0])
                    subitem.append(listRows[ilen][1])
                    subitem.append(listRows[ilen][2])
                    subitem.append(listRows[ilen][3])
                    subitem.append(f"ความมั่นใจ {item[1]}%")
                    items.append(subitem)
                    status=0
        elif old_dataInitem!=dataInitem:
             for ilen in range(len(listData)):
                strngChecker=str(item[0])
                subitem=[]
            
                if strngChecker==listData[ilen]:
                  
                    subitem.append(listRows[ilen][0])
                    subitem.append(listRows[ilen][1])
                    subitem.append(listRows[ilen][2])
                    subitem.append(listRows[ilen][3])
                    subitem.append(f"ความมั่นใจ {str(item[1])}%")
                    items.append(subitem)
  
        old_dataInitem=dataInitem

    for i in items:
        print(i)
    cursor=conn.close()
    conn.close()

    return items

