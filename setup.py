import setuptools
long_description = "Simple JSON database";
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name = "repositories-jimobama",
      version="1.0.0",
      description="Simple JSON database manager for python",
      long_description =long_description,
      url="https://github.com/miljimo/repositories.git",
      long_description_content_type="text/markdown",
      author="Obaro I. Johnson",
      author_email="johnson.obaro@hotmail.com",
      packages=setuptools.find_packages(),
      install_requires=[ "Crypto"],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",         
    ],python_requires='>=3.0');

