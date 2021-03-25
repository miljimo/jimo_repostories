import setuptools
import os;

long_description = "Simple JSON database";
readMEFile =  "README.md"
if (os.path.exists(readMEFile)):
  with open(readMEFile , "r") as fh:
      long_description = fh.read()
    
setuptools.setup(name = "jimobama_repositories",
      version="1.2.0",
      description="Simple JSON database manager for python",
      long_description =long_description,
      long_description_content_type="text/markdown",
      author="Obaro I. Johnson",
      author_email="johnson.obaro@hotmail.com",
      packages=["jimobama_repositories"],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",         
    ],python_requires='>=3.0');

