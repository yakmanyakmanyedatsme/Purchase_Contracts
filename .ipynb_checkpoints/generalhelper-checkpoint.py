import typing
from typing import List
import pickle as pck

def read_pc_file(i):
    files = os.listdir("data/")
    file_names = os.path.join("data",files[i])
    pc_file = open(file_names,"rb")
    pc_list = pck.load(pc_file)
    pc_file.close()
    return(pc_list)
    
def finished_list_read() -> List[str]:
    finished_file = open("finished_list.pkl",'rb')
    finished_list = pck.load(finished_file)
    finished_file.close()
    return(finished_list)

def finished_list_dump(finished_list: List[str]) -> None:
    finished_file = open("finished_list.pkl",'wb')
    pck.dump(finished_list, finished_file)
    finished_file.close()
