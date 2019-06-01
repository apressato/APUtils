import setuptools

def read_file(filename, mode='r'):
    "returns content from filename, making sure to close the file explicitly on exit."
    f = open(filename, mode)
    try:
        return f.read()
    finally:
        f.close()	
	
setuptools.setup(
     name = 'APUtils',  
     version = read_file("VERSION").split()[1],
     author = "Ascanio Pressato",
     author_email = "apressato.oss@gmail.com",
     description = "A Simple Utility Package",
     long_description = read_file("README.md"),
     long_description_content_type = "text/markdown",
     url = "",
     packages = ['APUtils'],
	 license = 'CC-BY-SA-4.0',
     classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",        
        "Programming Language :: Python :: 2",
        "License :: Creative Commons Attribution ShareAlike 4.0 International",
        "Operating System :: OS Independent",
     ],
     platforms = 'Windows, Linux, Unix, Windows Mobile',
 )
