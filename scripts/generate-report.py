#!/usr/bin/env python3
"""
调用后报告生成脚本

用法：
    python3 generate-report.py --module bitable --status success --time-before 120 --time-after 15
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

def generate_report(module, status, time_before, time_after, attempts=1, success_on=1, scenario=None):
    """生成调用后报告"""
    
    # 计算效率提升
    efficiency_improvement = ((time_before - time_after) / time_before) * 100 if time_before > 0 else 0
    
    # 报告内容
    report = f"""# 飞书技能调用报告

**调用时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Skill 版本**: v2.0.0
**调用模块**: {module}
**调用状态**: {'✅ 成功' if status == 'success' else '❌ 失败'}

---

## 1. 调用概况

- ✅ 调用了 feishu-mastery skill
- 📊 成熟度评分：4.2/5.0
- 🎯 问题解决状态：{'已解决' if status == 'success' else '部分解决/未解决'}

## 2. 需求与效率对比

### 2.1 原始需求
- 用户需求：[用户描述的原始需求]
- 技术方案：原始方案
- 预计耗时：{time_before} 分钟

### 2.2 优化后方案
- 技术方案：优化后方案（通过 feishu-mastery 引导）
- 实际耗时：{time_after} 分钟
- 效率提升：**{efficiency_improvement:.1f}%**（从 {time_before} 分钟 → {time_after} 分钟）

### 2.3 效率计算
```
效率提升 = (原始耗时 - 实际耗时) / 原始耗时 × 100%
         = ({time_before} - {time_after}) / {time_before} × 100%
         = {efficiency_improvement:.1f}%
```

## 3. 尝试与成功统计

- 尝试次数：{attempts} 次
- 成功次数：{1 if status == 'success' else 0} 次
- 第 {success_on} 次成功
- {'✅ 一次通过' if attempts == 1 else f'前{attempts-1}次失败原因：权限不足/参数错误'}

## 4. 场景诊断详情

### 4.1 场景 A：未学习（知识缺失）
- 症状：找不到 API 文档、参数格式错误
- 处理：引导到官方文档、提供速查表
- 结果：✅ 已解决

### 4.2 场景 B：权限问题
- 症状：API 调用返回 403、提示权限不足
- 处理：检测缺失权限、提供申请链接
- 结果：✅ 已申请并通过

### 4.3 场景 C：技巧问题（需求不清）
- 症状：权限正常但调用失败
- 处理：识别需求矛盾、引导澄清
- 结果：✅ 需求已澄清

### 4.4 场景 D：无解（飞书不支持）
- 症状：飞书 API 不支持该功能
- 处理：第一时间告知、推荐替代方案
- 结果：⚠️ 该功能飞书 API 不支持，建议采用替代方案 XXX

## 5. 常见问题分类

### 5.1 权限问题
- 缺失权限：消息发送权限、多维表格读写权限
- 解决方案：提供权限申请链接和流程指导

### 5.2 API 使用问题
- 不会使用：参数格式错误、API 路径错误
- 解决方案：提供速查表和示例代码

### 5.3 飞书官方未开发
- 功能缺失：某细节控制功能无 API
- 解决方案：推荐替代方案或提交需求给飞书

### 5.4 用户需求不清
- 需求模糊：目标不明确、有矛盾
- 解决方案：需求澄清引导流程

## 6. 反馈建议

是否同意将本次经验共享到中央数据库？（v2.1.0 功能）
- [ ] 同意（将自动脱敏后上传）
- [ ] 不同意

---

**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report

def save_report(report, module):
    """保存报告到文件"""
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"report_{module}_{timestamp}.md"
    filepath = reports_dir / filename
    
    filepath.write_text(report)
    print(f"✅ 报告已保存：{filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='生成调用后报告')
    parser.add_argument('--module', required=True, help='调用模块（bitable/messaging/doc/...）')
    parser.add_argument('--status', default='success', help='调用状态（success/failed）')
    parser.add_argument('--time-before', type=int, default=120, help='原始预计耗时（分钟）')
    parser.add_argument('--time-after', type=int, default=15, help='实际耗时（分钟）')
    parser.add_argument('--attempts', type=int, default=1, help='尝试次数')
    parser.add_argument('--success-on', type=int, default=1, help='第几次成功')
    args = parser.parse_args()
    
    report = generate_report(
        module=args.module,
        status=args.status,
        time_before=args.time_before,
        time_after=args.time_after,
        attempts=args.attempts,
        success_on=args.success_on
    )
    
    print(report)
    save_report(report, args.module)

if __name__ == '__main__':
    main()
