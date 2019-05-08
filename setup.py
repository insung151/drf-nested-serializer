from io import open

from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

version = '0.1.0'


setup(
    name='drf-nested-serializer',
    version=version,
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
    test_suite='run_tests.run_tests'
)