from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='fecru_api',
      version=version,
      description="Small wrapper for fecru REST API.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='atlassian fecru fisheye crucible',
      author='Jose Plana',
      author_email='jplana@tuenti.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=["simplejson",
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
