from setuptools import setup, find_packages
 
setup(
    name='cinderella',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.0.2',
        'mysqlclient>= 1.4.2.post1',
        'pyzmq>=17.1.2',
    ]
)
