#!/usr/bin/env python
from setuptools import setup, find_packages

from fees import VERSION

setup(
    name='django-fees',
    version=VERSION,
    description='Packages and plan subscriptions for Django',
    long_description=open('README.md').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-fees',
    packages=find_packages(),
    include_package_data=True,
    install_requires=('django', 'django-modeltrans', 'django-pragmatic'),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable'
    ],
    license='BSD License',
    keywords="django packages plans subscriptions pricing limitations",
)
