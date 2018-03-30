from setuptools import setup
setup(name='mecaruco',
      version=argiope.__version__,
      description="PROJ852: MECARUCO",
      long_description="",
      author='Ludovic Charleux',
      author_email='ludovic.charleux@univ-smb.fr',
      license='GPL v3',
      packages=['mecaruco'],
      zip_safe=False,
      url='https://github.com/lcharleux/mecaruco',
      install_requires=[
          "numpy",
          "scipy",
          "matplotlib",
          "pandas",
          "jupyter",
          "nbconvert"
          ],
      )
