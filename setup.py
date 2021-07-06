from setuptools import setup

long_description = open('README.rst').read()

setup(
    name="celery-jalalicrontab",
    description="A Celery schedule corntab which is work with jalali calendar",
    long_description=long_description,
    version="1.0.1",
    url="https://github.com/saber-solooki/jalalicrontab",
    license="Apache License, Version 2.0",
    author="Saber Solooki",
    author_email="saber.solooki@gmail.com",
    keywords="python celery schedule jalali calendar".split(),
    packages=["jalalicrontab"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Object Brokering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
    ],
    install_requires=['celery>=4.2', 'jdatetime~=3.6.0'],
    tests_require=['pytest'],
    long_description_content_type="text/x-rst"
)
