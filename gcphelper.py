from google.cloud import storage
from typing import List, TypeVar, Dict

T1 = TypeVar('T')
def list_buckets(storage_client: str) -> None:
    """Lists all buckets."""
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        print(bucket.name)

def get_filepaths(client: storage.client.Client, bucket: str) -> List[str]:
    files_list = client.list_blobs(bucket)
    paths = []
    for file in files_list:
        paths.append(file.name)
    return(paths)


def get_fileblobs(client: storage.client.Client, bucket: str) -> Dict[str, storage.blob.Blob]:
    files_list = client.list_blobs(bucket)
    blobs = {}
    for file in files_list:
        blobs[file.name] = file
    return(blobs)

def get_data( blob_list: List[storage.blob.Blob], isTxt: bool = True) -> Dict[str, str]:
    data_dict = {}
    if isTxt:
        for blob in blob_list:
            try:
                data_dict[blob.name] = blob.download_as_string().decode('utf-8')
            except Exception as e:
                print(e)
                data_dict[blob.name] = e
    return(data_dict)
    

def get_data_from_names(client: storage.client.Client, file_names: List[str],
                         bucket: str, isTxt: bool = True) -> Dict[str,str]:
    blobs = get_fileblobs(client, bucket)
    blobs = [blobs[k] for k in file_names]
    data_dict = get_data(blobs, isTxt)
    return(data_dict)
    
        
            
        
        
        