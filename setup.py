import os
from setuptools import setup

setup(
    name='py-cron-schedule',
    version='0.0.1',
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),
    python_requires='>=3.4',
    url='https://github.com/Thoxvi/PyCronSchedule',
    author='Thoxvi',
    author_email='A@Thoxvi.com',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='lambda function',

    packages=["py_cron_schedule"],
)