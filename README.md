# 🚀 Feishu-Lark Mastery

> **飞书/Lark 全能力操作技能** - 让 OpenClaw 更智能地调用飞书套件

[![Version](https://img.shields.io/badge/version-v2.0.0-blue)](https://github.com/dundunbaba/feishu-lark-mastery/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Feishu](https://img.shields.io/badge/Feishu-Suite-red)](https://open.feishu.cn/)
[![Lark](https://img.shields.io/badge/Lark-Suite-blue)](https://developers.larksuite.com/)

---

## ✨ 功能特性

### 🎯 核心功能
- **知识库引导** - 调用前自动查阅飞书官方文档
- **渐进披露学习** - L1-L4 层层深入，80% 问题在 L2 解决
- **成熟度检查** - 调用前评估，低成熟度强制学习
- **4 场景诊断** - 未学习/权限/技巧/无解，快速定位问题
- **调用后报告** - 效率提升计算、尝试统计、改善点总结
- **经验库建设** - 本地经验记录，持续迭代优化

### 🌍 区域支持
- **中国大陆** - 飞书 Suite（open.feishu.cn）
- **国际市场** - Lark Suite（developers.larksuite.com）

---

## 🚀 快速开始

### 安装

```bash
# 方式 1: 使用 OpenClaw Skills
npx skills add https://github.com/dundunbaba/feishu-lark-mastery

# 方式 2: 手动安装
git clone https://github.com/dundunbaba/feishu-lark-mastery.git
cp -r feishu-lark-mastery ~/.openclaw/workspace/skills/
```

### 使用

**自动生效** - 安装后自动加载，调用飞书工具前自动查阅知识库

**手动查阅**：
```bash
# 查看速查表
cat skills/feishu-lark-mastery/messaging/CHEATSHEET.md

# 查看成熟度评估
python3 skills/feishu-lark-mastery/scripts/calculate-maturity.py --all
```

---

## 📊 核心指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 调用前查阅率 | 100% | 每次调用前必须查阅 |
| L2 解决率 | 80% | 速查表解决 80% 问题 |
| 效率提升 | >50% | 平均节省 50% 调试时间 |
| 诊断准确率 | 90% | 4 场景诊断准确率 |

---

## 📁 目录结构

```
feishu-lark-mastery/
├── SKILL.md                 # 技能说明
├── README.md                # 本文件
├── references/
│   └── PRD.md               # 产品需求文档
├── common/                  # 通用知识
├── bitable/                 # 多维表格
├── doc/                     # 云文档
├── messaging/               # 消息与群组
├── wiki/                    # 知识库
├── drive/                   # 云空间
├── calendar/                # 日历
├── experience-db/           # 本地经验库
└── scripts/                 # 辅助脚本
```

---

## 🎯 4 场景诊断

| 场景 | 症状 | 处理 |
|------|------|------|
| **A: 未学习** | 找不到文档、参数错误 | 引导到官方文档 |
| **B: 权限问题** | 403 错误、权限不足 | 提供申请链接 |
| **C: 技巧问题** | 需求不清、调用失败 | 引导澄清需求 |
| **D: 无解** | 飞书 API 不支持 | 推荐替代方案 |

---

## 📈 调用后报告

每次调用后自动生成报告，包含：
- **效率提升计算** - 使用前 vs 使用后对比
- **尝试统计** - 尝试次数、成功次数
- **场景诊断** - 4 场景详细分析
- **改善点** - 已改善/待改善项

---

## 🙏 鸣谢

### 官方资源

本技能引用了以下官方文档和资源：

- **飞书开放平台** - https://open.feishu.cn/
- **Lark Developer** - https://developers.larksuite.com/
- **飞书 API 文档** - 所有官方 API 文档
- **飞书帮助中心** - 使用指南和最佳实践

### 社区贡献

感谢以下开源项目和社区的贡献：

- **OpenClaw** - https://github.com/openclaw/openclaw
  - 提供了技能开发框架和工具支持
  - OpenClaw 文档：https://docs.openclaw.ai
  - 技能规范参考：OpenClaw Skills Specification

- **飞书开放平台社区** - 问题解答和经验分享

### 经验知识

本技能中的经验知识（`experience/` 目录）来自：
- 实际项目中的踩坑总结
- 社区用户的问题反馈
- 持续迭代的优化建议

**贡献经验**：欢迎通过 Issue 或 PR 分享您的使用经验！

---

## 🤝 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 贡献方式
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献内容
- 📚 官方文档同步更新
- 💡 经验知识分享
- 🐛 Bug 修复
- ✨ 新功能建议

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 👤 作者

**田野 (Tian Ye)** (@dundunbaba)

---

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn/)
- [Lark Developer](https://developers.larksuite.com/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
- [GitHub 仓库](https://github.com/dundunbaba/feishu-lark-mastery)

---

**🌟 如果这个项目对你有帮助，请给一个 Star！**
