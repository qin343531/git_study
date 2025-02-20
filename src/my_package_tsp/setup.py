from setuptools import setup

package_name = 'my_package_tsp'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/usb_test_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='qin',
    maintainer_email='qin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = my_package_tsp.publisher:main',
            'subscriber = my_package_tsp.subscriber:main',
            'serial_comm = my_package_tsp.serial_comm:main',
            'serial_pub = my_package_tsp.serial_publisher:main',
            'usb_cam_test_node = my_package_tsp.usb_cam_test:main',
            'keyboard_pub = my_package_tsp.keyboard_pub:main',
            "spi_comm = my_package_tsp.spi_comm:main"
        ],
    },
)
