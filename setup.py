from setuptools import setup

setup(name="Kaster",
      version="1.0",
      description="Offline CLI password manager",
      url="https://github.com/NOVAglow/kaster",
      author="Nguyen Hoang Duong",
      author_email="novakglow@gmail.com",
      license="MIT",
      install_requires=[
          "pyperclip",
          "Crypto"
      ],
      classifiers=[
          "Development Status :: 1 - Production/Stable",
          "Environment :: Linux",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Linux",
          "Topic :: Password Management"
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ],
      )
