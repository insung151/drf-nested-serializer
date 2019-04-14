from io import open

from setuptools import setup, find_packages
from drf_nested_serializer import __version__


with open('README.md') as f:
    long_description = f.read()


setup(
    name='drf-nested-serializer',
    version=__version__,
    url='https://github.com/insung151/drf-nested-serializer',
    description='nested serializer for django-rest-framework',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=('drf restframework rest_framework django_rest_framework'
              ' serializers def_nested_serializer'),
    author='Inseong Hwang',
    author_email='insung151@naver.com',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    test_suite='tests.run_tests'
)