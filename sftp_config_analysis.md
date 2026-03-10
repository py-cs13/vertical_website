# SFTP配置文件分析与修复

## 问题分析

当前SFTP配置文件（`.vscode/sftp.json`）的问题在于**ignore和include规则的优先级**配置不当：

```json
{
  "ignore": [
    "**/*"  // 先忽略所有文件
  ],
  "include": [
    "docker-compose.yml"  // 然后只包含docker-compose.yml
  ]
}
```

这种配置方式在VSCode SFTP扩展中可能无法正常工作，因为：

1. 许多SFTP扩展先应用`ignore`规则，然后再应用`include`规则
2. 当`ignore`设置为`**/*`（忽略所有）时，`include`规则可能无法覆盖这个全局忽略
3. 正确的配置应该是先定义需要包含的文件，然后再排除不需要的文件

## 修复方案

### 方案1：修改ignore和include规则的顺序与内容

```json
{
  "name": "Vertical Website Server",
  "host": "101.43.177.216",
  "protocol": "sftp",
  "port": 22,
  "username": "ubuntu",
  "privateKeyPath": "/Users/shucui/ssh-key/tencent_ai.pem",
  "remotePath": "/home/ubuntu/docker/vertical_website_service/",
  "uploadOnSave": true,
  "syncMode": "update",
  "include": [
    "docker-compose.yml"
  ],
  "ignore": [
    "node_modules/",
    ".git/",
    ".vscode/",
    "*.log",
    "*.pyc",
    "__pycache__/"
  ]
}
```

### 方案2：使用更精确的ignore规则（不使用**/*）

```json
{
  "name": "Vertical Website Server",
  "host": "101.43.177.216",
  "protocol": "sftp",
  "port": 22,
  "username": "ubuntu",
  "privateKeyPath": "/Users/shucui/ssh-key/tencent_ai.pem",
  "remotePath": "/home/ubuntu/docker/vertical_website_service/",
  "uploadOnSave": true,
  "syncMode": "update",
  "ignore": [
    "node_modules/",
    ".git/",
    ".vscode/",
    "*.log",
    "*.pyc",
    "__pycache__/",
    "!docker-compose.yml"  // 排除除docker-compose.yml之外的所有文件
  ]
}
```

## 验证SFTP连接

1. **检查VSCode SFTP扩展是否正常工作**：
   - 打开VSCode的"活动栏"（左侧）
   - 点击"SFTP Explorer"图标
   - 检查是否显示远程服务器上的文件

2. **手动触发同步**：
   - 在VSCode中右键点击`docker-compose.yml`文件
   - 选择"SFTP: Upload File"选项

3. **检查远程服务器**：
   ```bash
   ssh ubuntu@101.43.177.216 -i /Users/shucui/ssh-key/tencent_ai.pem
   ls -la /home/ubuntu/docker/vertical_website_service/
   ```

## 可能的其他问题

1. **远程目录权限**：确保服务器上的目标目录存在且有正确的权限：
   ```bash
   ssh ubuntu@101.43.177.216 -i /Users/shucui/ssh-key/tencent_ai.pem
   mkdir -p /home/ubuntu/docker/vertical_website_service/
   chmod 755 /home/ubuntu/docker/vertical_website_service/
   ```

2. **VSCode SFTP扩展版本**：确保SFTP扩展是最新版本，旧版本可能有规则解析问题

3. **文件路径大小写**：确保文件名大小写一致（`docker-compose.yml`不是`Docker-compose.yml`）