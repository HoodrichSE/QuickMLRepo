from setuptools import find_packages,setup
from typing import List

REQ_BUILD_FLAG='-e .'
def get_requirements(filepath:str) -> List:
    '''
    This function reads package requirements from the given filepath
    '''
    requirements=[]
    with open(filepath) as filestream:
        requirements=filestream.readlines()
        # Remove endlines from .txt file
        [req.replace("\n","") for req in requirements]
        if REQ_BUILD_FLAG in requirements:
            requirements.remove(REQ_BUILD_FLAG)
    return requirements

setup(
name='quickml',
version='0.0.1',
author='SpencerG',
author_email='goodrichse@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)