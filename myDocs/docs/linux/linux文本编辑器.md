# linux文本编辑器

## vim

vim文本编辑器，比较古老，不好用

### vim模式

- (normal mode)正常模式: 浏览或从宏观上处理文本的模式，要进入编辑模式：按`i`，要退出vim，要先退出到命令行模式（`:`）
- 编辑模式：逐字添加或修改文本时进入的模式，编辑完要先退出到正常模式（按`esc`）
- 命令行模式：输入命令：保存、退出、搜索等的模式

### vim常用命令

```bash
vim 文件名 # 打开文件, 进入正常模式
i # 进入编辑模式
esc # 进入正常模式
: # 进入命令行模式
:q # 仅退出
:q! # 退出不保存
:wq # 保存并退出
```

```bash
h # 向左移动光标
j # 向下移动光标
k # 向上移动光标，k大j小
l # 向右移动光标
w # 移动到下一个单词的开头
e # 移动到下一个单词的结尾
b # 移动到上一个单词的开头
G # 移动到文件末尾
gg # 移动到文件开头

i # 在光标前插入, insert
I # 在行首插入
a # 在光标后插入，append
A # 在行尾插入
o # 在下一行插入新行
O # 在上一行插入新行
```

修改vim配置文件：

`vim --version` 查看vim版本，可以找到配置文件：
`user vimrc file: "$HOME/.vimrc"`

使用vim打开配置文件:
```bash
vim ~/.vimrc
set number # 显示行号
set relativenumber # 显示相对行号
```

使用行号快速定位：
```bash
4k # 向上移动4行
5j # 向下移动5行
```

复制与粘贴：
```bash
yy # 复制当前行，yank
yw # 复制当前单词, yank a word
p # 粘贴到下一行, put
3p # 粘贴3次
P # 粘贴到上一行
dd # 剪切当前行
dw # 剪切当前单词, delete a word
cw # 修改当前单词, change a word,删除字符后自动进入编辑模式
. # 重复上一次命令
u # 撤销上一次命令, undo
ctrl + r # 恢复上一次命令, redo
```

搜索：
```bash
/ # 搜索
```

## nano

- [nano](https://www.nano-editor.org/)
- [何必死磕vim，nano速通攻略！](https://www.bilibili.com/video/BV1xMkMBMEft)

nano文本编辑器十分简单，按`ctrl + g`可获取帮助

当设置终端语言为中文时，nano界面也会是中文显示，帮助也是中文
```bash
export LANG=zh_CN.UTF-8
```

配置nano：

```bash
# 官方提供的默认配置文件位置：/etc/nanorc
cp /etc/nanorc ~/.config/nano
# 配置文件位置：~/.config/nano/nanorc
nano ~/.config/nano/nanorc
```