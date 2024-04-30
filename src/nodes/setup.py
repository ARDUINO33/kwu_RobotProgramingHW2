import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*_launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='juwon',
    maintainer_email='77627794+ARDUINO33@users.noreply.github.com',
    description='ros2_Homework',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nodeOne = nodes.nodeOne:main',
            'nodeTwo = nodes.nodeTwo:main',
        ],
    },
)
