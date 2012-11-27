from setuptools import setup, find_packages

setup(name='nose-mongorunner',
      version="0.1.0",
      classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP'],
      author='Roman Kalyakin',
      author_email='roman@kalyakin.com',
      description="Nose plugin for automating mongodb for tests runs.",
      long_description=open("README.txt").read(),
      url='http://pypi.python.org/pypi/mongonose',
      license='BSD-derived',
      packages=find_packages(exclude=('tests',)),
      install_requires=["nose","pymongo"],
      include_package_data=True,
      tests_require=["nose"],
      test_suite = "nose.collector",
      zip_safe=True,
      entry_points="""\
      [nose.plugins.0.10]
      mongodb = mongonose:MongoDBPlugin
      """
      )
