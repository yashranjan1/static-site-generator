import os
from shutil import rmtree, copy

def init() -> None:
    """
        Prepares the public folder and make sure that all the required folders and files exist

        Takes:
        
        Returns: `None`
    """
    if not os.path.exists('./static/'):
        raise Exception('static folder must exist')
    public_path = './public/'
    if os.path.exists(public_path):
        rmtree(public_path)
    os.mkdir('./public/')

def copy_files(from_path: str, to_path: str) -> None:
    """
        Copies over the files from static to public.

        Takes:
        `from_path: str` => A path to copy from 
        `to_path: str` => A path to copy to
        
        Returns: `None`
    """
    files = os.listdir(from_path)
    for file in files:
        if os.path.isfile(f'{from_path}/{file}'):
            copy(f'{from_path}/{file}', to_path)
        else:
            if not os.path.exists(f'{to_path}/{file}'):
                os.mkdir(f'{to_path}/{file}')
            copy_files(f'{from_path}/{file}', f'{to_path}/{file}')
    

def main():
    init()
    copy_files('./static', './public')

if __name__ == "__main__":
    main()
