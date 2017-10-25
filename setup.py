from distutils.core import setup

setup(
    name='girder_jobmock',
    version='0.0.0',
    packages=['girder_jobmock',],
    license='Apache 2',
    install_requires=[
        'girder',
        'click'
    ],
    entry_points={
        'console_scripts': [
            "girder-jobmock = girder_jobmock.cli:cli"
        ]
    },
)
