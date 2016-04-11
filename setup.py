from setuptools import setup

setup(name='randle',
      version='0.7',
      packages=['randle'],
      entry_points={
          'console_scripts': [
              'randle = randle.__main__:main'
          ]
      },
      )
