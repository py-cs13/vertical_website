# VS Code SFTP配置指南

## 什么是SFTP？
SFTP（SSH File Transfer Protocol）是一种通过SSH安全传输文件的协议。它允许您在本地计算机和远程服务器之间安全地传输文件，同时支持远程文件的编辑和管理。

## 为什么使用SFTP？
1. **安全性**：通过SSH加密传输，确保数据安全
2. **便捷性**：直接在本地IDE中编辑远程文件
3. **实时同步**：保存文件时自动上传到服务器
4. **统一工作流**：无需切换工具即可完成本地和远程开发

## 配置步骤

### 1. 安装SFTP扩展
1. 在VS Code中打开扩展面板（快捷键：`Ctrl+Shift+X` 或 `Cmd+Shift+X`）
2. 搜索"SFTP"
3. 选择并安装由"Natizyskunk"开发的SFTP扩展

### 2. 创建SFTP配置文件

#### 2.1 自动创建配置文件
1. 安装扩展后，按`Ctrl+Shift+P`（或`Cmd+Shift+P`）打开命令面板
2. 输入"SFTP: Config"并选择
3. 扩展将自动在`.vscode`目录下创建`sftp.json`配置文件

#### 2.2 手动创建配置文件
如果自动创建失败，可以手动在项目的`.vscode`目录下创建`sftp.json`文件

### 3. 配置SFTP连接

#### 3.1 基本配置示例
```json
{
  "name": "Vertical Website Server",
  "host": "your-server-ip",
  "protocol": "sftp",
  "port": 22,
  "username": "your-username",
  "password": "your-password",
  "remotePath": "/home/user/vertical_website",
  "uploadOnSave": true,
  "syncMode": "update"
}
```

#### 3.2 使用SSH密钥认证（推荐）
```json
{
  "name": "Vertical Website Server",
  "host": "your-server-ip",
  "protocol": "sftp",
  "port": 22,
  "username": "your-username",
  "privateKeyPath": "/path/to/your/private-key",
  "passphrase": "your-passphrase-if-any",
  "remotePath": "/home/user/vertical_website",
  "uploadOnSave": true,
  "syncMode": "update"
}
```

#### 3.3 高级配置
```json
{
  "name": "Vertical Website Server",
  "host": "your-server-ip",
  "protocol": "sftp",
  "port": 22,
  "username": "your-username",
  "password": "your-password",
  "remotePath": "/home/user/vertical_website",
  "uploadOnSave": true,
  "syncMode": "update",
  "ignore": [
    "**/.vscode/**",
    "**/.git/**",
    "**/node_modules/**",
    "**/dist/**",
    "**/venv/**",
    "**/*.log"
  ],
  "watcher": {
    "files": "**/*",
    "autoUpload": true,
    "autoDelete": false
  }
}
```

## 配置参数说明

### 核心参数
- `name`: 连接名称（自定义）
- `host`: 服务器IP地址
- `protocol`: 协议类型，可选值：`sftp`或`ftp`
- `port`: 端口号（SFTP默认22，FTP默认21）
- `username`: 服务器用户名
- `password`: 服务器密码
- `privateKeyPath`: SSH私钥路径（如果使用密钥认证）
- `passphrase`: SSH私钥密码（如果私钥有密码）
- `remotePath`: 服务器上的项目目录路径

### 同步参数
- `uploadOnSave`: 保存文件时自动上传到服务器
- `syncMode`: 同步模式，可选值：`update`（只上传修改的文件）、`full`（全量同步）
- `ignore`: 忽略的文件和目录列表
- `watcher`: 文件监听配置，用于自动上传和删除文件

## 使用方法

### 连接服务器
1. 配置完成后，VS Code左侧活动栏会出现SFTP图标
2. 点击SFTP图标，展开"Vertical Website Server"连接
3. 右键点击连接名称，选择"Connect"即可连接服务器

### 文件操作
1. **浏览远程文件**：展开连接后可以浏览远程服务器上的文件和目录
2. **编辑远程文件**：双击远程文件即可在VS Code中打开编辑
3. **上传本地文件**：右键点击本地文件，选择"SFTP: Upload File"
4. **下载远程文件**：右键点击远程文件，选择"SFTP: Download File"
5. **同步文件夹**：右键点击文件夹，选择"SFTP: Sync Local -> Remote"或"SFTP: Sync Remote -> Local"

### 终端连接
1. 按`Ctrl+Shift+`（或`Cmd+Shift+`）打开终端
2. 输入`ssh username@server-ip`连接到远程服务器
3. 输入密码或使用SSH密钥认证
4. 成功连接后，您可以在终端中执行服务器命令

## 注意事项

### 1. 安全性
- **优先使用SSH密钥认证**：避免在配置文件中明文存储密码
- **保护私钥文件**：确保私钥文件权限设置为`600`（仅所有者可读可写）
- **定期更换密码和密钥**：增强账户安全性

### 2. 性能
- **合理配置忽略列表**：避免同步不必要的文件（如node_modules、venv等）
- **选择合适的同步模式**：根据项目大小选择update或full模式
- **避免频繁大文件操作**：大文件操作可能影响性能

### 3. 工作流
- **定期备份**：定期备份本地和远程项目文件
- **使用版本控制**：结合Git等版本控制工具管理代码
- **测试连接**：配置完成后先测试连接和文件传输

### 4. 常见问题

#### 4.1 连接失败
- 检查服务器IP、端口、用户名和密码是否正确
- 确保服务器SSH服务正常运行
- 检查防火墙设置是否允许SSH连接

#### 4.2 文件上传失败
- 检查服务器目录权限是否正确
- 确保远程路径存在
- 检查网络连接是否稳定

#### 4.3 同步冲突
- 避免多人同时编辑同一文件
- 使用版本控制工具解决冲突
- 定期同步本地和远程文件

## 示例配置文件

我们已经在`frontend/.vscode/sftp.json`目录下创建了一个示例配置文件，您可以根据自己的实际情况修改使用。

```json
{
  "name": "Vertical Website Server",
  "host": "your-server-ip",
  "protocol": "sftp",
  "port": 22,
  "username": "your-username",
  "password": "your-password",
  "remotePath": "/home/user/vertical_website",
  "uploadOnSave": true,
  "syncMode": "update",
  "ignore": [
    "**/.vscode/**",
    "**/.git/**",
    "**/node_modules/**",
    "**/dist/**",
    "**/venv/**",
    "**/*.log"
  ],
  "watcher": {
    "files": "**/*",
    "autoUpload": true,
    "autoDelete": false
  }
}
```

## 总结

通过SFTP配置，您可以在VS Code中轻松连接到远程服务器，直接编辑和管理远程文件，实现本地和远程开发环境的无缝集成。请根据您的实际服务器信息修改配置文件，并确保遵循安全最佳实践。

如果您在配置过程中遇到任何问题，可以随时查看该文档或联系我获取帮助。