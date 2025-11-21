from setuptools import setup, find_packages

setup(
    name="monsterdog_framework",
    version="11.987.0",
    description="Framework IA Quantique & Agentique - Architecture vΩ",
    author="Samuel Cloutier (ZORG-MASTER)",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "psutil",
        "pandas",
        "numpy",
        "pydantic",
        "websockets"
    ],
    entry_points={
        "console_scripts": [
            "monsterdog=main:main",
        ],
    },
    python_requires=">=3.8",
)
