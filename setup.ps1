python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip install pdm -i https://pypi.tuna.tsinghua.edu.cn/simple
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
pdm install
Powershell -NoExit script/setup-nb.ps1