from setuptools import setup, find_packages

setup(name='mongobox',
      version="0.1.0",
      classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP'],
      author='Roman Kalyakin',
      author_email='roman@kalyakin.com',
      description="Run sandboxed Mongo DB instance from a python app.",
      long_description=open("README.md").read(),
      url='http://github.com/theorm/mongobox',
      license=open("LICENSE").read(),
			package_data={'':['LICENSE']},
      packages=find_packages(exclude=('tests',)),
      install_requires=[],
      include_package_data=True,
      tests_require=["nose>=0.10","pymongo>=2.0"],
      test_suite = "nose.collector",
      zip_safe=True,
      entry_points={
        'nose.plugins.0.10': [
            'mongobox = mongobox.nose_plugin:MongoBoxPlugin',
        ],
      }
)
