# Project: 字幕编译工作台

## Skills

### subtitle-to-wechat
将英文视频/播客字幕翻译整理为微信公众号中文长文。

触发条件：用户上传英文字幕文件（.srt、.txt、.vtt）或要求翻译/整理/编译字幕为中文文章时。

详细工作流见 `.claude/skills/subtitle-to-wechat.md`。

## 项目结构

```
.claude/skills/          # Claude Code 技能定义
  subtitle-to-wechat.md  # 字幕编译技能

scripts/subtitle_to_wechat/  # 辅助脚本
  generate_docx.py           # 生成 Word 文档
  feishu_notify.py           # 推送飞书通知
```

## 依赖

- Python 3.11+
- python-docx（Word 文档生成）
- matplotlib（图表生成）
