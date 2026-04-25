'''
The setup.py filr is essential part of packaging and distributing Python projects. It is used by setuptools (or distutils in order Python versions) to define the configuration of the project, such as its metadata, dependencies and more
''' 

from setuptools import find_packages,setup   ###find_packages will scan intire this folder and where __init__.py it will find  that folder as package   ### setup is responsible to provide all the information regarding the project 
from typing import List 

def get_requirments()->List[str]:
    '''
    This function will return list of requirments
    '''
    requirments_lst:List[str]=[]
    try:
        with open('requirments.txt','r') as file:
            # Read Line from the file 
            lines= file.readlines()
            # Process each line 
            for line in lines:
                requirments = line.strip()
                # ignore empty lines and -e .
                if requirments and requirments!='-e .':
                    requirments_lst.appen(requirments)
    
    except FileNotFoundError:
        print("requirments.txt file not found")
        

    return requirments_lst


# setup my metadata
setup(
    name="Network Security",
    version="0.0.1",
    author="Ritesh Choudhari",
    author_email="riteshchoudhari003@gmail.com",
    packages=find_packages(),
    install_requires=get_requirments()
)
