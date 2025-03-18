from setuptools import setup, find_packages

setup(
    name='gapitoo',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'tqdm',
    ],
    author='ArtemB',
    description='Up-/Down- load stuff from google drive',
    url='https://github.com/melonheader/gapitoo',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
)
