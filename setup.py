from setuptools import setup, find_packages

VERSION='0.1.0'

setup(name='mongobox',
      version=VERSION,
      description="Run sandboxed Mongo DB instance from a python application.",
      long_description=open("README.md").read(),
      url='http://github.com/theorm/mongobox',
      license=open("LICENSE").read(),
      author='Roman Kalyakin',
      author_email='roman@kalyakin.com',
      packages=find_packages(exclude=('tests',)),
      package_data={'':['LICENSE','*.md']},
      include_package_data=True,
      install_requires=[],
      zip_safe=False,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Testing'
      ],
      tests_require=["nose>=0.10","pymongo>=2.0"],
      test_suite = "nose.collector",
      entry_points={
        'nose.plugins.0.10': [
            'mongobox = mongobox.nose_plugin:MongoBoxPlugin',
        ],
      }
)
