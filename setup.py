import setuptools

version = '0.1'

setuptools.setup(name='fecru_api',
    version=version,
    description="Small wrapper for fecru REST API.",
    long_description="""\
""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    keywords='atlassian fecru fisheye crucible',
    author='InfraDX Team',
    author_email='novum-infradx@telefonica.com',
    url='https://github.com/Telefonica/fecru_api',
    packages=setuptools.find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.7",
    install_requires=[
       "simplejson",
    ],
)
