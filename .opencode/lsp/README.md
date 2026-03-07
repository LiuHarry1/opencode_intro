# Custom Python LSP

本目录包含自定义的 Python Language Server，可在 **OpenCode**、**Cursor** 和 **VS Code** 中使用。

## 功能

- **Diagnostics** — TODO/FIXME 标注、超长行、`import *`、裸 except、print 调试
- **Completion** — Python 代码片段（def、class、for、try 等）及内置函数
- **Hover** — 内置函数与关键字的文档提示
- **Formatting** — 空白行清理

## 使用方法

### 1. OpenCode（Web / 本地）

**方式一：本地 stdio**（OpenCode 启动进程）

```json
"lsp": {
  "custom-python-lsp": {
    "command": ["python", ".opencode/lsp/custom_lsp_server.py"],
    "extensions": [".py"]
  }
}
```

**方式二：远程 TCP**（LSP 在另一台机器或已手动启动）

先用 bridge 连接远程 server：

```json
"lsp": {
  "custom-python-lsp": {
    "command": ["python", ".opencode/lsp/lsp_tcp_bridge.py", "远程IP", "6008"],
    "extensions": [".py"]
  }
}
```

或通过环境变量（适合 Docker 等）：

```json
"lsp": {
  "custom-python-lsp": {
    "command": ["python", ".opencode/lsp/lsp_tcp_bridge.py"],
    "extensions": [".py"],
    "env": {
      "LSP_TCP_HOST": "192.168.1.100",
      "LSP_TCP_PORT": "6008"
    }
  }
}
```

远程 server 需先启动：`python custom_lsp_server.py --tcp 6008 --host 0.0.0.0`

### 2. Cursor / VS Code

#### 推荐：TCP 模式（手动启动 server，远程连接）

扩展默认使用 TCP 模式，可避免 stdio 模式下的启动问题，且日志一定可见。

1. **先启动 LSP server**（在项目根目录执行）：
   ```bash
   python .opencode/lsp/custom_lsp_server.py --tcp
   ```
   默认监听 `127.0.0.1:6008`，日志会写入 `.opencode/lsp/lsp.log` 和终端。

2. **再打开 Cursor / VS Code**，打开本项目，编辑 Python 文件，扩展会自动连接已启动的 server。

3. **可选配置** `.vscode/settings.json`：
   ```json
   {
     "customPythonLsp.connectionMode": "tcp",
     "customPythonLsp.tcpHost": "127.0.0.1",
     "customPythonLsp.tcpPort": 6008
   }
   ```

4. **远程连接**（server 在另一台机器）：
   - server 端：`python custom_lsp_server.py --tcp 6008 --host 0.0.0.0`
   - 编辑器：`"customPythonLsp.tcpHost": "服务器IP"`

#### 方式 A：扩展开发模式（开发 / 测试）

1. 用 Cursor 或 VS Code 打开本项目
2. 按 **F5** 或选择 Run → Start Debugging
3. 会打开新窗口（Extension Development Host），并已加载本扩展
4. 在新窗口中打开任意含 `.opencode/lsp/` 的 Python 项目即可使用

#### 方式 B：安装扩展（长期使用）

1. 打包扩展：
   ```bash
   cd custom-python-lsp-extension
   npx @vscode/vsce package --no-dependencies
   ```

2. 安装 `.vsix`：
   - **Cursor**：`cursor --install-extension custom-python-lsp-0.1.0.vsix`
   - **VS Code**：`code --install-extension custom-python-lsp-0.1.0.vsix`
   - 或在编辑器内：Extensions → ⋯ → Install from VSIX

3. 重启 Cursor / VS Code

4. 打开包含 `.opencode/lsp/custom_lsp_server.py` 的项目，编辑 `.py` 文件即可使用

### 3. 配置（Cursor / VS Code）

在 `.vscode/settings.json` 中可配置：

```json
{
  "customPythonLsp.connectionMode": "tcp",
  "customPythonLsp.tcpHost": "127.0.0.1",
  "customPythonLsp.tcpPort": 6008,
  "customPythonLsp.pythonPath": "python",
  "customPythonLsp.serverPath": ".opencode/lsp/custom_lsp_server.py"
}
```

| 配置项 | 默认 | 说明 |
|--------|------|------|
| connectionMode | tcp | `tcp`=连接已启动的 server，`stdio`=扩展启动进程 |
| tcpHost | 127.0.0.1 | TCP 模式下 server 地址 |
| tcpPort | 6008 | TCP 模式下 server 端口 |

## 依赖

- Python 3.8+
- `pip install pygls lsprotocol`
