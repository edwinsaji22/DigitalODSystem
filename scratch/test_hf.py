import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(1.0)
sec.bottom_margin = Inches(1.0)
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)

# header with tabs
header = sec.header
p = header.paragraphs[0]
pPr = p._p.get_or_add_pPr()
tabs = parse_xml(r'<w:tabs ' + nsdecls('w') + r'><w:tab w:val="right" w:pos="9360"/></w:tabs>')
pPr.append(tabs)
r1 = p.add_run("Digital Leave and On-Duty (OD) Application System")
r1.font.name = "Times New Roman"
r1.font.size = Pt(10)
r2 = p.add_run("\t")
r3 = p.add_run("26MCAC22")
r3.font.name = "Times New Roman"
r3.font.size = Pt(10)
r3.font.bold = True

footer = sec.footer
pf = footer.paragraphs[0]
pfPr = pf._p.get_or_add_pPr()
tabs_f = parse_xml(r'<w:tabs ' + nsdecls('w') + r'><w:tab w:val="right" w:pos="9360"/></w:tabs>')
pfPr.append(tabs_f)
rf1 = pf.add_run("Kristu Jayanti University")
rf1.font.name = "Times New Roman"
rf1.font.size = Pt(10)
rf1.font.italic = True
rf2 = pf.add_run("\t")
rf3 = pf.add_run("Page ")
rf3.font.name = "Times New Roman"
rf3.font.size = Pt(10)
fld = parse_xml(r'<w:fldSimple ' + nsdecls('w') + r' w:instr="PAGE"/>')
pf._p.append(fld)

doc.add_paragraph("Test body paragraph")
doc.save("test_hf.docx")
print("Saved test_hf.docx successfully")
