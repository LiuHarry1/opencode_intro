# OpenCode Server

## 构建 Docker 镜像

```bash
docker build -t opencode-server -f dockerfile .
```

## 运行容器

```bash
docker run -d \
  --name opencode-server1 \
  -p 4096:4096 \
  -v "C:\Users\Harry\.local\share\opencode\auth.json:/root/.local/share/opencode/auth.json:ro" \
  opencode-server
```

可选：设置密码环境变量

```bash
docker run -d \
  --name opencode-server1 \
  -p 4096:4096 \
  -e OPENCODE_SERVER_PASSWORD=your_password \
  -v "C:\Users\Harry\.local\share\opencode\auth.json:/root/.local/share/opencode/auth.json:ro" \
  opencode-server
```
