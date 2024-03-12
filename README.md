# Edge Copilot Patch

Language: [中文](README.zh_CN.md)

---

This script patches the configuration file to solve the problem of disappearance of the Copilot icon in the upper right cornor of Edge Browser, due to its use in regions of which relevant services are unsupported (e.g. China Mainland and Russia).

## Environment

- Python3

- Supported OS: Windows10+, macOS and Linux

- Edge version: >=120

## Note

Running this script will force your Edge browser to shut down!

## Usage

1. Download this project then enter into the project directory

2. Download necessary python package

```shell
pip3 install -r requirements.txt
```

3. Run the script

```shell
python patch_edge_copilot.py
```

4. Restart the Edge and you will see the Copilot icon

## References

[解决新版Edge浏览器右上角不显示Copilot图标的问题]