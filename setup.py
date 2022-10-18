from setuptools import setup, find_packages
import io

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kafka-consumer-sns-sqs",
    version="0.0.1",
    author="Expedia Group",
    author_email="notificationhub@expediagroup.com",
    description="AWS SNS/SQS Kafka Consumer",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ExpediaGroup/kafka-consumer-sns-sqs",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "appdirs==1.4.4",
        "astroid==2.4.2; python_version >= '3.5'",
        "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "black==19.10b0; python_version >= '3.6'",
        "boto3==1.16.32",
        "botocore==1.19.32",
        "cached-property==1.5.2",
        "cerberus==1.3.2",
        "certifi==2020.12.5",
        "chardet==3.0.4",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "distlib==0.3.1",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "importlib-metadata==1.7.0",
        "iniconfig==1.1.1",
        "isort==5.6.4; python_version >= '3.6' and python_version < '4'",
        "jmespath==0.10.0; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "kafka==1.3.5",
        "kafka-python==2.0.2",
        "lazy-object-proxy==1.4.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "mccabe==0.6.1",
        "orderedmultidict==1.0.1",
        "packaging==20.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pathspec==0.8.1",
        "pep517==0.9.1",
        "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "pipenv-setup==3.1.1; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3' and python_version < '4'",
        "pipfile==0.0.2",
        "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pluggy==0.13.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "py==1.10.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pylint==2.6.0; python_version >= '3.5'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytest==6.1.2; python_version >= '3.5'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "regex==2020.11.13",
        "requests==2.25.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "requirementslib==1.5.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "s3transfer==0.3.3",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "typed-ast==1.4.1; python_version < '3.8' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython' and implementation_name == 'cpython'",
        "typing==3.7.4.3; python_version < '3.7'",
        "urllib3==1.26.2; python_version != '3.4'",
        "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "wheel==0.36.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "wrapt==1.12.1",
        "zipp==3.4.0; python_version < '3.8'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
