import typing
from typing import List
import pickle as pck
from google.cloud import storage
from itertools import takewhile

def read_pc_file(i: int) -> List[str]:
    storage_client = storage.Client()
    files_list = storage_client.list_blobs('reports_123', prefix="data/pc")
    blob_list = storage_client.bucket('reports_123')
    j = 0
    #if i == 0:
        #blob = storage_client.blob(files_list.next())
    #else:
    for fil in takewhile(lambda e: j != i+1, files_list): 
        blob = blob_list.blob(fil.name)
        j = j+1
    pickle_in = blob.download_as_string()
    
    pc_list = pck.loads(pickle_in)
    return([pc_list,fil.name])

def finished_list_exist() -> bool:
    storage_client = storage.Client()
    files_list = storage_client.bucket('reports_123')
    blob = files_list.blob("data/finished_list")
    return(blob.exists())
    
def finished_list_read() -> List[str]:
    try:
        storage_client = storage.Client()
        files_list = storage_client.bucket('reports_123')
        blob = files_list.blob("data/finished_list")
        finished_file = blob.download_as_bytes()
        finished_file = finished_file.decode()
        finished_list = finished_file.split("\n")
    except Exception as e:
        print(e)
        finished_list = "Does not Exist"
    return(finished_list)

def finished_list_dump(finished_list: List[str]) -> None:
    storage_client = storage.Client()
    files_list = storage_client.bucket('reports_123')
    blob = files_list.blob("data/finished_list")
    blob.upload_from_string("\n".join(finished_list))
