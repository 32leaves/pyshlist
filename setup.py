from setuptools import setup

setup(name='pyshlist',
      version='0.1',
      description='Command-line tool for managing your wishlist',
      url='http://github.com/32leaves/pyshlist',
      author='Christian Weichel',
      author_email='chris@32leav.es',
      license='MIT',
      py_modules = ['pyshlist'],
      install_requires = [
          'Click',
          'tinydb',
          'pandas',
          'numpy',
          'matplotlib'
      ],
      entry_points = {
          'console_scripts': [
            'pyshlist = pyshlist.command_line:main'
          ],
      },
      zip_safe=True)
