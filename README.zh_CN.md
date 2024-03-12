# Edge Copilot 补丁

Language: [English](README.md)

---

此脚本通过修改配置文件，解决新版Edge浏览器由于在不支持相关服务的地区（例如：中国大陆和俄罗斯）使用而导致的右上角Copilot图标消失的问题。

## 运行环境

- Python3

- 支持的操作系统: Windows10+, macOS and Linux

- Edge版本: >=119

## 注意

运行此脚本将会强制关闭Edge浏览器！

## 使用方法

1. 下载此项目然后进入项目文件夹

2. 下载必要的Python包

```shell
pip3 install -r requirements.txt
```

3. 运行脚本

```shell
python patch_edge_copilot.py
```

4. 重启Edge浏览器Copilot图标就出现了

## 参考

[解决新版Edge浏览器右上角不显示Copilot图标的问题](https://zhuanlan.zhihu.com/p/673914163)