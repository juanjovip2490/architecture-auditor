from setuptools import setup, find_packages

setup(
    name="architecture-auditor",
    version="1.0.0",
    description="Auditor de Patrones de Arquitectura y Código Limpio",
    author="Juan José Sáez",
    author_email="juanjovip2490@gmail.com",
    url="https://github.com/juanjovip2490/architecture-auditor",
    packages=find_packages(),
    install_requires=[
        "pathlib",
        "argparse",
        "json",
    ],
    entry_points={
        'console_scripts': [
            'audit=auditor:main',
            'audit-runner=audit_runner:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7+",
    ],
    python_requires=">=3.7",
)