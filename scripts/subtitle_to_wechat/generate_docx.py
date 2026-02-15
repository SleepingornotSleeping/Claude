#!/usr/bin/env python3
"""
生成微信公众号风格的 Word 文档。

用法：
    python3 generate_docx.py content.json output.docx [chart1.png chart2.png ...]

content.json 格式见 .claude/skills/subtitle-to-wechat.md
"""

import json
import sys
import os

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml


# ── 颜色常量 ──────────────────────────────────────────────
BLUE_PRIMARY = RGBColor(0x2B, 0x57, 0x9A)   # 深蓝主色
GRAY_INTRO = RGBColor(0x66, 0x66, 0x66)     # 导读灰色
BLACK = RGBColor(0x00, 0x00, 0x00)           # 正文黑色
FONT_NAME = "Microsoft YaHei"


def set_run_font(run, name=FONT_NAME, size=None, bold=False, color=None):
    """设置 run 的字体属性（同时设置中西文字体）。"""
    run.font.name = name
    run.font.bold = bold
    # 设置中文字体
    r = run._element
    rPr = r.find(qn("w:rPr"))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        r.insert(0, rPr)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="{name}"/>')
        rPr.insert(0, rFonts)
    else:
        rFonts.set(qn("w:eastAsia"), name)

    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color


def set_paragraph_spacing(paragraph, before=0, after=200, line=360):
    """设置段落间距和行距。"""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after / 20)  # after 单位换算
    pf.line_spacing = Pt(line / 20)


def add_blue_separator(doc):
    """在文档中添加蓝色分隔线。"""
    p = doc.add_paragraph()
    pPr = p._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="1" w:color="2B579A"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    set_paragraph_spacing(p, before=100, after=100)
    return p


def build_document(content, output_path):
    """根据 content dict 生成 docx 文档。"""
    doc = Document()

    # ── 页面设置 ──────────────────────────────────────
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # ── 大标题 ────────────────────────────────────────
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_para.add_run(content["title"])
    set_run_font(run, size=18, bold=True, color=BLUE_PRIMARY)
    set_paragraph_spacing(title_para, before=0, after=300)

    # ── 导读 / 推荐语 ────────────────────────────────
    for text in content.get("intro_paragraphs", []):
        p = doc.add_paragraph()
        run = p.add_run(text)
        set_run_font(run, size=10, color=GRAY_INTRO)
        set_paragraph_spacing(p)

    add_blue_separator(doc)

    # ── 要点摘录 ──────────────────────────────────────
    if content.get("key_points"):
        kp_title = doc.add_paragraph()
        run = kp_title.add_run("要点摘录")
        set_run_font(run, size=14, bold=True, color=BLUE_PRIMARY)
        set_paragraph_spacing(kp_title, after=100)

        for i, point in enumerate(content["key_points"], 1):
            p = doc.add_paragraph()
            run = p.add_run(f"{i}. {point}")
            set_run_font(run, size=11, color=BLACK)
            set_paragraph_spacing(p, after=80)

        add_blue_separator(doc)

    # ── 正文章节 ──────────────────────────────────────
    for sec_idx, section_data in enumerate(content.get("sections", [])):
        # 章节标题
        h2 = doc.add_paragraph()
        run = h2.add_run(section_data["title"])
        set_run_font(run, size=14, bold=True, color=BLUE_PRIMARY)
        set_paragraph_spacing(h2, before=200, after=150)

        # 章节段落
        for para_data in section_data.get("paragraphs", []):
            p_type = para_data.get("type", "normal")
            text = para_data.get("text", "")

            p = doc.add_paragraph()
            set_paragraph_spacing(p)

            if p_type == "speaker":
                # 说话人姓名加粗蓝色
                speaker = para_data.get("speaker", "")
                speaker_run = p.add_run(f"{speaker}\uff1a")
                set_run_font(speaker_run, size=11, bold=True, color=BLUE_PRIMARY)
                text_run = p.add_run(text)
                set_run_font(text_run, size=11, color=BLACK)

            elif p_type == "highlight_strong":
                run = p.add_run(text)
                set_run_font(run, size=11, bold=True, color=BLUE_PRIMARY)

            elif p_type == "highlight_light":
                run = p.add_run(text)
                set_run_font(run, size=11, bold=False, color=BLUE_PRIMARY)

            else:  # normal
                run = p.add_run(text)
                set_run_font(run, size=11, color=BLACK)

        # 章节分隔线（最后一个章节不加）
        if sec_idx < len(content.get("sections", [])) - 1:
            add_blue_separator(doc)

    # ── 嵌入图表 ──────────────────────────────────────
    for chart in content.get("charts", []):
        chart_path = chart.get("path", "")
        caption = chart.get("caption", "")
        if os.path.exists(chart_path):
            add_blue_separator(doc)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run()
            run.add_picture(chart_path, width=Inches(5.5))
            set_paragraph_spacing(p, after=50)

            if caption:
                cap_p = doc.add_paragraph()
                cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = cap_p.add_run(caption)
                set_run_font(run, size=9, color=GRAY_INTRO)
                set_paragraph_spacing(cap_p, after=200)

    # ── 保存 ──────────────────────────────────────────
    doc.save(output_path)
    print(f"[OK] 文档已生成: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("用法: python3 generate_docx.py content.json output.docx")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    build_document(content, output_path)


if __name__ == "__main__":
    main()
