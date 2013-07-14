from setuptools import setup, find_packages
import os


version = '1.0~dev'
ldesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(name='restdns-cli',
      version=version,
      description='A Command Line Interface for Restdns',
      long_description=ldesc,
      classifiers=['License :: OSI Approved :: MIT License'],
      keywords='cli restdns rest',
      author='Antoine Millet',
      author_email='antoine@inaps.org',
      url='https://github.com/NaPs/restdns-cli',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['restdns', 'restdns.clients'],
      include_package_data=True,
      zip_safe=True,
      entry_points={'restdns.clients.cli.commands': ['config = restdns.clients.cli.commands.config:Config',
                                                     'show = restdns.clients.cli.commands.show:Show',
                                                     'set = restdns.clients.cli.commands.set:Set',
                                                     'rset = restdns.clients.cli.commands.set:RSet',
                                                     'create = restdns.clients.cli.commands.create:Create',
                                                     'rcreate = restdns.clients.cli.commands.create:RCreate',
                                                     'types = restdns.clients.cli.commands.types:Types']},
      install_requires=['requests', 'PrettyTable'])
