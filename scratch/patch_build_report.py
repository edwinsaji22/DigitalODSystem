import re

with open("build_60page_report.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update section setup (page border, header, footer)
old_section_setup = """    # 1. Page Setup: 1.0 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(10)"""

new_section_setup = """    # 1. Page Setup: 1.0 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)
        section.different_first_page_header_footer = True

        # Page border on every page
        sectPr = section._sectPr
        pgBorders = parse_xml(
            '<w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'w:offsetFrom="page">'
            '<w:top w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
            '<w:left w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
            '<w:right w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
            '</w:pgBorders>'
        )
        sectPr.append(pgBorders)

        # Header: Top Left: Project Name, Top Right: 26MCAC22 (inside margins)
        header = section.header
        hp = header.paragraphs[0]
        hp.text = ""
        hpPr = hp._p.get_or_add_pPr()
        tabs_h = parse_xml(r'<w:tabs ' + nsdecls('w') + r'><w:tab w:val="right" w:pos="9360"/></w:tabs>')
        hpPr.append(tabs_h)
        hr1 = hp.add_run("Digital Leave and On-Duty (OD) Application System")
        hr1.font.name = "Times New Roman"
        hr1.font.size = Pt(9.5)
        hr1.font.italic = True
        hr1.font.color.rgb = RGBColor(60, 60, 60)

        hr_tab = hp.add_run("\\t")

        hr2 = hp.add_run("26MCAC22")
        hr2.font.name = "Times New Roman"
        hr2.font.size = Pt(10)
        hr2.font.bold = True
        hr2.font.color.rgb = RGBColor(60, 60, 60)

        # Footer: Bottom Left: Kristu Jayanti University, Bottom Right: Page X (inside margins)
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = ""
        fpPr = fp._p.get_or_add_pPr()
        tabs_f = parse_xml(r'<w:tabs ' + nsdecls('w') + r'><w:tab w:val="right" w:pos="9360"/></w:tabs>')
        fpPr.append(tabs_f)
        fr1 = fp.add_run("Kristu Jayanti University")
        fr1.font.name = "Times New Roman"
        fr1.font.size = Pt(9.5)
        fr1.font.italic = True
        fr1.font.color.rgb = RGBColor(60, 60, 60)

        fr_tab = fp.add_run("\\t")

        fr2 = fp.add_run("Page ")
        fr2.font.name = "Times New Roman"
        fr2.font.size = Pt(10)
        fr2.font.color.rgb = RGBColor(60, 60, 60)

        fldSimple = parse_xml(r'<w:fldSimple ' + nsdecls('w') + r' w:instr="PAGE"/>')
        fp._p.append(fldSimple)"""

assert old_section_setup in code, "old_section_setup not found"
code = code.replace(old_section_setup, new_section_setup)

# 2. Update typography, add_h1, add_h2, add_p, add_table_caption
old_funcs = """    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        return p"""

new_funcs = """    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_p(text):
        if not text or text.strip() == "":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            return p
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(0.4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_table_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p"""

assert old_funcs in code, "old_funcs not found"
code = code.replace(old_funcs, new_funcs)

# 3. Update cover page details
old_cover_sub = 'r_sub = p_sub.add_run("Submitted in partial fulfilment of the requirements for\\n“Practical Course Title” for the 1st Semester\\n\\n")'
new_cover_sub = 'r_sub = p_sub.add_run("Submitted in partial fulfilment of the requirements for\\n“Java and Web Programming Lab” for the 1st Semester\\n\\n")'
code = code.replace(old_cover_sub, new_cover_sub)

old_reg = 'r_reg = p_c2.add_run("26MCAC22")'
new_reg = 'r_reg = p_c2.add_run("26MCAC22 | I MCA C")'
code = code.replace(old_reg, new_reg)

old_guide = 'r_guide = p_guide.add_run("Under the guidance of\\n<Guide Name>")'
new_guide = 'r_guide = p_guide.add_run("Under the guidance of\\nDr. Nithya.B\\nDepartment of Computer Applications\\nAcademic Year 2026–2027")'
code = code.replace(old_guide, new_guide)

# 4. Add table captions before each table
old_table1 = 't_sp = doc.add_table(rows=len(specs_data), cols=3)'
new_table1 = 'add_table_caption("Table 1: Software Specifications")\n    t_sp = doc.add_table(rows=len(specs_data), cols=3)'
code = code.replace(old_table1, new_table1)

old_table2 = 't_fr = doc.add_table(rows=len(fr_data), cols=3)'
new_table2 = 'add_table_caption("Table 2: Functional Requirements Matrix")\n    t_fr = doc.add_table(rows=len(fr_data), cols=3)'
code = code.replace(old_table2, new_table2)

old_table3 = 't_u = doc.add_table(rows=len(u_cols), cols=3)'
new_table3 = 'add_table_caption("Table 3: Database Schema - Users Table")\n    t_u = doc.add_table(rows=len(u_cols), cols=3)'
code = code.replace(old_table3, new_table3)

old_table4 = 't_od = doc.add_table(rows=len(od_cols), cols=3)'
new_table4 = 'add_table_caption("Table 4: Database Schema - OD Requests Table")\n    t_od = doc.add_table(rows=len(od_cols), cols=3)'
code = code.replace(old_table4, new_table4)

old_table5 = 't_tc = doc.add_table(rows=len(tc_data), cols=5)'
new_table5 = 'add_table_caption("Table 5: System Verification and Test Plan")\n    t_tc = doc.add_table(rows=len(tc_data), cols=5)'
code = code.replace(old_table5, new_table5)

old_table6 = 't_gl = doc.add_table(rows=len(gl_data), cols=2)'
new_table6 = 'add_table_caption("Table 6: Academic and Technical Glossary")\n    t_gl = doc.add_table(rows=len(gl_data), cols=2)'
code = code.replace(old_table6, new_table6)

# 5. Update TOC loop so it doesn't get first line indent
old_toc_loop = """    for item in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(item)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)"""

new_toc_loop = """    for item in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(item)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)"""
code = code.replace(old_toc_loop, new_toc_loop)

# 6. Save to all targets including PROJECT_BASED_PRACTICAL_REPORT_EDWIN_SAJI.docx
old_save = """    out_file = r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\Digital_OD_Practical_Report.docx"
    doc.save(out_file)
    print("SUCCESS: 60+ Page Report saved at", out_file)
    try:
        doc.save(r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\Project_Practical_Report.docx")
        print("SUCCESS: Also updated Project_Practical_Report.docx")
    except Exception as e:
        print("Note: Project_Practical_Report.docx was locked, saved cleanly to Digital_OD_Practical_Report.docx")"""

new_save = """    targets = [
        r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\Digital_OD_Practical_Report.docx",
        r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\Project_Practical_Report.docx",
        r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\PROJECT_BASED_PRACTICAL_REPORT_EDWIN_SAJI.docx"
    ]
    for target in targets:
        try:
            doc.save(target)
            print("SUCCESS: Report saved cleanly to", target)
        except Exception as e:
            print("Could not save to", target, ":", e)"""
code = code.replace(old_save, new_save)

with open("build_60page_report.py", "w", encoding="utf-8") as f:
    f.write(code)

print("build_60page_report.py updated successfully!")
