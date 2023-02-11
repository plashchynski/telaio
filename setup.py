#!/use/bin/env python

from setuptools import setup

install_requires = [
    'av>=10.0.0',
    'numpy>=1.18.5',
    'ffmpeg-python>=0.2.0',
    'opencv-python>=4.7.0.68'
]

if __name__ == '__main__':
    setup(
            install_requires=install_requires
        )
