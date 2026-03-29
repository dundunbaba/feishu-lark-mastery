# 推送到 GitHub 操作指南

**仓库**: https://github.com/dundunbaba/feishu-lark-mastery

---

## 方式 1：使用 GitHub CLI（推荐）

### 安装 GitHub CLI

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 验证安装
gh --version
```

### 认证并推送

```bash
# 1. 登录 GitHub
gh auth login

# 2. 进入技能目录
cd /home/admin/.openclaw/workspace/skills/feishu-lark-mastery

# 3. 推送代码
gh repo deploy-key add ~/.ssh/id_ed25519.pub --title "OpenClaw Deploy Key" 2>/dev/null || true
git push -u origin main
```

---

## 方式 2：使用 Git + Personal Access Token

### 步骤 1：创建 Personal Access Token

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写说明：`OpenClaw Push Token`
4. 选择权限：✅ `repo`（完整仓库权限）
5. 点击 "Generate token"
6. **复制 Token**（只显示一次，保存好！）

### 步骤 2：推送代码

```bash
# 进入技能目录
cd /home/admin/.openclaw/workspace/skills/feishu-lark-mastery

# 推送代码（替换 YOUR_TOKEN 为你的 Token）
git push -u origin main
# 如果提示输入密码，粘贴你的 Token
```

或者使用带 Token 的 URL：

```bash
# 移除旧远程
git remote remove origin

# 添加带 Token 的远程（替换 YOUR_TOKEN）
git remote add origin https://YOUR_TOKEN@github.com/dundunbaba/feishu-lark-mastery.git

# 推送
git push -u origin main
```

---

## 方式 3：手动推送（最简单）

```bash
# 1. 进入技能目录
cd /home/admin/.openclaw/workspace/skills/feishu-lark-mastery

# 2. 推送代码
git push -u origin main

# 3. 当提示输入用户名时：
# Username for 'https://github.com': dundunbaba
# Password for 'https://dundunbaba@github.com': [粘贴你的 Personal Access Token]
```

---

## 验证推送成功

推送完成后，打开仓库查看：
https://github.com/dundunbaba/feishu-lark-mastery

应该看到：
- ✅ 所有文件已上传
- ✅ 最新提交：`feat: v2.0.0 初始发布`
- ✅ 分支：main

---

## 安装命令（推送成功后）

```bash
# 方式 1: OpenClaw Skills
npx skills add https://github.com/dundunbaba/feishu-lark-mastery

# 方式 2: 手动安装
git clone https://github.com/dundunbaba/feishu-lark-mastery.git
cp -r feishu-lark-mastery ~/.openclaw/workspace/skills/
```

---

**推送成功后，请告诉我！** 🫡
