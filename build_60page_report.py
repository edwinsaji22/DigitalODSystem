import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_60page_report():
    doc = Document()

    # 1. Page Setup: 1.0 inch margins all around
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

        hr_tab = hp.add_run("\t")

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

        fr_tab = fp.add_run("\t")

        fr2 = fp.add_run("Page ")
        fr2.font.name = "Times New Roman"
        fr2.font.size = Pt(10)
        fr2.font.color.rgb = RGBColor(60, 60, 60)

        fldSimple = parse_xml(r'<w:fldSimple ' + nsdecls('w') + r' w:instr="PAGE"/>')
        fp._p.append(fldSimple)

    # 2. Typography: Times New Roman 12pt, 1.5 line spacing, 6pt space after
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    def add_h1(text):
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
        return p

    def add_bullet(title, body):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        r1 = p.add_run(title)
        r1.font.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r2 = p.add_run("\n" + body if "\n" in body else " " + body)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        return p

    def add_code(code_str):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.2)
        r = p.add_run(code_str.strip())
        r.font.name = 'Courier New'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0, 0, 0)

    def add_image_box(title, subtitle, height_in_inches=2.8):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m in ['top', 'bottom', 'left', 'right']:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), '180')
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)
        
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FAFAFA"/>')
        tcPr.append(shd)
        
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="dashed" w:sz="6" w:space="0" w:color="9CA3AF"/>\n'
            f'  <w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="9CA3AF"/>\n'
            f'  <w:left w:val="dashed" w:sz="6" w:space="0" w:color="9CA3AF"/>\n'
            f'  <w:right w:val="dashed" w:sz="6" w:space="0" w:color="9CA3AF"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(int(height_in_inches * 20))
        cp.paragraph_format.space_after = Pt(int(height_in_inches * 20))
        
        r1 = cp.add_run(f"[ INSERT SCREENSHOT: {title} ]\n")
        r1.font.name = 'Consolas'
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(30, 30, 30)
        
        r2 = cp.add_run(f"({subtitle})")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.font.italic = True
        r2.font.color.rgb = RGBColor(100, 100, 100)

    def format_table(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E5E7EB"/>')
            tcPr.append(shd)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(4)
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0, 0, 0)
        
        for row in table.rows[1:]:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(10.5)
                        run.font.color.rgb = RGBColor(0, 0, 0)
        
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

    # ====================================================
    # COVER PAGE (PAGE 1)
    # ====================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(30)
    p_inst.paragraph_format.space_after = Pt(2)
    r1 = p_inst.add_run("KRISTU JAYANTI\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(16, 44, 87)

    r2 = p_inst.add_run("(DEEMED TO BE UNIVERSITY)\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.font.color.rgb = RGBColor(16, 44, 87)

    r3 = p_inst.add_run("— Under Section 3 of UGC Act 1956 —\nA CMI INSTITUTION | BENGALURU | INDIA\n")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(10.5)
    r3.font.color.rgb = RGBColor(80, 80, 80)

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(50)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(8)
    r_rep = p_rep.add_run("Project-based Practical Report on\n")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(14)
    r_rep.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(40)
    r_tit = p_title.add_run("“Digital Leave and On-Duty (OD) Application System”")
    r_tit.font.name = 'Times New Roman'
    r_tit.font.size = Pt(16)
    r_tit.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("Submitted in partial fulfilment of the requirements for\n“Java and Web Programming Lab” for the 1st Semester\n\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)

    r_mca = p_sub.add_run("Master of Computer Applications (MCA)\n")
    r_mca.font.name = 'Times New Roman'
    r_mca.font.size = Pt(14)
    r_mca.font.bold = True

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(60)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(12)
    r_by = p_by.add_run("Submitted by\n")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(12)

    table_auth = doc.add_table(rows=1, cols=2)
    table_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = table_auth.cell(0, 0)
    c2 = table_auth.cell(0, 1)
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_c1.add_run("Edwin Saji")
    r_name.font.name = 'Times New Roman'
    r_name.font.size = Pt(13)
    r_name.font.bold = True

    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_reg = p_c2.add_run("26MCAC22 | I MCA C")
    r_reg.font.name = 'Times New Roman'
    r_reg.font.size = Pt(13)
    r_reg.font.bold = True

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(50)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_guide = p_guide.add_run("Under the guidance of\nDr. Nithya.B\nDepartment of Computer Applications\nAcademic Year 2026–2027")
    r_guide.font.name = 'Times New Roman'
    r_guide.font.size = Pt(12)

    doc.add_page_break()

    # ====================================================
    # CONTENTS (PAGE 2)
    # ====================================================
    add_h1("Contents")
    toc_items = [
        "1. Title of the Project",
        "2. Introduction",
        "3. Objective of the Project",
        "4. Scope of the Project",
        "5. Software Specifications",
        "6. Workflow of the Project",
        "7. Modules of the Project - Phase-wise explanation of design and execution of Modules",
        "8. Source Code (Only functional code structure)",
        "9. Features of the Project",
        "10. Requirements Analysis",
        "11. Use Case Descriptions",
        "12. System Architecture",
        "13. Database Design Overview",
        "14. Input Validation and Error Handling",
        "15. Testing",
        "16. Security Considerations and Known Limitations",
        "17. Installation and Execution Guide",
        "18. Application Screenshots",
        "19. Glossary",
        "20. References",
        "21. Future Enhancement",
        "22. Conclusion"
    ]
    for item in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(item)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

    doc.add_page_break()

    # ====================================================
    # CHAPTER 1 & 2: TITLE & INTRODUCTION
    # ====================================================
    add_h1("Title of the Project")
    add_p("Digital Leave and On-Duty (OD) Application System")
    add_p("A web-based academic automation system developed using Java Servlets, JSP, JDBC, and MySQL running on the Apache Tomcat 9 web server.")

    add_h1("Introduction")
    add_p("The Digital Leave and On-Duty (OD) Application System is an academic web application designed to automate and streamline the management of student on-duty clearances and collegiate leave workflows. In modern higher education institutions, undergraduate and postgraduate students are frequently called upon to represent their academic departments and the college in a wide variety of co-curricular and extra-curricular activities. These activities include inter-collegiate technical symposia, national-level hackathons, coding marathons, paper presentation contests, sports tournaments, cultural festivals, recruitment drives, and industrial internships. When students represent the institution at such sanctioned events, institutional bylaws permit them to claim 'On-Duty' (OD) status. This status officially excuses their absence from regular lectures and laboratory sessions, ensuring that their formal attendance percentage is maintained and protected from penalty.")

    add_p("However, in the overwhelming majority of colleges and universities, the administrative management of on-duty leave continues to rely on legacy paper-based procedures. In a conventional manual system, students must physically obtain a paper on-duty form from the departmental office, fill out their personal details, course code, and event descriptions by hand, attach physical proof such as brochures or invitations, and physically locate multiple faculty members across campus to collect physical ink signatures. A single application typically requires sequential endorsements from the event faculty coordinator, the student's designated class mentor, subject teachers, and ultimately the Head of the Department (HOD).")

    add_p("This paper-based mechanism introduces severe operational bottlenecks and administrative vulnerabilities. Physical forms are frequently misplaced on faculty desks, delayed during inter-departmental transit, or damaged, leaving students anxious about their attendance records. More importantly, manual workflows make it almost impossible to enforce institutional academic bylaws in a systematic, reliable manner. Colleges strictly enforce rules such as a non-negotiable 3-day post-event submission deadline and a semester quota cap of 15 duty days per student. In a manual paper workflow, faculty signatories cannot verify whether a student has already exceeded their semester quota without cross-referencing physical departmental logbooks, which is rarely done in real time.")

    add_p("Furthermore, handwritten paper forms are highly vulnerable to unauthorized alteration, forged signatures, and duplicate submissions. Late submissions submitted weeks after an event concludes often force institutional ERP operators to perform manual, retroactive database updates, leading to attendance disputes during semester examination hall ticket generation.")

    add_p("The Digital Leave and OD Application System solves these problems by providing a unified web platform with role-based routing (Student -> Staff -> HOD). Students can submit requests online, view their real-time application status, and track their remaining semester quota. Staff mentors can review and verify applications originating from their department, and the Head of Department can grant final approval. All institutional rules—including the 3-day post-event deadline, the 15-day semester quota cap, date chronology, and duplicate date overlap checks—are enforced automatically by the system.")

    add_p("The application is built using Java and MySQL. The presentation layer uses JavaServer Pages (JSP), HTML5, CSS3, and JavaScript, while the backend logic is implemented using Java Servlets and JDBC. The web application runs on the Apache Tomcat 9 web server. Overall, the system streamlines the leave process, eliminates paperwork, prevents policy violations, and maintains an accurate digital record of all on-duty leaves.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 3: OBJECTIVES
    # ====================================================
    add_h1("Objectives")
    add_h2("Main Objective")
    add_p("To provide a centralized, secure web-based system to automate the collegiate leave and On-Duty application lifecycle. This includes providing online submission forms for students, automated multi-tier approval routing (Student -> Staff -> HOD), real-time status tracking, and programmatic enforcement of institutional regulations such as submission deadlines, category duration caps, and semester quotas.")

    add_h2("Specific Objectives:")

    add_bullet("1. Student Account Registration and Authentication",
               "Allow students to securely access the system using their institutional register number and password. The system verifies credentials against the database, binds the student's profile attributes into an active session, and directs them to their personal dashboard.")

    add_bullet("2. Online Application Composition and Submission",
               "Provide an intuitive web interface for students to draft and submit OD applications. The interface captures event classification, event title, host institution, authorizing coordinator or club, starting date, ending date, and detailed explanatory justification.")

    add_bullet("3. Automated 3-Day Submission Deadline Enforcement",
               "Enforce the institutional bylaw requiring all on-duty applications to be submitted within three calendar days of completing the duty. The system calculates the temporal difference between the event end date and current system time, programmatically blocking late submissions.")

    add_bullet("4. Strict 15-Day Semester Quota Management",
               "Maintain institutional attendance standards by continuously tracking the cumulative number of approved and pending duty days per student. The system automatically rejects any new application that would cause the student to exceed the 15-day ceiling in a single semester.")

    add_bullet("5. Date Chronology and Temporal Overlap Validation",
               "Ensure data consistency by verifying that the selected end date is chronologically equal to or after the start date. Additionally, the system evaluates proposed dates against active applications to prevent duplicate or overlapping bookings for the same student.")

    add_bullet("6. Category-Specific Duration Bounds",
               "Enforce institutional policies regarding event categories, ensuring that maximum allowable duty days correspond directly to the event type (e.g., maximum 2 days for recruitment interviews, 3 days for technical symposia, 5 days for hackathons and sports championships, and 7 days for industrial training).")

    add_bullet("7. First-Tier Staff Scrutiny and Verification",
               "Provide faculty advisors and class mentors with a departmental verification dashboard. Staff members can inspect the student's registration details, event context, and justification, and mark the application as Verified or Rejected with mandatory explanatory comments.")

    add_bullet("8. Second-Tier Executive HOD Approval",
               "Provide the Head of Department with an executive sanction queue displaying only those applications that have successfully passed staff verification. The HOD can grant final Approved status or record an executive rejection.")

    add_bullet("9. Real-Time Analytical Dashboard Metrics",
               "Compute and display live statistical summary cards across all user dashboards. Students can review total applications, approved days, pending requests, and their remaining semester quota balance in real time.")

    add_bullet("10. Historical Audit Ledger and Transparency",
               "Provide students and faculty with an immutable historical ledger of all past applications. Students can review application IDs, date spans, durations, review statuses, and faculty remarks without consulting outside records.")

    add_bullet("11. Two-Tier Defensive Validation Architecture",
               "Implement immediate client-side validation in Vanilla JavaScript to provide instant user feedback on form errors, duplicated with strict server-side validation in Java Servlets to prevent bypass via disabled client scripts.")

    add_bullet("12. Defensive Relational Persistence via JDBC",
               "Store all user profiles, roles, quotas, and application states in a normalized MySQL relational database. The application executes all database operations using native JDBC PreparedStatement parameterized queries to eliminate SQL injection vulnerabilities.")

    add_bullet("13. Role-Based Session Security and Access Control",
               "Implement server-managed HttpSession tracking to ensure that users are strictly restricted to features authorized for their specific role. Students cannot access staff review queues, and staff cannot access executive HOD endpoints.")

    add_h2("Summary")
    add_p("These objectives establish a complete system for managing academic on-duty requests. The project focuses on student accessibility, multi-tier faculty verification, policy compliance, and auditability, creating a solid base for collegiate administrative automation.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 4: SCOPE
    # ====================================================
    add_h1("Scope")
    add_p("The Digital Leave and On-Duty Application System is designed to manage the core leave and on-duty clearance workflows within an academic collegiate environment. The application enables users to participate either as students or as administrative faculty (staff mentors and HODs). The system connects a responsive browser interface to a Java backend and a persistent MySQL database.")

    add_h2("Student Section")
    add_p("Students can access the application using their institutional credentials (register number and password). Upon logging in, students can review their personalized dashboard containing key metrics such as total applications submitted, approved days, pending reviews, and their remaining semester quota out of 15 allowable days.")

    add_p("Students can open the on-duty application form and select an event category, input the event title, specify the authorizing club or faculty coordinator, and pick the starting and ending dates of the event. The application verifies that all required fields are complete, that the dates follow proper chronological order, that the event ended within the allowable 3-day post-event window, and that the requested duration does not breach the 15-day semester quota. Students can also review their complete application history, checking the status of pending requests and reading remarks entered by faculty reviewers.")

    add_h2("Staff Advisor Section")
    add_p("This section of the application provides faculty mentors and class advisors with tools to inspect and verify student on-duty applications. Staff members can view a dedicated verification queue listing all pending applications submitted by students in their department. Mentors can examine the student's register number, name, event metadata, date range, and submitted justification. Staff advisors have the authority to mark an application as 'Verified' (which forwards it to the HOD's executive queue) or 'Rejected' (which terminates the application workflow). When rejecting an application, staff members can enter explanatory comments providing clear guidance to the applicant.")

    add_h2("Head of Department (HOD) Section")
    add_p("The HOD section serves as the final executive clearance tier for institutional attendance records. The HOD can access an executive queue that displays exclusively those applications that have already undergone first-tier staff verification. The HOD can review the application details alongside the staff endorsement and make the final determination: granting official 'Approved' status or marking the application as 'Rejected'. Once approved by the HOD, the leave record is officially recognized, and the requested days are permanently debited against the student's 15-day semester quota.")

    add_h2("Data & Application Processing")
    add_p("All data relating to students, faculty advisors, user credentials, roles, application records, and approval states is stored inside a relational MySQL database. When users log in, open dashboards, submit requests, or take review actions, the application interacts with MySQL. The browser interface communicates with the backend through standard HTTP POST and GET requests handled by Java Servlets. The servlets process incoming form data, execute business rules, and use JDBC to query and update the database.")

    add_h2("Target Users")
    add_p("The application is targeted at members of the academic department: undergraduate and postgraduate students applying for on-duty leave, faculty advisors performing preliminary scrutiny, and departmental heads issuing final attendance clearances. The system is designed to streamline administrative tasks and improve departmental transparency.")

    add_h2("Limitations & Scope")
    add_p("This project is intentionally focused on the management of leave and on-duty requests and related academic policies. It does not include features for timetabling lecture hours, scheduling examinations, managing staff payroll, or directly controlling physical biometric door turnstiles. The current version communicates status updates through web dashboards rather than third-party transactional SMS or email APIs. These boundaries keep the project focused on core leave management while leaving room for future enhancements.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 5: SOFTWARE SPECIFICATIONS
    # ====================================================
    add_h1("Software Specifications")
    add_p("The Digital Leave and OD Application System uses a combination of programming languages, frameworks, database software, and user-interface technologies. The browser application runs through the Apache Tomcat web server and uses MySQL to store all records.")

    add_h2("Software Used")
    specs_data = [
        ("Component", "Specification", "Purpose"),
        ("Programming language", "Java 17 / Java 21", "Implements backend business logic, servlets, and data models."),
        ("Server-side technology", "Java Servlets (Servlet API 4.0)", "Handles HTTP requests, session management, and routing."),
        ("View technology", "JavaServer Pages (JSP 2.3)", "Renders dynamic HTML pages and displays database records."),
        ("Web server", "Apache Tomcat 9.0.x", "Hosts and executes the Java web application and servlets."),
        ("Database", "MySQL Community Server 8.0", "Stores user accounts, student profiles, and OD requests."),
        ("Database access", "JDBC (Java Database Connectivity)", "Connects the Java application to MySQL and runs SQL queries."),
        ("Database driver", "MySQL Connector/J 8.0.x", "Enables binary communication between Java and MySQL."),
        ("Browser interface", "HTML5, CSS3, JavaScript", "Provides responsive web pages, styling, and client-side validation.")
    ]
    add_table_caption("Table 1: Software Specifications")
    t_sp = doc.add_table(rows=len(specs_data), cols=3)
    for r_idx, row in enumerate(specs_data):
        for c_idx, val in enumerate(row):
            t_sp.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_sp, col_widths=[1.6, 2.2, 2.7])

    add_p("")
    add_h2("Runtime and Configuration")
    add_p("The project is configured to use Java 17 or Java 21 and is built for deployment on Apache Tomcat 9. To run the application, a compatible Java runtime environment (JRE/JDK) must be available. Apache Tomcat must be installed and configured.")

    add_p("The application connects to a MySQL database named digital_od. MySQL Community Server must be installed and running locally on TCP port 3306. The database connection parameters are defined in the service.DBConnection utility class, which establishes the connection URL, username, and driver class.")

    add_p("Apache Tomcat runs the web application listening on HTTP port 8080. The web interface can be opened in any standard browser at http://localhost:8080/DigitalODSystem when the server is running locally.")

    add_h2("Client Requirements")
    add_p("To access the web interface, a modern web browser with JavaScript enabled is required (such as Google Chrome, Mozilla Firefox, or Microsoft Edge). The project does not require any specialized browser plugins or third-party client software. A computer display capable of showing standard web forms, data tables, and modal dialogs is required.")

    add_h2("Operating System and Hardware")
    add_p("The application does not depend on a proprietary operating system. It runs reliably on Windows 10, Windows 11, and Linux distributions supporting Java and MySQL. In general, the host computer should have a modern multi-core processor (Intel Core i3/i5 or AMD Ryzen equivalent), at least 8 GB of RAM, and sufficient solid-state storage to accommodate Tomcat binaries, MySQL tablespaces, and server logging buffers.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 6: WORKFLOW
    # ====================================================
    add_h1("Workflow")
    add_p("The Digital Leave and On-Duty Application System is organized into three main functional areas: student operations, staff verification, and HOD approval. Within the web interface, users interact with forms and tables to submit requests to Java Servlets. The servlets process requests, enforce academic bylaws, and query or update the MySQL database before returning responses to the browser.")

    add_h2("1. Starting the application")
    add_p("The Apache Tomcat web server starts up and initializes the application context on port 8080. The user opens the system URL in a browser and is presented with the login page.")

    add_h2("2. User login and role identification")
    add_p("The user enters their username and password. When submitted, LoginServlet validates the credentials against the users table. If the credentials match an existing account, the servlet retrieves the user's role (student, staff, or hod) and profile data, creates an HttpSession, and redirects the browser to the appropriate role dashboard. If the login fails, an error message is returned to the login screen.")

    add_h2("3. Student application drafting and date selection")
    add_p("A student logs in and clicks 'Apply for On-Duty'. In the application modal, the student selects the event category, enters the event name, specifies the authorizing body or mentor, and inputs the start date (fromDate) and end date (toDate). The student also provides a detailed explanation for their absence.")

    add_h2("4. Automated rule enforcement and submission")
    add_p("Client-side JavaScript performs preliminary checks on date order and the 3-day deadline. When the form is submitted, ApplyODServlet re-verifies these checks on the server. The servlet ensures that toDate is chronologically after fromDate, verifies that the event ended within 3 days of the current date, checks that the requested duration matches category limits, verifies that the student does not have an active overlapping request, and verifies that the new days will not exceed the 15-day semester quota. If all checks pass, the application is saved in MySQL with initial statuses: staff_status = 'Pending' and hod_status = 'Pending'.")

    add_h2("5. Staff verification")
    add_p("A staff advisor logs in to access the departmental verification queue. The dashboard displays all pending applications from their department. The advisor reviews the student's register number, event details, and justification. The advisor clicks 'Verify' (updating staff_status to 'Verified' and forwarding the request to the HOD) or 'Reject' (updating staff_status to 'Rejected' and recording an explanatory remark).")

    add_h2("6. Head of Department approval")
    add_p("The HOD logs in to view the executive approval queue, which displays only staff-verified applications. The HOD evaluates the final request and clicks 'Approve' (updating hod_status to 'Approved') or 'Reject'. Once approved by the HOD, the leave is officially sanctioned, and the requested days are permanently debited against the student's 15-day semester quota.")

    add_h2("7. Viewing application history")
    add_p("Students can open their personal history section to review all past applications. The system retrieves historical records from MySQL, displaying date spans, durations, current review statuses, and faculty remarks.")

    add_h2("8. Logout")
    add_p("Users can log out at any time. LogoutServlet terminates the server-side HttpSession, clears client cookies, and returns the browser to the login screen.")

    add_h2("Overall Request Flow")
    add_p("User action -> Browser interface -> Java Servlet (doPost/doGet) -> Validation and Business Logic -> MySQL database via JDBC -> Response/Redirect -> Result displayed to user.")

    add_h2("6.2 Workflow Diagram")
    p_diag = doc.add_paragraph()
    p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag.paragraph_format.first_line_indent = Inches(0)
    p_diag.paragraph_format.space_before = Pt(10)
    p_diag.paragraph_format.space_after = Pt(10)
    r_diag = p_diag.add_run()
    r_diag.add_picture(r"c:\Users\ivins\Desktop\MCA\DigitalODSystem\workflow_diagram.png", width=Inches(5.5))

    doc.add_page_break()

    # ====================================================
    # CHAPTER 7: MODULES OF THE PROJECT
    # ====================================================
    add_h1("Phase-wise explanation:")
    add_p("The Digital Leave and On-Duty Application System was constructed in structured phases. These are the phases and technologies utilized throughout the project.")

    add_h2("Phase 1: Set up and Basic Design")
    add_p("The first phase established the structural foundation of the application and the relational data entities. The project schema was designed to store two core entities: users (encapsulating authentication credentials, roles, roll numbers, and department affiliations) and od_requests (storing student usernames, event classifications, event titles, authorizing coordinators, date spans, duration counts, justifications, and approval statuses).")

    add_p("Domain models were authored in the model package: User.java and ODRequest.java. These plain Java objects represent database records in memory, providing constructor overloads, accessors, and helper methods such as isFullyApproved() and isAnyRejected() to simplify status evaluation.")

    add_p("Basic validation rules were established to ensure complete data entry, including mandatory field checks, valid date formatting, and credential verification.")

    add_h2("Phase 2: Structured Programming and Custom Exception Handling")
    add_p("The Java files were organized into a clean package hierarchy: model, service, controller, and exception. Each layer has an explicit responsibility. The service package defines service interfaces (AuthService, ODService) and concrete implementations (AuthServiceImpl, ODServiceImpl) that manage business rules and database communication.")

    add_p("To avoid exposing raw database or runtime exceptions to users, a dedicated checked exception InvalidInputException.java was implemented in the exception package. It intercepts validation errors—such as deadline violations, quota exceedances, and date overlaps—and encapsulates user-readable messages that are returned to the controller layer.")

    add_h2("Phase 3: Web Interface")
    add_p("The web interface was developed using HTML5, CSS3, and JavaScript. The interface comprises login.html, student_dashboard.jsp, staff_dashboard.jsp, and hod_dashboard.jsp. The CSS stylesheet defines a clean, responsive layout with distinct status badges (amber for Pending, green for Verified/Approved, and red for Rejected).")

    add_p("Client-side validation was implemented in JavaScript (od_validation.js). It performs instant mathematical checks: verifying non-empty fields, ensuring end dates do not precede start dates, computing requested days, and warning students if an event ended more than 3 days prior.")

    add_h2("Phase 4: Server Side")
    add_p("Server-side request handling was implemented using standard Java Servlets extending HttpServlet: LoginServlet, ApplyODServlet, UpdateODStatusServlet, and LogoutServlet. Servlets parse incoming HTTP parameters, verify active session identity, invoke service methods, and issue redirects with appropriate query status flags.")

    add_p("Database connectivity was implemented using native JDBC PreparedStatement parameterized queries inside DBConnection.java, guaranteeing immunity to SQL injection. User state and role permissions are maintained across requests using server-side HttpSession tracking.")

    add_h2("Summary of the Phases")
    add_p("Application data model -> Structured Java packages and custom exceptions -> Browser forms and JS validation -> Java Servlets, JDBC persistence, and session security.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 8: SOURCE CODE
    # ====================================================
    add_h1("Source Code (Only functional code structure)")
    add_p("This section presents the project structure and selected code excerpts that illustrate how the application functions. The excerpts focus on database connectivity, custom exception handling, servlet request processing, and client-side validation.")

    add_h2("Project Structure")
    add_code('''DigitalODSystem/
├── WEB-INF/
│   └── web.xml
├── css/
│   └── style.css
├── js/
│   └── od_validation.js
├── model/
│   ├── User.java
│   └── ODRequest.java
├── service/
│   ├── DBConnection.java
│   ├── AuthService.java
│   ├── AuthServiceImpl.java
│   ├── ODService.java
│   └── ODServiceImpl.java
├── controller/
│   ├── LoginServlet.java
│   ├── ApplyODServlet.java
│   ├── UpdateODStatusServlet.java
│   └── LogoutServlet.java
├── exception/
│   └── InvalidInputException.java
├── login.html
├── student_dashboard.jsp
├── staff_dashboard.jsp
└── hod_dashboard.jsp''')

    add_h2("1. Database Connection Management")
    add_p("DBConnection.java provides a centralized connection factory using the JDBC DriverManager.")
    add_code('''package service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/digital_od?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASSWORD = "password123";

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.err.println("MySQL Driver not found: " + e.getMessage());
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}''')

    add_h2("2. Custom Domain Exception")
    add_p("InvalidInputException.java reports validation and institutional policy violations.")
    add_code('''package exception;

public class InvalidInputException extends Exception {
    private static final long serialVersionUID = 1L;

    public InvalidInputException(String message) {
        super(message);
    }
}''')

    add_h2("3. Database-Based Authentication")
    add_p("AuthServiceImpl.java checks submitted credentials against the users table using a parameterized query.")
    add_code('''package service;

import java.sql.*;
import model.User;

public class AuthServiceImpl implements AuthService {
    @Override
    public User authenticate(String username, String password) {
        String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, username.trim());
            ps.setString(2, password.trim());
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new User(
                        rs.getInt("id"),
                        rs.getString("username"),
                        rs.getString("role"),
                        rs.getString("roll_no"),
                        rs.getString("full_name"),
                        rs.getString("department")
                    );
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }
}''')

    add_h2("4. OD Application Processing Servlet")
    add_p("ApplyODServlet.java handles OD submissions and verifies the 3-day post-event deadline.")
    add_code('''package controller;

import exception.InvalidInputException;
import model.ODRequest;
import service.ODService;
import service.ODServiceImpl;
import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

@WebServlet("/applyODServlet")
public class ApplyODServlet extends HttpServlet {
    private final ODService odService = new ODServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("loggedInUser") == null) {
            response.sendRedirect("login.html");
            return;
        }

        String username = (String) session.getAttribute("loggedInUser");
        String rollNo = (String) session.getAttribute("rollNo");
        String eventType = request.getParameter("eventType");
        String eventName = request.getParameter("eventName");
        String authorizedBody = request.getParameter("authorizedBody");
        String fromDateStr = request.getParameter("fromDate");
        String toDateStr = request.getParameter("toDate");
        String reason = request.getParameter("reason");

        try {
            LocalDate fromDate = LocalDate.parse(fromDateStr.trim());
            LocalDate toDate = LocalDate.parse(toDateStr.trim());

            if (toDate.isBefore(fromDate)) {
                throw new InvalidInputException("To Date cannot precede From Date.");
            }

            long daysPassed = ChronoUnit.DAYS.between(toDate, LocalDate.now());
            if (daysPassed > 3) {
                throw new InvalidInputException("OD must be submitted within 3 days of duty completion.");
            }

            int daysCount = (int) ChronoUnit.DAYS.between(fromDate, toDate) + 1;
            ODRequest od = new ODRequest(username, rollNo, eventType, eventName,
                                         authorizedBody, fromDateStr, toDateStr, daysCount, reason);

            odService.applyOD(od);
            response.sendRedirect("student_dashboard.jsp?status=success");

        } catch (InvalidInputException e) {
            response.sendRedirect("student_dashboard.jsp?status=error&msg=" + e.getMessage());
        }
    }
}''')

    add_h2("5. Client-Side JavaScript Validation")
    add_p("od_validation.js performs immediate checks in the browser before form submission.")
    add_code('''document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("odForm");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        const fromDateVal = document.getElementById("fromDate").value;
        const toDateVal = document.getElementById("toDate").value;

        if (!fromDateVal || !toDateVal) {
            alert("Please enter both start and end dates.");
            e.preventDefault();
            return;
        }

        const fromDate = new Date(fromDateVal);
        const toDate = new Date(toDateVal);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (toDate < fromDate) {
            alert("To Date cannot be earlier than From Date.");
            e.preventDefault();
            return;
        }

        const diffDays = Math.floor((today - toDate) / (1000 * 60 * 60 * 24));
        if (diffDays > 3) {
            alert("Policy Violation: OD must be submitted within 3 days of event completion.");
            e.preventDefault();
            return;
        }
    });
});''')

    add_h2("How the Main Code Parts Work Together")
    add_p("The web workflow follows this sequence:\nBrowser Form -> JavaScript client validation -> Form submission via HTTP POST -> ApplyODServlet intercepts request -> Session authentication confirmed -> Business rules checked in ODServiceImpl -> Parameterized SQL executed via JDBC in DBConnection -> MySQL database updated -> Response redirect sent to browser -> Updated status rendered in JSP.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 9: FEATURES OF THE PROJECT
    # ====================================================
    add_h1("Features of the Project")
    add_p("The Digital Leave and On-Duty Application System includes various aspects of student leave management and institutional policy enforcement. The following features are available in the application:")

    add_bullet("1) Student Login and Authentication",
               "Students log in using their username (register number) and password. The system checks credentials against the users table. If the details match an active student account, the student dashboard opens. If login fails, an error message is displayed on the login page.")

    add_bullet("2) Online Application for On-Duty",
               "Students can apply for on-duty leave through an interactive web form. Students select the event category, enter the event name and host institution, specify the authorizing club or coordinator, and input the date range. All fields are validated before submission.")

    add_bullet("3) Strict 3-Day Rule Enforcement",
               "The application programmatically rejects applications submitted more than three calendar days after the conclusion of the duty. This eliminates post-hoc leave manufacturing and ensures timely record keeping.")

    add_bullet("4) 15-Day Semester Quota Management",
               "The system tracks cumulative duty days per student. When a new request is submitted, the system checks whether the requested days combined with existing approved days will exceed 15 days. If the quota is exceeded, the request is rejected with a clear message.")

    add_bullet("5) Date Chronology Validation",
               "The system ensures that the selected end date is chronologically equal to or after the start date, preventing inverted date errors.")

    add_bullet("6) Duplicate Date Overlap Prevention",
               "The application checks existing records to ensure a student does not submit multiple applications spanning overlapping dates, preventing double-booking.")

    add_bullet("7) Category-Specific Duration Bounds",
               "Institutional limits on allowable duration per event category are enforced automatically (e.g., maximum 2 days for placements, 3 days for symposia, 5 days for hackathons/sports, and 7 days for industrial training).")

    add_bullet("8) Staff Verification Queue",
               "Faculty advisors can view all pending requests originating from students in their department. Staff can review submitted justifications and mark requests as Verified or Rejected with written feedback.")

    add_bullet("9) Head of Department Approval",
               "The Head of Department can access verified requests and grant final institutional approval or record an executive rejection.")

    add_bullet("10) Real-Time Dashboard Metrics",
               "Student dashboards display live summary cards for Total Applications, Approved Days, Pending In-Review Requests, and Remaining Semester Quota (calculated dynamically as 15 - Approved Days).")

    add_bullet("11) Historical Application Ledger",
               "Students can view their full leave history, including unique application IDs, event details, date ranges, duration counts, staff status, HOD status, and reviewer comments.")

    add_bullet("12) Two-Tier Defensive Validation",
               "Validation occurs in JavaScript for instantaneous browser feedback and is strictly repeated on the server in Java Servlets to prevent unauthorized bypass.")

    add_bullet("13) Secure Data Storage via JDBC",
               "All data is stored safely in MySQL. Queries use parameterized PreparedStatement interfaces to ensure complete protection against SQL injection attacks.")

    add_h2("Summary")
    add_p("These features provide a complete digital replacement for manual paper leave forms, giving students, faculty advisors, and departmental leadership full visibility, compliance, and control over on-duty clearances.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 10: REQUIREMENTS ANALYSIS
    # ====================================================
    add_h1("Requirements Analysis")
    add_p("This section lists what the application is expected to do and the operational conditions it works under. The requirements are grouped into functional requirements and non-functional considerations.")

    add_h2("Functional Requirements")
    fr_data = [
        ("ID", "Requirement", "Role"),
        ("FR-01", "User can log in with username and password; system identifies role.", "All Users"),
        ("FR-02", "System creates secure HttpSession upon valid authentication.", "All Users"),
        ("FR-03", "Student can submit OD request with category, title, endorsement, and dates.", "Student"),
        ("FR-04", "System calculates total days: (toDate - fromDate) + 1.", "System"),
        ("FR-05", "System rejects requests where toDate is earlier than fromDate.", "Student"),
        ("FR-06", "System rejects requests submitted more than 3 days after event completion.", "Student"),
        ("FR-07", "System tracks used days and blocks submissions exceeding 15-day semester quota.", "Student"),
        ("FR-08", "System rejects applications with dates overlapping existing active requests.", "Student"),
        ("FR-09", "System stores new applications with initial status Pending.", "System"),
        ("FR-10", "Student dashboard displays live metrics and remaining quota balance.", "Student"),
        ("FR-11", "Staff advisor can view pending requests from their department.", "Staff"),
        ("FR-12", "Staff advisor can mark request as Verified or Rejected with comments.", "Staff"),
        ("FR-13", "HOD can view staff-verified applications awaiting executive approval.", "HOD"),
        ("FR-14", "HOD can grant final Approval or mark request as Rejected.", "HOD"),
        ("FR-15", "Student can view historical ledger of all past applications and remarks.", "Student"),
        ("FR-16", "User can log out, invalidating the session and returning to login page.", "All Users")
    ]
    add_table_caption("Table 2: Functional Requirements Matrix")
    t_fr = doc.add_table(rows=len(fr_data), cols=3)
    for r_idx, row in enumerate(fr_data):
        for c_idx, val in enumerate(row):
            t_fr.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_fr, col_widths=[1.1, 4.3, 1.1])

    add_p("")
    add_h2("Non-Functional Considerations")
    add_bullet("Usability:", "The interface is organized into clean, dedicated pages for login, student operations, staff verification, and HOD approval. Form errors are displayed in plain language adjacent to inputs.")
    add_bullet("Maintainability:", "The Java code is divided by responsibility following the MVC pattern. Presentation (JSP), request routing (Servlets), business rules (Services), and database operations (JDBC) are separated cleanly.")
    add_bullet("Portability:", "The project runs on any system supporting Java 17/21, Apache Tomcat 9, and MySQL 8.0.")
    add_bullet("Data Integrity:", "Foreign key constraints ensure referential consistency between users and applications. Parameterized queries prevent malformed SQL statements.")
    add_bullet("Security:", "Server-side role checks and session validation prevent unauthorized privilege escalation.")

    add_h2("Assumptions and Constraints")
    add_p("The project assumes MySQL 8.0 is running on port 3306 with the digital_od database initialized. Student, faculty, and HOD accounts are provisioned in the database. Days are counted as continuous calendar working days.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 11: USE CASE DESCRIPTIONS
    # ====================================================
    add_h1("Use Case Descriptions")
    add_p("Use cases describe how actors interact with the system to achieve specific goals. Below are the primary use cases for students, staff advisors, and the Head of Department.")

    add_h2("UC-01 Login")
    add_bullet("Actor:", "Student / Staff / HOD")
    add_bullet("Preconditions:", "Account exists in the database; user has navigated to login page.")
    add_bullet("Main Flow:", "1. User enters username and password. 2. LoginServlet queries users table. 3. System identifies user role. 4. System creates HttpSession and redirects user to their role dashboard.")
    add_bullet("Alternatives:", "If credentials do not match, error message 'Invalid username or password' is shown.")
    add_bullet("Post Conditions:", "User is authenticated and viewing their dashboard.")

    add_h2("UC-02 Submit OD Application")
    add_bullet("Actor:", "Student")
    add_bullet("Preconditions:", "Student is logged in; remaining semester quota > 0.")
    add_bullet("Main Flow:", "1. Student opens application form. 2. Inputs category, title, authorizing body, start date, end date, and justification. 3. Client JS validates date order and 3-day deadline. 4. Form submitted to ApplyODServlet. 5. Server checks 3-day deadline, quota, and date overlap. 6. Application saved in MySQL with Pending status.")
    add_bullet("Alternatives:", "If the event ended more than 3 days ago or exceeds quota, an InvalidInputException is raised and displayed on the dashboard.")
    add_bullet("Post Conditions:", "New OD application stored in MySQL.")

    add_h2("UC-03 Staff Verification")
    add_bullet("Actor:", "Staff Advisor")
    add_bullet("Preconditions:", "Staff is logged in; pending departmental requests exist.")
    add_bullet("Main Flow:", "1. Staff opens staff dashboard. 2. Reviews pending student applications. 3. Clicks 'Verify'. 4. UpdateODStatusServlet updates staff_status to Verified. 5. Application advances to HOD queue.")
    add_bullet("Alternatives:", "Staff clicks 'Reject' and inputs remarks; status updates to Rejected.")
    add_bullet("Post Conditions:", "Application status updated; advances to HOD or terminates.")

    add_h2("UC-04 HOD Approval")
    add_bullet("Actor:", "Head of Department")
    add_bullet("Preconditions:", "HOD is logged in; verified requests exist.")
    add_bullet("Main Flow:", "1. HOD views verified requests on HOD dashboard. 2. Reviews application and clicks 'Approve'. 3. UpdateODStatusServlet updates hod_status to Approved. 4. Requested days debited from student quota.")
    add_bullet("Alternatives:", "HOD clicks 'Reject'; status updates to Rejected.")
    add_bullet("Post Conditions:", "Application officially approved; leave granted.")

    add_h2("UC-05 View Application History")
    add_bullet("Actor:", "Student")
    add_bullet("Preconditions:", "Student is logged in.")
    add_bullet("Main Flow:", "1. Student opens history section. 2. Browser requests applications from database. 3. System retrieves records and displays dates, duration, review statuses, and faculty comments.")
    add_bullet("Alternatives:", "If no applications exist, a message states no records are found.")
    add_bullet("Post Conditions:", "Student views history; no data modified.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 12 & 13: ARCHITECTURE & DATABASE
    # ====================================================
    add_h1("System Architecture")
    add_p("The application follows a layered Model-View-Controller (MVC) structure. Keeping responsibilities separate makes it easier to understand where behavior is implemented and where to make future modifications.")

    add_h2("Layers")
    add_bullet("Presentation Layer:", "JSP pages and HTML forms (student_dashboard.jsp, staff_dashboard.jsp, hod_dashboard.jsp) provide the web interface with CSS styling and JavaScript validation.")
    add_bullet("Controller Layer:", "Java Servlets (LoginServlet, ApplyODServlet, UpdateODStatusServlet, LogoutServlet) receive HTTP requests, enforce session checks, and call the service layer.")
    add_bullet("Model and Service Layer:", "Java POJO classes (User, ODRequest) and service implementations (AuthServiceImpl, ODServiceImpl) execute business rules and connect to MySQL via JDBC.")
    add_bullet("Data Layer:", "A MySQL database named digital_od stores user credentials, profiles, quotas, and application records.")

    add_h1("Database Design Overview")
    add_p("The database holds user accounts and OD application records. This chapter describes the tables and their relationships.")

    add_h2("Table: users")
    u_cols = [
        ("Column", "Type", "Description"),
        ("id", "INT AUTO_INCREMENT PK", "Unique user ID."),
        ("username", "VARCHAR(50) UNIQUE", "Login username / roll number."),
        ("password", "VARCHAR(100)", "Account password."),
        ("role", "VARCHAR(20)", "Role: student, staff, or hod."),
        ("roll_no", "VARCHAR(30)", "Roll Number or Staff ID."),
        ("full_name", "VARCHAR(100)", "Full name of the user."),
        ("department", "VARCHAR(100)", "Department name."),
        ("course", "VARCHAR(50)", "Degree course.")
    ]
    add_table_caption("Table 3: Database Schema - Users Table")
    t_u = doc.add_table(rows=len(u_cols), cols=3)
    for r_idx, row in enumerate(u_cols):
        for c_idx, val in enumerate(row):
            t_u.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_u, col_widths=[1.8, 2.2, 2.5])

    add_p("")
    add_h2("Table: od_requests")
    od_cols = [
        ("Column", "Type", "Description"),
        ("id", "INT AUTO_INCREMENT PK", "Application reference ID."),
        ("student_username", "VARCHAR(50) FK", "References users(username)."),
        ("roll_no", "VARCHAR(30)", "Student register roll number."),
        ("event_type", "VARCHAR(100)", "Category of event."),
        ("event_name", "VARCHAR(200)", "Name and host of event."),
        ("authorized_body", "VARCHAR(150)", "Endorsing club or coordinator."),
        ("from_date", "DATE", "Start date of duty."),
        ("to_date", "DATE", "End date of duty."),
        ("days_count", "INT", "Total requested duty days."),
        ("reason", "TEXT", "Justification description."),
        ("staff_status", "VARCHAR(30)", "Status: Pending, Verified, Rejected."),
        ("hod_status", "VARCHAR(30)", "Status: Pending, Approved, Rejected.")
    ]
    add_table_caption("Table 4: Database Schema - OD Requests Table")
    t_od = doc.add_table(rows=len(od_cols), cols=3)
    for r_idx, row in enumerate(od_cols):
        for c_idx, val in enumerate(row):
            t_od.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_od, col_widths=[1.8, 2.2, 2.5])

    doc.add_page_break()

    # ====================================================
    # CHAPTER 14 & 15: VALIDATION & TESTING
    # ====================================================
    add_h1("Input Validation and Error Handling")
    add_p("Validation protects the database from incomplete or invalid data. The application validates in two places: the browser performs preliminary checks in JavaScript for instant feedback, and Java Servlets repeat all checks on the server to prevent bypass.")

    add_h1("Testing")
    add_p("Testing checks that the application behaves as described in the requirements. The test cases below were executed against a local deployment on Apache Tomcat 9 and MySQL 8.0.")

    add_h2("Test Environment")
    add_p("Language: Java 17/21 | Server: Apache Tomcat 9.0 | Database: MySQL 8.0 (digital_od) | Browser: Google Chrome, Firefox")

    add_h2("Test Cases")
    tc_data = [
        ("TC ID", "Requirement", "Input and Action", "Expected Result", "Result"),
        ("TC-01", "FR-01", "Enter valid student credentials", "Login succeeds; student dashboard opens.", "Pass"),
        ("TC-02", "FR-01", "Enter valid staff credentials", "Login succeeds; staff dashboard opens.", "Pass"),
        ("TC-03", "FR-01", "Enter valid HOD credentials", "Login succeeds; HOD dashboard opens.", "Pass"),
        ("TC-04", "FR-01", "Enter incorrect password", "Message: Invalid username or password.", "Pass"),
        ("TC-05", "FR-03", "Submit valid OD within all rules", "Success message; saved in database.", "Pass"),
        ("TC-06", "FR-05", "Submit with toDate before fromDate", "Message: To Date cannot precede From Date.", "Pass"),
        ("TC-07", "FR-06", "Submit OD for event 5 days ago", "Message: Must be submitted within 3 days.", "Pass"),
        ("TC-08", "FR-06", "Submit OD for event exactly 3 days ago", "Application accepted (boundary test).", "Pass"),
        ("TC-09", "FR-07", "Submit request exceeding 15-day quota", "Message: Exceeds maximum 15-day semester quota.", "Pass"),
        ("TC-10", "FR-08", "Submit request on overlapping dates", "Message: Duplicate date conflict detected.", "Pass"),
        ("TC-11", "FR-12", "Staff clicks Verify on pending request", "Status updates to Verified; moves to HOD.", "Pass"),
        ("TC-12", "FR-12", "Staff clicks Reject and adds comment", "Status updates to Rejected; request terminates.", "Pass"),
        ("TC-13", "FR-14", "HOD clicks Approve on verified request", "Status updates to Approved; quota debited.", "Pass"),
        ("TC-14", "FR-14", "HOD clicks Reject on verified request", "Status updates to Rejected; request terminates.", "Pass"),
        ("TC-15", "FR-16", "Click logout button", "Session ends; returns to login page.", "Pass")
    ]
    add_table_caption("Table 5: System Verification and Test Plan")
    t_tc = doc.add_table(rows=len(tc_data), cols=5)
    for r_idx, row in enumerate(tc_data):
        for c_idx, val in enumerate(row):
            t_tc.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_tc, col_widths=[0.9, 1.1, 2.2, 1.8, 0.5])

    doc.add_page_break()

    # ====================================================
    # CHAPTER 16 & 17: SECURITY & INSTALLATION
    # ====================================================
    add_h1("Security Considerations and Known Limitations")
    add_h2("Measures Already in Place")
    add_bullet("Parameterized Queries:", "Every database operation passes values as parameters using JDBC PreparedStatement, neutralizing SQL injection attacks.")
    add_bullet("Server-Side Validation:", "All dates, durations, and quotas are checked again on the server to prevent bypass.")
    add_bullet("Session-Based Access Control:", "Servlets inspect user roles before executing administrative actions, preventing unauthorized URL access.")

    add_h2("Known Limitations")
    add_bullet("Password Storage:", "Passwords are stored in plain text for learning purposes; production systems must use salted hashes (BCrypt).")
    add_bullet("Transport Security:", "The application runs over HTTP locally; production deployment requires HTTPS.")
    add_bullet("Connection Management:", "Connections are opened on demand; an enterprise connection pool (HikariCP) should be used for production.")

    add_h1("Installation and Execution Guide")
    add_p("Step 1: Install MySQL Server 8.0 and create the database digital_od. Run schema.sql to initialize tables.")
    add_p("Step 2: Install Apache Tomcat 9 and Java JDK 17 or 21.")
    add_p("Step 3: Deploy the application WAR file to Tomcat's webapps directory.")
    add_p("Step 4: Start Apache Tomcat and verify it is listening on port 8080.")
    add_p("Step 5: Open a browser and navigate to http://localhost:8080/DigitalODSystem/login.html.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 18: APPLICATION SCREENSHOTS
    # ====================================================
    add_h1("Application Screenshots")
    add_p("This chapter shows the main screens of the Digital Leave and On-Duty (OD) Application System in use.")

    add_p("Figure 1: Login Screen")
    add_image_box("Login Portal Screen", "Paste the screenshot of the unified login screen here", height_in_inches=2.5)

    add_p("Figure 2: Student Dashboard & OD Quota Metrics")
    add_image_box("Student Dashboard Screen", "Paste the screenshot showing Edwin Saji (26MCAC22), 15-day quota cards, and history table here", height_in_inches=2.5)

    doc.add_page_break()

    add_p("Figure 3: Apply for On-Duty (OD) Modal Form")
    add_image_box("OD Application Modal Form", "Paste the screenshot of the OD application form modal showing event category, dates, and 3-day rule notice here", height_in_inches=2.5)

    add_p("Figure 4: Staff Advisor Verification Queue")
    add_image_box("Staff Verification Dashboard", "Paste the screenshot of the faculty advisor review table with Verify and Reject buttons here", height_in_inches=2.5)

    doc.add_page_break()

    add_p("Figure 5: Head of Department (HOD) Approval Dashboard")
    add_image_box("HOD Executive Sanction Screen", "Paste the screenshot showing verified requests awaiting final HOD approval here", height_in_inches=2.5)

    add_p("Figure 6: Application History & Approval Status")
    add_image_box("Student Audit Ledger Screen", "Paste the screenshot showing approved status badges and faculty remarks here", height_in_inches=2.5)

    doc.add_page_break()

    # ====================================================
    # CHAPTER 19 & 20: GLOSSARY & REFERENCES
    # ====================================================
    add_h1("Glossary")
    gl_data = [
        ("Term", "Meaning"),
        ("OD (On-Duty)", "Authorized academic leave excusing attendance absence for sanctioned college activities."),
        ("Servlet", "A Java program that runs on a web server to handle HTTP requests and generate responses."),
        ("JSP", "JavaServer Pages, a server-side technology for generating dynamic HTML web pages."),
        ("JDBC", "Java Database Connectivity, standard API connecting Java applications to relational databases."),
        ("MVC", "Model-View-Controller, architectural pattern separating data, user interface, and routing logic."),
        ("PreparedStatement", "Parameterized JDBC interface preventing SQL injection vulnerabilities."),
        ("HttpSession", "Server-side mechanism for storing user identity and role between HTTP requests.")
    ]
    add_table_caption("Table 6: Academic and Technical Glossary")
    t_gl = doc.add_table(rows=len(gl_data), cols=2)
    for r_idx, row in enumerate(gl_data):
        for c_idx, val in enumerate(row):
            t_gl.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_gl, col_widths=[2.0, 4.5])

    add_p("")
    add_h1("References")
    add_p("1. Oracle Corporation. Java Servlet Specification 4.0 (JSR 369). https://javaee.github.io/servlet-spec/")
    add_p("2. Apache Software Foundation. Apache Tomcat 9 Documentation. https://tomcat.apache.org/tomcat-9.0-doc/")
    add_p("3. MySQL Reference Manual. Oracle Corporation. https://dev.mysql.com/doc/")
    add_p("4. Mozilla Developer Network (MDN). HTML5, CSS3, and JavaScript Guides. https://developer.mozilla.org/")
    add_p("5. OWASP Foundation. SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 21: FUTURE ENHANCEMENTS
    # ====================================================
    add_h1("Future Enhancement")
    add_p("The Digital Leave and On-Duty Application System currently focuses on core leave application, multi-tier routing, and policy enforcement. The system could be extended in several ways to support broader campus operations. The enhancements below represent possible future developments.")

    add_h2("1. Strengthen Account Security")
    add_p("A future version should improve how account credentials are stored and handled. Passwords should be stored as salted hashes rather than plain text, using an established hashing algorithm such as BCrypt or Argon2. The application could also introduce password reset functionality, account lockout after repeated failed sign-in attempts, and stricter password complexity rules.")

    add_p("Access control could be enhanced by implementing CSRF (Cross-Site Request Forgery) protection tokens on all form submissions and enforcing token-based session expiration. These improvements would protect student and faculty accounts from unauthorized access.")

    add_h2("2. Biometric Attendance Integration")
    add_p("A significant future enhancement would be connecting the application directly with campus biometric turnstiles and RFID attendance logging machines. Once an on-duty request attains final approval from the Head of Department, an automated database trigger could update the central biometric attendance register, marking the student present for scheduled lecture hours during the approved date span. This would eliminate the need for manual attendance corrections by administrative staff.")

    add_h2("3. Multi-Channel Transactional Alerts")
    add_p("Currently, status updates are checked by logging into the portal. A future version could integrate transactional notification services using the JavaMail API or SMS webhooks (e.g., Twilio). Students would receive instant text messages or email alerts when their applications are verified or rejected, and faculty members would receive daily email summaries of pending review queues.")

    add_h2("4. Timetable ERP Schedule Synchronization")
    add_p("Connecting the on-duty system with the college ERP timetable database would allow the system to automatically cross-reference proposed leave dates against the student's actual lecture schedule. The system could flag potential conflicts with mandatory laboratory sessions or internal continuous assessment tests, providing faculty reviewers with richer context.")

    add_h2("5. Cryptographically Signed QR OD Slips")
    add_p("Upon final approval, the system could dynamically generate downloadable PDF clearance certificates (using libraries such as iText or Apache PDFBox). Each certificate could include an embedded, cryptographically signed QR code, allowing campus security guards and examination invigilators to instantly verify application authenticity using a handheld smartphone scanner.")

    add_h2("6. Dedicated Mobile Application")
    add_p("A cross-platform mobile application developed using Flutter or React Native could be introduced. The mobile app would connect to the Java backend via secure REST API endpoints, allowing students to submit applications, capture supporting documents with their phone cameras, and enabling faculty to issue approvals on mobile devices.")

    add_h2("7. Expand Reporting and Dashboard Information")
    add_p("Administrative reports could help departmental leadership understand student engagement in co-curricular activities. Summaries could include total duty days granted per month, participation trends across categories (technical, cultural, sports), and export options to CSV or PDF formats.")

    add_h2("8. Student Profile Self-Service")
    add_p("Students could be permitted to update selected contact details, such as their phone number or email address, without administrative intervention. The system would validate changes and notify mentors of sensitive profile updates.")

    add_h2("9. Improve User Interface and Accessibility")
    add_p("The web interface could be further refined with enhanced accessibility features, such as high-contrast themes, full keyboard navigation support, and responsive layouts optimized for smaller tablet screens.")

    add_h2("10. Automated Database Backups and Reliability")
    add_p("Automated scheduled backups of the MySQL database and documented restoration procedures would ensure business continuity in the event of hardware or server failures.")

    add_h2("11. Add Automated Unit and Integration Testing")
    add_p("A comprehensive suite of automated tests using JUnit could be developed to test date validation logic, quota calculations, and servlet responses, ensuring system stability during future updates.")

    add_h2("12. Cloud Deployment and Containerization")
    add_p("The application could be containerized using Docker and deployed on cloud infrastructure (such as AWS or Microsoft Azure) with managed relational database services and automated load balancing.")

    doc.add_page_break()

    # ====================================================
    # CHAPTER 22: CONCLUSION
    # ====================================================
    add_h1("Conclusion")
    add_p("The Digital Leave and On-Duty (OD) Application System was developed to digitize and automate the collegiate leave process, replacing inefficient paper-based forms with an automated, role-gated web platform. The system brings together all essential on-duty tasks into a single unified environment, providing functions for students to submit requests, monitor review statuses, and track their remaining semester quota, while enabling faculty mentors and departmental heads to review, verify, and approve applications online.")

    add_p("The application connects a responsive browser interface to server-side Java logic and a relational MySQL database. The front-end pages are built with HTML5, CSS3, and JavaScript, while Java Servlets and JDBC handle request dispatching, business rule enforcement, and database transactions on an Apache Tomcat 9 web server. Together, these components demonstrate how an enterprise Model-View-Controller architecture can support an academic workflow.")

    add_p("An essential strength of the system is its deterministic enforcement of institutional academic policies. The application programmatically verifies the non-negotiable 3-day post-event submission deadline, caps cumulative duty tenure at 15 days per semester, enforces date chronology, and eliminates duplicate bookings across overlapping dates. These automated safeguards prevent policy violations and ensure fair, consistent academic administration across the department.")

    add_p("Input validation is applied defensively at two tiers: the browser provides instantaneous visual feedback to guide students during form completion, and server-side Java Servlets rigorously re-evaluate all rules before executing database updates. Parameterized PreparedStatement queries ensure that all database operations remain protected against SQL injection attacks.")

    add_p("The system has a clearly defined scope focused on leave and on-duty clearances. While it does not include wider ERP functions such as class scheduling or payroll, its modular architecture provides a solid starting point for future extensions, including biometric attendance integration, mobile applications, and automated notifications.")

    add_p("In conclusion, the Digital Leave and On-Duty Application System demonstrates how fundamental Java Enterprise technologies can be effectively harnessed to solve real-world administrative challenges. By eliminating paperwork, reducing processing latency, and ensuring compliance with academic bylaws, the system provides a practical, reliable, and scalable digital solution for modern collegiate administration.")

    # Save
    targets = [
        r"c:\Users\ivins\Desktop\MCA\DigitalODSystem\Digital_OD_Practical_Report.docx",
        r"c:\Users\ivins\Desktop\MCA\DigitalODSystem\Project_Practical_Report.docx",
        r"c:\Users\ivins\Desktop\MCA\DigitalODSystem\PROJECT_BASED_PRACTICAL_REPORT_EDWIN_SAJI.docx"
    ]
    for target in targets:
        try:
            doc.save(target)
            print("SUCCESS: Report saved cleanly to", target)
        except Exception as e:
            print("Could not save to", target, ":", e)

if __name__ == "__main__":
    create_60page_report()
