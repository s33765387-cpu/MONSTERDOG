from setuptools import setup, find_packages

setup(
    name="monsterdog_framework",
    version="11.987.0",
    description="Framework IA Quantique & Agentique - Architecture vΩ",
    author="Samuel Cloutier (ZORG-MASTER)",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "psutil>=5.9.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "websockets>=12.0"
    ],
    entry_points={
        "console_scripts": [
            "monsterdog=main:main",
        ],
    },
    python_requires=">=3.8",
)
