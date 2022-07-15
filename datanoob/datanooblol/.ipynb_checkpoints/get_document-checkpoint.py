import os

def init_doc():
    """
    Initialize doc
    
    """
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make html"
    os.system(command)
    copy_to()

def update_doc():
    """
    Update doc
    
    """
    
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make clean html"
    os.system(command)
    copy_to()

def copy_to():
    """
    Copy to document
    
    """
    source = "/usr/src/datanoob/_docs/_build/html/*"
    target = "/usr/src/datanoob/document"
    os.system(f"cp -Rf {source} {target}")