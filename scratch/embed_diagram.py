with open("build_60page_report.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """    add_h2("Overall Request Flow")
    add_p("User action -> Browser interface -> Java Servlet (doPost/doGet) -> Validation and Business Logic -> MySQL database via JDBC -> Response/Redirect -> Result displayed to user.")"""

replacement = """    add_h2("Overall Request Flow")
    add_p("User action -> Browser interface -> Java Servlet (doPost/doGet) -> Validation and Business Logic -> MySQL database via JDBC -> Response/Redirect -> Result displayed to user.")

    add_h2("6.2 Workflow Diagram")
    p_diag = doc.add_paragraph()
    p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag.paragraph_format.first_line_indent = Inches(0)
    p_diag.paragraph_format.space_before = Pt(10)
    p_diag.paragraph_format.space_after = Pt(10)
    r_diag = p_diag.add_run()
    r_diag.add_picture(r"c:\\Users\\ivins\\Desktop\\MCA\\DigitalODSystem\\workflow_diagram.png", width=Inches(5.5))"""

assert target in content, "Target not found in build_60page_report.py"
content = content.replace(target, replacement)

with open("build_60page_report.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated build_60page_report.py to embed workflow_diagram.png!")
