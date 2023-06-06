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
    sql="select cuse_desc_thai from TRANSCRIPTS_COUSE"
    cursor.execute(sql)
    rows = cursor.fetchall()  
            

    
    
    data_desc=[word_tokenize(str(text[0]).replace('\r\n', ' ').replace('\n', ' ').replace(' ', ''), engine="newmm") for text in rows ]
    listData= [[" ".join(getData),count] for count ,getData in enumerate(data_desc) ] 
    tokens =description
    data=word_tokenize(tokens.replace('\r\n', ' ').replace('\n', ' ').replace(' ', ''), engine="newmm")

    joinData = " ".join(data)

    showeData=process.extract(joinData,listData, limit=10,  scorer=fuzz.token_sort_ratio)
    items=[]

    status=1

    for item in showeData:
        
        dataInitem=item[0][0].replace(' ', '')
        subitem=[]
      
        if status==1:    
            subitem.append(dataInitem)
            subitem.append(item[0][1]+1)
            subitem.append(item[1])
            items.append(subitem)
            status=0
        elif old_dataInitem!=dataInitem:
            subitem.append(dataInitem)
            subitem.append(item[0][1]+1)
            subitem.append(item[1])
            items.append(subitem)
        old_dataInitem=dataInitem

    print(items)
    cursor=conn.close()
    conn.close()

    return items
