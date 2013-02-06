from setuptools import setup, find_packages

VERSION='0.1.0'

setup(name='mongobox',
      version=VERSION,
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
      author='Roman Kalyakin',
      author_email='roman@kalyakin.com',
      description="Run sandboxed Mongo DB instance from a python application.",
      long_description=open("README.md").read(),
      url='http://github.com/theorm/mongobox',
      license=open("LICENSE").read(),
			package_data={'':['LICENSE','README.md','AUTHORS.md']},
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
