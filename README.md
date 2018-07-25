# panzerserver

Raspberry Pi上で動作する戦車の制御プログラムです。コントロールはAndroidのアプリから行います→[PanzerDroid](https://github.com/misakahi/PanzerDroid)

# Install

Python3用のpipをインストールします。

```
# raspbianの場合
sudo apt-get install python3-pip
```

[RPi.GPIO](https://pypi.org/project/RPi.GPIO/)をインストールします。

```
sudo pip3 install RPi.GPIO
```

リポジトリをクローンし、インストールします。

```
git clone https://github.com/misakahi/panzerserver
sudo pip3 -e install panzerserver
```

# Usage

`main.py`を管理者権限で実行します。

```
sudo python3 -m panzerserver.main
```

オプションは`--help`で確認できます。

```
python -m panzerserver.main --help             

usage: main.py [-h] [--port PORT] [--config CONFIG]

Panzer Vor!!

optional arguments:
  -h, --help       show this help message and exit
  --port PORT      port number (default: 50051)
  --config CONFIG  config file (optional)
```