from setuptools import setup
from setuptools.command.install import install
import os


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        os.system("systemctl restart audioswitch.service")


setup(name="audioswitch",
      version='0.1',
      description='Swap audio on headphone events',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      author='flare561',
      license='MIT',
      packages=['audioswitch'],
      entry_points={
          'console_scripts': ['audioswitch=audioswitch:main'],
      },
      data_files=[('/etc/systemd/system/', ['audioswitch.service'])],
      cmdclass={'install': PostInstallCommand}
      )
