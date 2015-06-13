from setuptools import setup

setup(name='asynctools',
  version='0.1',
  description='Handy tools and patterns for distributed async processing',
  url='http://github.com/JosiahKerley/asynctools',
  author='Josiah Kerley',
  author_email='josiahkerley@gmail.com',
  license='MIT',
  packages=['asynctools'],
  install_requires=['redis',],
  zip_safe=False,)
