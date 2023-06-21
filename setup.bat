@echo off
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip install pdm -i https://pypi.tuna.tsinghua.edu.cn/simple
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
pdm install
pdm run python -m ensurepip
pdm run python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pdm run pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
./run.bat