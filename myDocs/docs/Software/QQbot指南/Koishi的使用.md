# Koishi的使用

## 数据备份

### 1panel一键备份方法😎

> 前提：使用1Panel应用商店部署koishi

在应用商店的已安装应用列表点击备份即可。

恢复时导入备份文件即可。

### Linux-Docker部署的koishi备份方法🙌

无特殊步骤，与正常Docker备份一致
> **Docker 数据存储方式**
> Docker 数据通常通过以下两种方式持久化：

1. **数据卷（Volumes）**
   - Docker 管理的存储路径（默认在 `/var/lib/docker/volumes/`）。

2. **绑定挂载（Bind Mounts）**
   - 直接映射宿主机的目录到容器中（如 `-v /host/path:/container/path`）。

| 操作       | 绑定挂载（Bind Mounts）              | Docker 卷（Volume）      |
| -------- | ------------------------------ | --------------------- |
| **备份**   | 直接操作宿主机目录                      | 通过临时容器操作卷             |
| **恢复**   | 直接解压到宿主机目录                     | 通过临时容器解压到卷            |
| **路径**   | 需明确宿主机路径（如 `/opt/koishi/data`） | 只需卷名（如 `koishi_data`） |
| **适用场景** | 开发调试、直接管理文件                    | 生产环境、数据隔离             |

#### 绑定挂载步骤

1. **查找koishi对应数据卷**

   ```bash
   # 查看容器挂载的卷信息
   docker inspect <容器名称> | grep -A 10 "Mounts"
   
   #预期输出
   "Mounts": [
               {
                   "Type": "bind", #此处显示bind,为绑定挂载，若显示volume,则为Docker管理的存储
                   "Source": "/opt/1panel/apps/koishi/koishi/data“,  #宿主机路径
                   "Destination": "/koishi",
                   "Mode": "rw",
                   "RW": true,
                   "Propagation": "rprivate"
               }
             ]
   ```

2. **备份绑定挂载的目录**
   若 `Type` 为 `bind`，直接备份 `Source` 路径：

   ```bash
   cd <存储备份路径，可以为/var/backups>
   # 示例：备份宿主机目录到当前目录
   tar czvf koishi_backup_$(date +%Y%m%d).tar.gz -C </opt/1panel/apps/koishi/koishi/data,这里填目标路径> .
   #命令含义解释: tar                                    Linux 的归档打包工具
   #           c：创建新的归档文件 z：使用gzip压缩 v：显示详细过程（verbose）f：指定归档文件名
   #           koishi_backup_$(date +%Y%m%d).tar.gz    备份文件名（含当前日期）
   #           -C <目标路径>                            切换到指定目录后再打包
   #           .                                        打包当前目录的所有内容
   ```

   备份的文件会放在当前目录，如果执行命令前未使用`cd`命令，则默认在`/root`路径。

3. **检查备份**

   ```bash
   tar -ztvf <备份文件名>
   ```

4. **恢复备份**

   ```bash
   # 停止容器
   docker stop koishi
   # 解压备份（覆盖原有数据）
   tar xzvf /backups/koishi_backup_20240328.tar.gz \
     -C </opt/1panel/apps/koishi/koishi/data,宿主机挂载路径>
   # 重启容器
   docker start koishi
   ```

#### 数据卷步骤

1. **备份**

   ```bash
   docker run --rm -v <卷名:/volume_data> -v $(pwd):/backup alpine \
     tar czvf </backup/volume_backup.tar.gz备份文件路径> -C /volume_data .
   ```

2. **恢复**

   ```bash
   docker run --rm -v <卷名:/volume_data> -v $(pwd):/backup alpine \
     tar xzvf </backup/volume_backup.tar.gz备份文件路径> -C /volume_data
   ```

### 使用systools插件的自动备份方法😋

#### Github云备份配置

> **GitHubToken获取**

- 点击右上角头像 → **Settings** → 左侧菜单栏 → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**。

- 设置Token基本信息
  
  - **Note**：填写 Token 用途（如 "CI/CD" 或 "API Access"）。
  - **Expiration**：设置有效期（建议选择短期或自定义日期，增强安全性）。
  - **Select scopes**：勾选所需权限（按需选择，遵循最小权限原则）。

- 常用权限说明
  
  | 权限名称             | 用途                    |
  | ---------------- | --------------------- |
  | `repo`           | 访问私有仓库和公有仓库的读写权限      |
  | `workflow`       | 允许操作 GitHub Actions   |
  | `admin:org`      | 管理组织设置（慎用）            |
  | `user`           | 访问用户数据（如邮箱）           |
  | `read:packages`  | 读取 GitHub Packages    |
  | `write:packages` | 上传/管理 GitHub Packages |

- 滚动到页面底部 → 点击 **Generate token** → **复制生成的 Token**（页面关闭后将无法再次查看！）。

> 填写插件配置

**_githubToken**：填写classic token。

**需要备份至 GitHub 的文件**：koishi数据路径（获取方法详见上文），**注意**这里是文件路径，不支持文件夹整体保存。（貌似有点麻烦）

## 插件配置

### 过滤器的使用

过滤器是Koishi中用于处理消息的强大工具。它们可以根据特定条件过滤掉不需要的消息或执行特定操作。

在插件配置处，点击“添加条件”按钮，可以选择不同的过滤器类型，如“用户ID”、“群组ID”等。

选择群组ID后，可以输入具体的群组ID，设置`不等于`，则该群组的对应插件指令将不会被执行。
在该群组的help输出中，指令将不会显示。

其他过滤器类型的使用方法类似，可以根据需要进行配置。

选择添加“与”条件后，可以添加多个过滤器条件，只有当所有条件都满足时，插件指令才会被执行。

如果需要添加“或”条件，可以在现有条件下点击“添加或条件”，然后选择新的过滤器类型。

如果需要删除某个条件，可以点击该条件右侧的删除按钮。
