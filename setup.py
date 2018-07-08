from setuptools import setup, find_packages

requires = [
    'numpy',
]

setup(
    name='iba2raystation',
    include_package_data=True,
    packages=find_packages(),
    version='0.1.4',
    description='Converts an IBA OmniPro Accept CSV into a RaySearch RayStation CSV',
    author='Dan Cutright',
    author_email='dan.cutright@gmail.com',
    url='https://github.com/cutright/IBA2RayStation',
    download_url='https://github.com/cutright/DVH-Analytics/archive/master.zip',
    license="MIT License",
    keywords=['radiation therapy', 'beam commissioning'],
    classifiers=[],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'iba2rs=iba2rs.main:main',
        ],
    },
    long_description="""IBA2RayStation
    
    This program will convert an IBA OmniPro Accept CSV file into a RayStation CSV file for beam commissioning.
    """
)