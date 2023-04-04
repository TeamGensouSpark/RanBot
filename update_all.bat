@echo off
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
python -m pip install --upgrade -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install --upgrade -r ./src/resources/additional_plugins.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pause