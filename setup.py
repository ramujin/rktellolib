from setuptools import find_packages, setup

setup(
  name='rktellolib',
  packages=find_packages(include=['rktellolib']),
  version='1.0.0',
  license='MIT',
  description='A simple library to interface with the DJI Tello drone',
  author='Ramsin Khoshabeh',
  author_email='ramsin@ucsd.edu',
  url='https://github.com/ramujin',
  download_url='https://github.com/ramujin/rktellolib/archive/v1.0.0.tar.gz',
  keywords=['dji', 'tello', 'ryze', 'drone', 'sdk', 'official sdk'],
  install_requires=[
    'opencv-python',
  ],
  python_requires='>=3.5',
  classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
  ],
)