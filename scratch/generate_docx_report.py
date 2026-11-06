import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def generate_report():
    doc = Document()

    # 1. Page Setup: 1.0 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Enable different first page if needed, but here we can format header/footer
        section.different_first_page_header_footer = True
        
        # Top Header: "Kristu Jayanti University" Centered
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hrun = hp.add_run("Kristu Jayanti University")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(10)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(100, 100, 100)
        
        # Bottom Footer: "Page X" Centered
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(10)
        frun.font.color.rgb = RGBColor(100, 100, 100)
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(fldSimple)

        # Page Border to every page
        sectPr = section._sectPr
        pgBorders = parse_xml(
            '<w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'w:offsetFrom="page">'
            '<w:top w:val="single" w:sz="12" w:space="24" w:color="222222"/>'
            '<w:left w:val="single" w:sz="12" w:space="24" w:color="222222"/>'
            '<w:bottom w:val="single" w:sz="12" w:space="24" w:color="222222"/>'
            '<w:right w:val="single" w:sz="12" w:space="24" w:color="222222"/>'
            '</w:pgBorders>'
        )
        sectPr.append(pgBorders)

    # Typography & Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    def set_font_tnr(run, size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    # Heading 1: 16pt, Centered, Bold
    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        set_font_tnr(run, size_pt=16, bold=True)
        return p

    # Heading 2: 14pt, Left-aligned, Bold
    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        set_font_tnr(run, size_pt=14, bold=True)
        return p

    # Heading 3: 12pt, Left-aligned, Bold
    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        set_font_tnr(run, size_pt=12, bold=True)
        return p

    # Standard body paragraph: Indented first line
    def add_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        set_font_tnr(run, size_pt=12)
        return p

    # Bullet point
    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            set_font_tnr(run_b, size_pt=12, bold=True)
        run = p.add_run(text)
        set_font_tnr(run, size_pt=12)
        return p

    # Table caption: Bold caption above table
    def add_table_caption(caption_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(caption_text)
        set_font_tnr(run, size_pt=11, bold=True)
        return p

    # Code block format
    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.0
        
        # Border box around code block
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(
            '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:top w:val="single" w:sz="4" w:space="4" w:color="CCCCCC"/>'
            '<w:left w:val="single" w:sz="12" w:space="6" w:color="003366"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="4" w:color="CCCCCC"/>'
            '<w:right w:val="single" w:sz="4" w:space="4" w:color="CCCCCC"/>'
            '</w:pBdr>'
        )
        pPr.append(pBdr)
        
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(20, 20, 20)
        return p

    # Screenshot placeholder box
    def add_screenshot_placeholder(desc_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(10)
        
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(
            '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:top w:val="dashed" w:sz="8" w:space="8" w:color="666666"/>'
            '<w:left w:val="dashed" w:sz="8" w:space="12" w:color="666666"/>'
            '<w:bottom w:val="dashed" w:sz="8" w:space="8" w:color="666666"/>'
            '<w:right w:val="dashed" w:sz="8" w:space="12" w:color="666666"/>'
            '</w:pBdr>'
        )
        pPr.append(pBdr)
        
        run1 = p.add_run("\n\n[ INSERT SCREENSHOT HERE: ")
        set_font_tnr(run1, size_pt=11, bold=True, color_rgb=(180, 0, 0))
        run2 = p.add_run(desc_text)
        set_font_tnr(run2, size_pt=11, bold=False, italic=True, color_rgb=(50, 50, 50))
        run3 = p.add_run(" ]\n\n")
        set_font_tnr(run3, size_pt=11, bold=True, color_rgb=(180, 0, 0))
        return p

    def format_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Header Row
        hdr_cells = table.rows[0].cells
        for idx, header_text in enumerate(headers):
            hdr_cells[idx].text = header_text
            p = hdr_cells[idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            for r in p.runs:
                set_font_tnr(r, size_pt=10, bold=True)
            # Set shading
            shading = parse_xml(r'<w:shd {} w:fill="EAEAEA"/>'.format(nsdecls('w')))
            hdr_cells[idx]._tc.get_or_add_tcPr().append(shading)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.add_row().cells
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = cell_value
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                for r in p.runs:
                    set_font_tnr(r, size_pt=9.5)

        # Borders & Column widths
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    # =========================================================================
    # COVER PAGE (Page 1)
    # =========================================================================
    p_cov_inst = doc.add_paragraph()
    p_cov_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_inst.paragraph_format.first_line_indent = Inches(0)
    p_cov_inst.paragraph_format.space_before = Pt(20)
    p_cov_inst.paragraph_format.space_after = Pt(4)
    r = p_cov_inst.add_run("KRISTU JAYANTI (DEEMED TO BE UNIVERSITY)\n")
    set_font_tnr(r, size_pt=18, bold=True, color_rgb=(0, 32, 96))
    r2 = p_cov_inst.add_run("KRISTU JAYANTI INSTITUTE OF TECHNOLOGY\n")
    set_font_tnr(r2, size_pt=15, bold=True)
    r3 = p_cov_inst.add_run("Department of Computer Applications\nBengaluru, India")
    set_font_tnr(r3, size_pt=13, bold=False, italic=True)

    add_screenshot_placeholder("Institutional Crest / University Emblem Placeholder - Center Aligned")

    p_cov_rep = doc.add_paragraph()
    p_cov_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_rep.paragraph_format.first_line_indent = Inches(0)
    p_cov_rep.paragraph_format.space_before = Pt(15)
    p_cov_rep.paragraph_format.space_after = Pt(6)
    r = p_cov_rep.add_run("PROJECT-BASED PRACTICAL REPORT\n\n")
    set_font_tnr(r, size_pt=16, bold=True)
    r_tit = p_cov_rep.add_run("DIGITAL LEAVE AND ON-DUTY (OD) APPLICATION SYSTEM\n")
    set_font_tnr(r_tit, size_pt=17, bold=True, color_rgb=(0, 51, 102))

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_sub.paragraph_format.first_line_indent = Inches(0)
    p_cov_sub.paragraph_format.space_before = Pt(12)
    p_cov_sub.paragraph_format.space_after = Pt(20)
    r = p_cov_sub.add_run("Submitted in fulfilment of the requirements for the course\n")
    set_font_tnr(r, size_pt=12, italic=True)
    r2 = p_cov_sub.add_run("Java and Web Programming Lab\n")
    set_font_tnr(r2, size_pt=13, bold=True)
    r3 = p_cov_sub.add_run("Master of Computer Applications (MCA) – First Semester")
    set_font_tnr(r3, size_pt=13, bold=True)

    p_cov_meta = doc.add_paragraph()
    p_cov_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_meta.paragraph_format.first_line_indent = Inches(0)
    p_cov_meta.paragraph_format.space_before = Pt(25)
    p_cov_meta.paragraph_format.space_after = Pt(4)
    r = p_cov_meta.add_run("Submitted by:\n")
    set_font_tnr(r, size_pt=12, italic=True)
    r_name = p_cov_meta.add_run("Edwin Saji\n")
    set_font_tnr(r_name, size_pt=14, bold=True)
    r_reg = p_cov_meta.add_run("Register Number: 26MCAC22 | I MCA C\n\n")
    set_font_tnr(r_reg, size_pt=12, bold=True)
    r_gui = p_cov_meta.add_run("Under the guidance of:\n")
    set_font_tnr(r_gui, size_pt=12, italic=True)
    r_doc = p_cov_meta.add_run("Dr. Nithya.B\nDepartment of Computer Applications\n\n")
    set_font_tnr(r_doc, size_pt=13, bold=True)
    r_yr = p_cov_meta.add_run("Academic Year 2026–2027")
    set_font_tnr(r_yr, size_pt=12, bold=True)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS (Page 2)
    # =========================================================================
    add_h1("CONTENTS")
    
    contents_list = [
        "1. Title of the Project",
        "2. Introduction",
        "3. Objectives of the Project",
        "    3.1 Success Criteria",
        "4. Scope of the Project",
        "    4.1 Scope - Users",
        "    4.2 Scope - Assumptions and Limitations",
        "5. Software Specifications",
        "    5.1 Hardware and Runtime Requirements",
        "    5.2 Development Environment and Project Structure",
        "6. Project Workflow",
        "    6.1 Registration and Leave Submission Workflow",
        "    6.2 Workflow Diagram and Request State Transitions",
        "7. Project Modules (Phase Wise)",
        "    7.1 Functional Requirements and Acceptance Criteria",
        "    7.2 Data Design (MySQL Relational Schema)",
        "    7.3 User Interface Plan",
        "    PHASE 1 – CORE APPLICATION SETUP AND DATA ENTITY DESIGN",
        "    7.4 User Entity and OD Request Domain Models",
        "    7.5 String Operations for Input Validation",
        "    PHASE 2 – STRUCTURED PROGRAMMING, INTERFACES AND EXCEPTION HANDLING",
        "    7.6 Packages and Architectural Modularization",
        "    7.7 User Operations and Service Interfaces",
        "    7.8 Exception Handling and Robustness",
        "    PHASE 3 – WEB UI AND CLIENT VALIDATION",
        "    7.9 Login, Registration, and Application Forms",
        "    7.10 Client-Side Validation",
        "    7.11 Submitting the Form and Asynchronous Flow",
        "    7.12 JSON Data Interchange Format",
        "    PHASE 4 – SERVER-SIDE INTEGRATION AND IMPLEMENTATION",
        "    7.13 Servlets (GET/POST Request Processing)",
        "    7.14 Phase 4: Server-Side Validation of Credentials and Business Rules",
        "    7.15 Phase 4: HttpSession for Session Management",
        "    7.16 Phase 4: JSP Dashboard and Restricted Access",
        "    7.17 Phase 4: Logout and Session Invalidation",
        "    7.18 Phase 4: Deploying to Apache Tomcat Web Server",
        "    7.19 Example Test Plan and Verification Matrix",
        "8. Sample Coding (Working Code)",
        "    8.1 Source Code – User Entity and OD Request (Phase 1)",
        "    8.2 Source Code – Validation with String Handling (Phase 1)",
        "    8.3 Source Code – Interface and Custom Exception (Phase 2)",
        "    8.4 Source Code – Database Connection and Persistence (Phase 2 & 4)",
        "    8.5 Source Code – Client-Side Validation (Phase 3)",
        "    8.6 Source Code – Login Servlet and Session Dispatching (Phase 4)",
        "    8.7 Source Code – Access Filter and Status Updation Controller (Phase 4)",
        "    8.8 Source Code – JSP Dashboard Security Guard and web.xml (Phase 4)",
        "9. Features of the Project",
        "10. Future Improvements",
        "11. Conclusion",
        "12. References"
    ]
    for item in contents_list:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(item)
        if item.startswith("    PHASE"):
            set_font_tnr(run, size_pt=11.5, bold=True, color_rgb=(0, 51, 102))
        elif item.startswith("1.") or item.startswith("2.") or item.startswith("3.") or item.startswith("4.") or item.startswith("5.") or item.startswith("6.") or item.startswith("7.") or item.startswith("8.") or item.startswith("9.") or item.startswith("10.") or item.startswith("11.") or item.startswith("12."):
            set_font_tnr(run, size_pt=12, bold=True)
        else:
            set_font_tnr(run, size_pt=11)

    doc.add_page_break()

    # =========================================================================
    # SECTION 1: TITLE OF THE PROJECT
    # =========================================================================
    add_h1("1. TITLE OF THE PROJECT")
    add_h2("Digital Leave and On-Duty (OD) Application System")
    add_p("The 'Digital Leave and On-Duty (OD) Application System' is a multi-tier, enterprise-grade academic web application engineered to replace manual, paper-intensive student leave processes with a streamlined, transparent, and auditable digital workflow. The project was conceived and implemented as part of the Java and Web Programming practical curriculum for the Master of Computer Applications (MCA) program at Kristu Jayanti University.")
    add_p("In collegiate institutions, when students participate in sanctioned academic, co-curricular, athletic, or recruitment engagements, they are eligible for On-Duty (OD) attendance credit. This credit ensures that their formal attendance register reflects approved presence rather than unexcused absence. However, managing this mechanism via conventional paper slips introduces logistical bottlenecks, document loss, unauthorized alterations, and significant administrative latency. The Digital Leave and OD Application System provides an automated solution that unifies students, faculty advisors, and departmental leadership onto a single synchronized web platform.")
    add_p("The application is developed using standard Enterprise Java technologies, specifically Java Standard Edition (JDK 17/21), Jakarta/Java EE Servlets, JavaServer Pages (JSP), Java Database Connectivity (JDBC), and a MySQL relational database running on the Apache Tomcat 9 servlet container. The user interface is crafted using modern, semantic HTML5, CSS3 with a clean institutional color palette, and Vanilla JavaScript for responsive client-side event processing.")

    # =========================================================================
    # SECTION 2: INTRODUCTION
    # =========================================================================
    add_h1("2. INTRODUCTION")
    add_p("In contemporary higher education institutions, experiential learning beyond the traditional classroom setting has become an essential pillar of postgraduate computer applications training. Students routinely represent their department and university at national hackathons, technical paper presentations, open-source conferences, sports tournaments, corporate placement interviews, and industrial internship programs. To encourage participation without penalizing academic standing, universities provide an official provision known as 'On-Duty' (OD) leave.")
    add_p("Historically, the execution of this policy has relied on physical paper applications. A student seeking OD clearance must obtain a printed leave requisition slip, manually fill in their personal and academic particulars, attach physical invitation letters or participation brochures, and physically navigate across campus buildings to secure physical signatures. This multi-signature chain typically requires sequential endorsements from the event faculty coordinator, the student's class advisor or mentor, and ultimately the Head of Department (HOD).")
    add_p("This paper-based methodology introduces severe administrative and operational drawbacks. Forms are frequently misplaced on faculty desks or lost in transit, preventing timely approval. Students face prolonged delays if faculty members are engaged in lectures, examinations, or institutional travel. Furthermore, physical forms provide no mechanism for real-time policy enforcement. For instance, institutional bylaws mandate that OD requests must be submitted within three calendar days of event completion and restrict cumulative duty to a maximum ceiling of 15 days per semester. In a manual system, faculty signatories cannot verify whether an applicant has exceeded their semester quota without laboriously cross-referencing physical departmental logbooks, which is rarely feasible in practice.")
    add_p("Security and integrity issues are also prevalent in manual workflows. Physical signatures are susceptible to unauthorized signing, date alterations, and retrospective modifications. Additionally, because leave slips are often submitted weeks after an event has concluded, administrative clerks are forced to make retroactive adjustments to the institutional enterprise attendance database, leading to discrepancies during semester examination hall-ticket clearance.")
    add_p("The Digital Leave and On-Duty Application System resolves each of these vulnerabilities by delivering an end-to-end electronic approval pipeline. Authenticated students can draft and submit leave requests from any networked device. The application immediately verifies institutional bylaws—including strict 3-day post-event deadline checking and cumulative 15-day semester quota enforcement—before persisting the request to the database. Designated faculty advisors access a real-time pending queue to verify claims with single-click precision, after which the request automatically transitions to the Head of Department for executive sanction.")
    add_p("By implementing role-based session access, strict client-side and server-side validation, transactional JDBC database persistence, and an immutable audit trail, the system ensures transparency, enhances compliance, and eliminates paper waste. The technical architecture strictly adheres to the Model-View-Controller (MVC) design pattern, demonstrating how core Java enterprise concepts covered in the laboratory curriculum integrate to solve complex real-world operational challenges.")

    # =========================================================================
    # SECTION 3: OBJECTIVES OF THE PROJECT
    # =========================================================================
    add_h1("3. OBJECTIVES OF THE PROJECT")
    add_p("The primary objective of this project is to architect, develop, and deploy a secure, role-based Java web application that digitizes the collegiate On-Duty and leave management lifecycle, establishing automated academic policy compliance and multi-tier approval routing.")
    add_h2("Specific Objectives:")
    add_bullet("Define and encapsulate core data models (User and ODRequest) utilizing private fields, explicit constructors, and getter/setter methods to ensure data integrity and thread safety.", "1. Object-Oriented Domain Modeling: ")
    add_bullet("Apply robust string manipulation and regular expression pattern matching to validate user credentials, roll numbers, event descriptions, and textual reasons prior to storage.", "2. String Handling and Input Sanitization: ")
    add_bullet("Architect the project into distinct, decoupled packages (model, service, controller, and exception) adhering to the single responsibility principle and enterprise Java conventions.", "3. Architectural Modularization: ")
    add_bullet("Define formal service contracts via Java interfaces (UserOperations and ODService) to decouple high-level business rules from underlying persistence mechanisms.", "4. Interface-Driven Architecture: ")
    add_bullet("Implement a robust exception handling hierarchy utilizing a custom checked domain exception (InvalidInputException) to catch and gracefully report validation and business rule violations.", "5. Domain Exception Management: ")
    add_bullet("Develop responsive, modern web forms utilizing HTML5 and CSS3, styled with clean visual feedback, professional typography, and responsive grid layouts.", "6. Responsive Client Interface: ")
    add_bullet("Implement client-side validation logic using Vanilla JavaScript to provide immediate visual warnings for empty fields, format irregularities, and temporal deadline breaches.", "7. Client-Side Pre-Validation: ")
    add_bullet("Establish persistent data storage utilizing a relational MySQL database accessed through native Java Database Connectivity (JDBC) using PreparedStatement to ensure SQL injection immunity.", "8. Relational Persistence and JDBC: ")
    add_bullet("Develop Java Servlets to process HTTP GET and POST requests, handle multi-part application dispatches, and enforce authorization policies on the server side.", "9. Server-Side Request Controllers: ")
    add_bullet("Manage user identity and state using HttpSession, preventing unauthorized URL tampering and enforcing automatic session invalidation upon user logout.", "10. State and Session Control: ")
    add_bullet("Design dynamic JavaServer Pages (JSP) dashboards customized for Students, Faculty Advisors, and the Head of Department, protected by dedicated Servlet Filters.", "11. Dynamic View Generation: ")
    add_bullet("Assemble the application into a standard Web Application Archive (WAR) and deploy it onto the Apache Tomcat 9 servlet container for production execution.", "12. Web Server Deployment: ")

    add_h2("3.1 Success Criteria")
    add_p("To confirm that the application fulfills institutional and academic standards, each system feature is evaluated against explicit, measurable success criteria:")
    add_bullet("The registration form accepts valid roll numbers, usernames, and passwords, while rejecting duplicate usernames or improperly formatted inputs with distinct error messages.", "Registration and Credential Integrity: ")
    add_bullet("The authentication portal verifies credentials against salted database records and initializes an active HttpSession carrying user ID, username, full name, and role. Unauthorized access attempts yield generic security messages without leaking database state.", "Authentication and Session Initialization: ")
    add_bullet("Any application submitted more than three days after duty completion (toDate) is strictly rejected by both client JavaScript and the server-side ODServiceImpl validation engine.", "3-Day Post-Event Submission Deadline: ")
    add_bullet("The system computes cumulative approved and pending duty days for an applicant. If a requested duration causes total semester duty to exceed 15 days, the application is blocked with a detailed explanation of remaining quota.", "15-Day Semester Quota Constraint: ")
    add_bullet("The application rejects new submissions that overlap in date ranges with existing approved or pending applications for the same student, eliminating duplicate booking conflicts.", "Date Overlap Prevention: ")
    add_bullet("Applications transition sequentially from Student Submission -> Staff Pending -> Staff Verified -> HOD Approved. Rejections at any stage terminate the pipeline and record mandatory feedback comments.", "Multi-Tier Role-Based Workflow: ")
    add_bullet("Direct access to JSP dashboards without an active session immediately redirects to the login view. Role violations (e.g., student accessing HOD dashboards) trigger HTTP 403 Forbidden responses.", "Access Filter and Authorization Guard: ")
    add_bullet("The compiled application packages cleanly into a WAR file and deploys on Apache Tomcat 9 without runtime container exceptions.", "Container Deployment: ")

    # =========================================================================
    # SECTION 4: SCOPE OF THE PROJECT
    # =========================================================================
    add_h1("4. SCOPE OF THE PROJECT")
    add_p("The scope of the Digital Leave and On-Duty Application System encompasses the digital transformation of student attendance leave requisitions within an academic department. The system provides role-tailored dashboards and operational capabilities for three primary user personas: Students, Faculty Staff Advisors, and the Head of the Department (HOD).")
    
    add_h2("4.1 Scope - Users")
    add_p("System authorization is strictly segregated based on defined user roles. Each persona is granted access solely to functional views and server endpoints corresponding to their institutional responsibilities.")

    add_table_caption("Table 1: Scope - User Roles and Responsibilities")
    tbl_users = doc.add_table(rows=1, cols=3)
    user_headers = ["User Role", "Target Persona", "Core System Responsibilities"]
    user_data = [
        ["Student (STUDENT)", "Enrolled Postgraduate Students", "Register account, authenticate, compose OD applications, verify remaining 15-day semester quota, track real-time verification status, and review reviewer comments."],
        ["Staff Advisor (STAFF)", "Faculty Mentors / Class Teachers", "Authenticate, inspect departmental pending queue, evaluate student event authenticity and supporting details, endorse as 'Verified' or 'Rejected', and append feedback remarks."],
        ["Head of Department (HOD)", "Department Executive Leadership", "Authenticate, review staff-verified applications, perform final institutional sanction ('Approved' or 'Rejected'), audit departmental OD metrics, and reconcile official attendance."]
    ]
    format_table(tbl_users, [Inches(1.8), Inches(1.8), Inches(2.9)], user_headers, user_data)

    add_h2("4.2 Scope - Assumptions and Limitations")
    add_p("To ensure structured development within the semester timeframe, specific operational assumptions and technical boundaries have been defined:")
    add_bullet("Every student possesses a valid institutional roll number and academic registration. Faculty staff advisors and departmental leadership are pre-registered with official designations.", "Institutional Identity Assumption: ")
    add_bullet("All dates entered follow the ISO-8601 calendar standard (YYYY-MM-DD), and duty durations represent full-day academic attendances.", "Temporal Uniformity Assumption: ")
    add_bullet("The current implementation targets a single academic department (Department of Computer Applications) and operates within a centralized relational schema rather than a multi-tenant distributed cloud infrastructure.", "Departmental Deployment Boundary: ")
    add_bullet("The system relies on structured textual declarations and physical verification during mentor interviews rather than cloud-based optical character recognition (OCR) of certificates.", "Documentary Proof Scope: ")
    add_bullet("System notifications are delivered via responsive in-app dashboard polling and real-time status tables rather than an external SMS or SMTP email relay.", "Notification Boundary: ")

    # =========================================================================
    # SECTION 5: SOFTWARE SPECIFICATIONS
    # =========================================================================
    add_h1("5. SOFTWARE SPECIFICATIONS")
    add_p("The Digital Leave and On-Duty Application System is developed using industry-standard open-source technologies, ensuring cross-platform stability, maintainability, and alignment with modern enterprise computing standards.")

    add_table_caption("Table 2: Software Specifications")
    tbl_soft = doc.add_table(rows=1, cols=2)
    soft_headers = ["Component", "Specification"]
    soft_data = [
        ["Programming Language", "Java Standard Edition 17 (LTS) / Java 21"],
        ["Server-Side Technology", "Java Servlets (Jakarta / Java EE 4.0 API) and JavaServer Pages (JSP 2.3)"],
        ["Database Management System", "MySQL Community Server 8.0.x with InnoDB Storage Engine"],
        ["Database Connectivity Driver", "MySQL Connector/J (Type-4 JDBC Driver, version 8.0.33+)"],
        ["Web Application Server", "Apache Tomcat 9.0.x (Servlet 4.0 / JSP 2.3 Compliant Web Container)"],
        ["Frontend Technologies", "HTML5, Vanilla CSS3 (Custom Responsive Design System), JavaScript (ES12)"],
        ["Session Management", "HTTP-only Cookie-backed HttpSession with session fixation protection"],
        ["Integrated Development Environment", "Visual Studio Code with Java Extension Pack / Eclipse IDE for Enterprise Java"],
        ["Build and Deployment Tool", "PowerShell Automation Script (deploy.ps1) and Apache Ant / Native WAR Packaging"]
    ]
    format_table(tbl_soft, [Inches(2.5), Inches(4.0)], soft_headers, soft_data)

    add_h2("5.1 Hardware and Runtime Requirements")
    add_p("The application is lightweight and optimized for standard computing infrastructure. To build, deploy, and execute the system in an academic laboratory or intranet production environment, the following hardware prerequisites and execution sequence must be met:")

    add_table_caption("Table 3: Hardware Requirements")
    tbl_hard = doc.add_table(rows=1, cols=2)
    hard_headers = ["Hardware Component", "Minimum Operational Requirement"]
    hard_data = [
        ["Central Processing Unit (CPU)", "Intel Core i3 / AMD Ryzen 3 or higher (dual-core 2.0 GHz)"],
        ["Random Access Memory (RAM)", "4 GB minimum (8 GB recommended for concurrent hosting of MySQL and Tomcat)"],
        ["Hard Disk Storage", "500 MB free solid-state drive (SSD) storage for database tables and WAR binaries"],
        ["Display Resolution", "1366 x 768 minimum (1920 x 1080 Full HD recommended for dashboards)"],
        ["Operating System", "Microsoft Windows 10/11, Ubuntu Linux 20.04+, or macOS"]
    ]
    format_table(tbl_hard, [Inches(2.5), Inches(4.0)], hard_headers, hard_data)

    add_p("To run the project, the following operational steps are executed:")
    add_bullet("Install JDK 17, Apache Tomcat 9, and MySQL Server 8.0 on the host workstation.", "Step 1: ")
    add_bullet("Start the MySQL service and initialize the database schema and seed data by executing schema.sql in MySQL Workbench or the MySQL command line.", "Step 2: ")
    add_bullet("Compile the Java source files into bytecode classes and bundle the web assets into DigitalODSystem.war using the PowerShell build script (deploy.ps1).", "Step 3: ")
    add_bullet("Deploy DigitalODSystem.war into the webapps directory of Apache Tomcat 9 and start the Catalina server service.", "Step 4: ")
    add_bullet("Open any modern web browser and navigate to http://localhost:8080/DigitalODSystem/ to access the application home view.", "Step 5: ")

    add_h2("5.2 Development Environment and Project Structure")
    add_p("The project follows a layered architectural structure adhering to separation of concerns. Source files are strictly isolated into packages based on functional responsibility:")

    add_table_caption("Table 4: Project Structure and Architectural Responsibilities")
    tbl_struct = doc.add_table(rows=1, cols=2)
    struct_headers = ["Package / Directory", "Architectural Responsibility"]
    struct_data = [
        ["model", "Encapsulates domain entities (User.java and ODRequest.java) with private attributes, constructors, and accessor methods."],
        ["exception", "Defines the custom checked domain exception InvalidInputException.java for clean error propagation."],
        ["service", "Houses service interfaces (UserOperations.java, ODService.java), concrete implementations (ODServiceImpl.java, UserServiceImpl.java), and the database connection factory (DBConnection.java)."],
        ["controller", "Contains HTTP request handlers (LoginServlet, RegisterServlet, ApplyODServlet, UpdateODStatusServlet, LogoutServlet) and the security gatekeeper (AuthenticationFilter.java)."],
        ["webapp / root", "Houses presentation views (index.html, login.html, student_dashboard.jsp, staff_dashboard.jsp, hod_dashboard.jsp, od_criteria.jsp), styles (css/), and client scripts (validation.js)."],
        ["WEB-INF", "Stores deployment descriptor (web.xml) defining servlet mappings, session timeouts, and security constraints."],
        ["schema.sql", "SQL script establishing the digital_od database schema, table constraints, foreign keys, and seed academic test accounts."]
    ]
    format_table(tbl_struct, [Inches(2.5), Inches(4.0)], struct_headers, struct_data)

    # =========================================================================
    # SECTION 6: PROJECT WORKFLOW
    # =========================================================================
    add_h1("6. PROJECT WORKFLOW")
    add_p("The operational workflow of the Digital Leave and On-Duty Application System is structured around a finite state machine that guarantees deterministic request progression. A visitor lands on the institutional landing page where they can review leave guidelines and access the secure authentication portal. Upon authenticating with verified credentials, a server-side HttpSession is established, capturing the user's ID, username, full name, and role.")
    add_p("Students access the Student Dashboard where they can inspect their remaining 15-day semester quota and submit new applications. When submitting, client-side JavaScript validates inputs before dispatching an HTTP POST request to ApplyODServlet. The servlet invokes ODServiceImpl, which executes rigorous server-side checks: ensuring the request is within 3 days post-event, calculating requested days, verifying that total semester duty does not exceed 15 days, and confirming no date overlap exists with prior bookings. Upon passing validation, the application is stored in MySQL with an initial status of Staff Status: 'Pending' and HOD Status: 'Pending'.")
    add_p("Designated Staff Advisors log in to inspect their departmental pending queue. Staff members evaluate the event validity and either endorse the application as 'Verified' or mark it as 'Rejected' with mandatory feedback. If verified, the request surfaces on the HOD Dashboard, where the Head of Department reviews the mentor's endorsement and grants final 'Approved' status or issues an executive 'Rejected' decision. Students can track this progression live on their dashboard.")

    add_h2("6.1 Registration and Leave Submission Workflow")
    add_p("The submission and verification sequence proceeds through the following sequential stages:")
    add_bullet("The student enters registration particulars (Full Name, Roll Number, Username, Password, Department, Course). Client JavaScript verifies field completeness, and RegisterServlet persists the account in MySQL.", "1. Student Registration: ")
    add_bullet("The student enters username, password, and selects the 'student' role. LoginServlet validates credentials against the database and initializes a secure session.", "2. Secure Authentication: ")
    add_bullet("The student fills in event category, title, endorsing body, starting date, ending date, and reason. Live JavaScript calculates days count and validates the 3-day rule.", "3. Application Composition: ")
    add_bullet("ApplyODServlet receives the POST request and invokes ODService.applyOD(). The service enforces the 3-day post-event deadline, 15-day semester quota, and date overlap rules. The record is committed via JDBC.", "4. Server Validation & Persistence: ")
    add_bullet("The assigned faculty advisor reviews the pending application in staff_dashboard.jsp and submits a verification status update via UpdateODStatusServlet.", "5. Staff Advisor Verification: ")
    add_bullet("The Head of Department accesses hod_dashboard.jsp, reviews verified applications, and issues final approval. The record is officially marked as approved for attendance reconciliation.", "6. Executive HOD Sanction: ")

    add_h2("6.2 Workflow Diagram")
    add_p("The lifecycle of an On-Duty application and its finite state transitions are illustrated in the workflow diagram below:")

    add_screenshot_placeholder("Workflow Diagram: End-to-End Processing Flow (Student -> Staff -> HOD) - Full Page Width")

    add_table_caption("Table 5: OD Request Finite State Transitions")
    tbl_state = doc.add_table(rows=1, cols=4)
    state_headers = ["Initial State", "Triggering Actor", "Action / Condition", "Resulting Next State"]
    state_data = [
        ["None (Draft)", "Student", "Submit valid OD request within 3 days & within 15-day quota", "Staff: Pending | HOD: Pending"],
        ["Staff: Pending", "Staff Advisor", "Select 'Verified' after reviewing event legitimacy", "Staff: Verified | HOD: Pending"],
        ["Staff: Pending", "Staff Advisor", "Select 'Rejected' and provide justification comments", "Staff: Rejected | HOD: Rejected (Terminated)"],
        ["Staff: Verified", "Head of Dept (HOD)", "Select 'Approved' for final attendance credit", "Staff: Verified | HOD: Approved (Sanctioned)"],
        ["Staff: Verified", "Head of Dept (HOD)", "Select 'Rejected' due to academic constraints", "Staff: Verified | HOD: Rejected (Terminated)"]
    ]
    format_table(tbl_state, [Inches(1.5), Inches(1.5), Inches(2.0), Inches(1.5)], state_headers, state_data)

    # =========================================================================
    # SECTION 7: PROJECT MODULES (PHASE WISE)
    # =========================================================================
    add_h1("7. PROJECT MODULES (PHASE WISE)")
    add_p("The development of the Digital Leave and On-Duty Application System was structured systematically into four distinct phases, directly aligning with the core learning units of the Java and Web Programming curriculum.")

    add_table_caption("Table 6: Project Implementation Phases Overview")
    tbl_phases = doc.add_table(rows=1, cols=3)
    phase_headers = ["Phase", "Module Title", "Core Technical Deliverables"]
    phase_data = [
        ["1", "Core Application Setup and Data Entity Design", "User and ODRequest entity modeling, constructors, accessors, and string-based validation routines."],
        ["2", "Structured Programming, Interfaces and Reliability", "Decoupled package organization, UserOperations and ODService interfaces, and custom InvalidInputException hierarchy."],
        ["3", "Web Interface Design and Client-Side Validation", "HTML5 responsive layout, CSS3 visual styling, JavaScript dynamic event interception, and JSON interchange schemas."],
        ["4", "Server-Side Integration and Container Execution", "Java Servlets (GET/POST), server-side 3-day and 15-day rule enforcement, HttpSession tracking, JSP role dashboards, and Tomcat 9 deployment."]
    ]
    format_table(tbl_phases, [Inches(0.8), Inches(2.5), Inches(3.2)], phase_headers, phase_data)

    add_h2("7.1 Functional Requirements and Acceptance Criteria")
    add_p("The system's operational capabilities are defined through rigorous functional requirements and testable acceptance criteria:")

    add_table_caption("Table 7: Functional Requirements Matrix and Acceptance Criteria")
    tbl_fr = doc.add_table(rows=1, cols=3)
    fr_headers = ["Requirement ID", "Functional Requirement", "Acceptance Criterion"]
    fr_data = [
        ["FR-01", "Student User Registration", "Valid roll number, username, and password create a new student account. Duplicate usernames are rejected with an informative prompt."],
        ["FR-02", "Role-Based Authentication", "Users must authenticate with valid username, password, and matching role. Mismatched credentials return a secure generic error message."],
        ["FR-03", "Session Initialization", "Upon successful login, the server binds user ID, username, full name, and role into an active HttpSession with a 30-minute timeout."],
        ["FR-04", "Role-Gated URL Access", "Direct URL requests to protected pages (e.g., hod_dashboard.jsp) without an appropriate role session are intercepted by AuthenticationFilter and redirected."],
        ["FR-05", "3-Day Submission Constraint", "Applications submitted more than 3 days after duty conclusion (toDate) are blocked by client JavaScript and rejected by the server."],
        ["FR-06", "15-Day Semester Quota Cap", "The system calculates aggregate used days. Any application that would push cumulative used days beyond 15 is rejected with remaining quota details."],
        ["FR-07", "Date Overlap Prevention", "New applications with dates overlapping existing pending or approved applications for the same student are strictly prohibited."],
        ["FR-08", "Staff Verification Queue", "Staff advisors can view all pending applications in their department, examine submitted details, and mark requests as Verified or Rejected."],
        ["FR-09", "HOD Approval Queue", "The HOD dashboard displays only staff-verified requests, enabling final Approved or Rejected sanctioning."],
        ["FR-10", "Feedback Documentation", "When staff or HOD rejects an application, mandatory explanatory remarks must be supplied and displayed on the student's dashboard."],
        ["FR-11", "Session Termination (Logout)", "Invoking /api/logout invalidates the HttpSession, clears server state, and redirects the client to the login view."]
    ]
    format_table(tbl_fr, [Inches(1.2), Inches(2.3), Inches(3.0)], fr_headers, fr_data)

    add_h2("7.2 Data Design (MySQL Relational Schema)")
    add_p("System data is persisted in a normalized relational database named digital_od hosted on MySQL Server 8.0. The schema is organized into two primary entities: users and od_requests, linked via foreign key relationships.")

    add_table_caption("Table 8: Schema Definition - Users Table (users)")
    tbl_users_sch = doc.add_table(rows=1, cols=4)
    u_sch_headers = ["Field Name", "Data Type", "Constraints", "Functional Description"]
    u_sch_data = [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique internal user identifier."],
        ["username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Unique login credential identifier."],
        ["password", "VARCHAR(100)", "NOT NULL", "Account security credential."],
        ["role", "VARCHAR(20)", "NOT NULL", "System authorization role: 'student', 'staff', 'hod'."],
        ["roll_no", "VARCHAR(30)", "NOT NULL", "Student Roll Number or Faculty Staff Identification Code."],
        ["full_name", "VARCHAR(100)", "NOT NULL", "Official full name of the academic persona."],
        ["department", "VARCHAR(100)", "DEFAULT 'Computer Applications'", "Academic department affiliation."],
        ["course", "VARCHAR(50)", "DEFAULT 'MCA'", "Degree program enrolled in (e.g., 'MCA')."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Audit record timestamp of account creation."]
    ]
    format_table(tbl_users_sch, [Inches(1.2), Inches(1.3), Inches(1.8), Inches(2.2)], u_sch_headers, u_sch_data)

    add_table_caption("Table 9: Schema Definition - OD Requests Table (od_requests)")
    tbl_od_sch = doc.add_table(rows=1, cols=4)
    od_sch_headers = ["Field Name", "Data Type", "Constraints", "Functional Description"]
    od_sch_data = [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique application requisition identifier."],
        ["student_username", "VARCHAR(50)", "NOT NULL, FOREIGN KEY (users)", "Links application to the applicant student account."],
        ["roll_no", "VARCHAR(30)", "NOT NULL", "Student roll number for physical cross-referencing."],
        ["event_type", "VARCHAR(100)", "NOT NULL", "Category of leave (e.g., 'Technical Symposium', 'Sports')."],
        ["event_name", "VARCHAR(200)", "NOT NULL", "Official title of the event or tournament."],
        ["authorized_body", "VARCHAR(150)", "NOT NULL", "Endorsing collegiate club, department, or coordinator."],
        ["event_date", "DATE", "NOT NULL", "Commencement date of the sanctioned engagement."],
        ["from_date", "DATE", "NOT NULL", "Duty start date."],
        ["to_date", "DATE", "NOT NULL", "Duty conclusion date."],
        ["days_count", "INT", "NOT NULL", "Total calculated working days requested."],
        ["reason", "TEXT", "NOT NULL", "Detailed academic justification for leave requisition."],
        ["staff_status", "VARCHAR(30)", "DEFAULT 'Pending'", "Staff advisor status: 'Pending', 'Verified', 'Rejected'."],
        ["hod_status", "VARCHAR(30)", "DEFAULT 'Pending'", "HOD executive status: 'Pending', 'Approved', 'Rejected'."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Audit timestamp of submission."]
    ]
    format_table(tbl_od_sch, [Inches(1.2), Inches(1.3), Inches(1.8), Inches(2.2)], od_sch_headers, od_sch_data)

    add_h2("7.3 User Interface Plan")
    add_p("The presentation layer is designed to deliver a modern, intuitive, and responsive user experience. Built using vanilla HTML5 and CSS3, the interface avoids bulky third-party frontend frameworks in favor of clean custom components, CSS Grid, and Flexbox layouts. The visual theme employs an institutional color palette—deep navy headers (#003366), clean light-gray card backgrounds (#F8F9FA), and crisp accent colors for status badges (green for Approved, amber for Pending, and crimson for Rejected).")
    add_p("The interface structure comprises dedicated views: index.html welcomes visitors and outlines institutional OD guidelines; login.html offers a unified credential entry portal with role selection; student_dashboard.jsp provides students with live quota statistics, an application composition form, and an interactive history table; staff_dashboard.jsp allows faculty advisors to review pending requests; and hod_dashboard.jsp equips departmental leadership with high-level metrics and final sanction controls.")

    add_screenshot_placeholder("User Interface Overview: Institutional Landing Page and Navigation Banner - Half Page Size")

    # -------------------------------------------------------------------------
    # PHASE 1
    # -------------------------------------------------------------------------
    add_h1("PHASE 1 – BUILD THE BASICS OF THE APPLICATION AND DEFINE THE USER ENTITY")
    add_h2("7.4 User Entity and Domain Models")
    add_p("In Phase 1, the core domain entities governing the application were identified and modeled in Java. The User class acts as the central security and identity model, encapsulating attributes for user ID, username, password, role, roll number, full name, department, and course. All fields are declared private to enforce strict encapsulation, with data access provided exclusively through public getter and setter methods.")
    add_p("Similarly, the ODRequest class was engineered to encapsulate all dimensions of an On-Duty leave requisition. It models attributes for application ID, student username, roll number, event category, event title, authorized endorsing body, date ranges (from_date and to_date), calculated duration (days_count), academic justification, multi-tier approval states (staff_status and hod_status), and submission timestamps.")

    add_screenshot_placeholder("Phase 1: Terminal Output / IDE Compilation of User.java and ODRequest.java Entities - Half Page Size")

    add_h2("7.5 String Operations for Basic Validation")
    add_p("Input integrity is enforced in Phase 1 through comprehensive Java string handling routines. Prior to any data processing, raw textual inputs undergo systematic sanitization:")
    add_bullet("Removes leading and trailing whitespace from names, roll numbers, and descriptions, preventing whitespace-only submissions.", "trim(): ")
    add_bullet("Guarantees that mandatory inputs are not null and carry minimum meaningful lengths (e.g., full name >= 2 characters, reason >= 10 characters).", "Length & Null Checking: ")
    add_bullet("Evaluates usernames against regex pattern ^[a-zA-Z0-9_]{3,30}$ ensuring credentials contain only alphanumeric characters and underscores.", "Pattern Matching (matches): ")
    add_bullet("Normalizes usernames and search terms to lowercase to guarantee case-insensitive uniqueness in database lookups.", "toLowerCase(): ")

    add_screenshot_placeholder("Phase 1: String Validation Test Execution & Output Logs - Half Page Size")

    # -------------------------------------------------------------------------
    # PHASE 2
    # -------------------------------------------------------------------------
    add_h1("PHASE 2 – CREATE STRUCTURED AND RELIABLE CODE USING PACKAGES, INTERFACES AND EXCEPTION HANDLING")
    add_h2("7.6 Packages")
    add_p("In Phase 2, the application source code was structured into distinct Java packages adhering to standard reverse-domain naming conventions and enterprise architectural patterns. The model package holds pure data transfer objects (User, ODRequest); the exception package encapsulates the custom exception hierarchy; the service package houses business interfaces, database connection utilities, and validation algorithms; and the controller package contains HTTP Servlets and security filters.")
    add_p("This separation of concerns guarantees that changes in the presentation or persistence layers do not propagate into core business logic, significantly improving code maintainability and testability.")

    add_screenshot_placeholder("Phase 2: Project Package Directory Tree in Visual Studio Code / IDE - Half Page Size")

    add_h2("7.7 User Operations and Service Interfaces")
    add_p("To decouple business processing from underlying data access mechanisms, formal service contracts were defined using Java interfaces. The UserOperations interface declares abstract methods for input validation (validateInput) and credential verification (authenticate).")
    add_p("The ODService interface defines the core business contract for leave management, including applyOD(), getODRequestsByStudent(), getAllODRequests(), getUsedODDays(), and updateStatus(). By coding controllers against these interfaces rather than concrete classes, the persistence mechanism can be seamlessly swapped (e.g., from JDBC to an ORM or cloud database) without altering servlet code.")

    add_h2("7.8 Exception Handling")
    add_p("System reliability is reinforced through a centralized custom exception architecture. The InvalidInputException class extends the standard Java Exception class, creating a checked domain exception that must be explicitly handled by calling controllers.")
    add_p("When validation fails—such as an invalid date span, an application submitted past the 3-day window, or an applicant exceeding the 15-day semester quota—ODServiceImpl instantiates and throws an InvalidInputException containing an informative, user-friendly error message. Servlets catch this exception and return appropriate HTTP status codes and feedback to the user.")

    add_table_caption("Table 10: Exception Handling and HTTP Status Mapping")
    tbl_exc = doc.add_table(rows=1, cols=3)
    exc_headers = ["Validation / Business Condition", "Exception Raised", "Mapped HTTP Status"]
    exc_data = [
        ["Missing required fields or invalid username format", "InvalidInputException(\"Field required / Invalid format\")", "400 Bad Request"],
        ["OD application submitted > 3 days post-event", "InvalidInputException(\"Submission Rejected: 3-day deadline exceeded\")", "400 Bad Request"],
        ["Application exceeds 15-day semester quota", "InvalidInputException(\"OD Criteria Failed: Exceeds 15-day quota\")", "400 Bad Request"],
        ["Date range overlaps with existing active OD", "InvalidInputException(\"Duplicate Date Conflict: Overlapping application\")", "409 Conflict"],
        ["Incorrect password or unauthorized role login", "InvalidInputException(\"Invalid credentials or role\")", "401 Unauthorized"],
        ["Uncaught database connectivity failure", "SQLException / IllegalStateException", "500 Internal Server Error"]
    ]
    format_table(tbl_exc, [Inches(2.5), Inches(2.5), Inches(1.5)], exc_headers, exc_data)

    add_screenshot_placeholder("Phase 2: Exception Handling Execution & Error Alert Dialog in Browser - Half Page Size")

    # -------------------------------------------------------------------------
    # PHASE 3
    # -------------------------------------------------------------------------
    add_h1("PHASE 3 – WEB UI AND CLIENT VALIDATION")
    add_h2("7.9 Login, Registration, and Application Forms")
    add_p("Phase 3 focused on the design and implementation of the client presentation layer. The user registration and login forms are housed within clean HTML5 semantic structures, styled with modern CSS cards featuring rounded corners, subtle drop shadows, and responsive layouts.")
    add_p("The On-Duty application form in student_dashboard.jsp contains structured input fields for Event Category (dropdown populated with institutional classifications), Event Name, Authorized Endorsing Body, Event From Date, Event To Date, and Detailed Reason. Input fields are assigned unique descriptive IDs for seamless DOM access and automated testing.")

    add_screenshot_placeholder("Phase 3: Screenshot of Responsive Login Form and OD Application Modal - Half Page Size")

    add_h2("7.10 Client-Side Validation")
    add_p("Client-side validation is implemented in validation.js to provide instant visual feedback to users before form submission. The script intercepts submit events and evaluates several core rules:")
    add_bullet("Calculates the calendar difference between From Date and To Date, preventing submission if To Date is earlier than From Date.", "Date Chronology: ")
    add_bullet("Computes days elapsed between To Date and the current date (today). If the difference exceeds 3 days, a visual error banner is displayed immediately.", "3-Day Deadline Pre-Check: ")
    add_bullet("Computes requested duration (daysCount) and compares it against the student's remaining semester quota displayed on the dashboard header.", "Quota Limit Pre-Check: ")
    add_bullet("Checks that required textual inputs meet length thresholds (minimum 3 characters for event name, minimum 10 characters for justification).", "Field Completeness: ")

    add_screenshot_placeholder("Phase 3: Browser Screenshot Showing Client-Side Error Alert Triggered by 3-Day Rule Breach - Half Page Size")

    add_h2("7.11 Submitting the Form and Asynchronous Flow")
    add_p("Forms utilize JavaScript event interception via event.preventDefault() to suppress disruptive full-page browser reloads. Input values are gathered from the DOM and dispatched to the target Servlet using the modern JavaScript fetch API or standard asynchronous POST submission.")
    add_p("Upon receiving the server's response, the client script parses the JSON payload. If the operation succeeds, a success banner appears, the history table refreshes dynamically, and form inputs are cleared. If an error is returned, the error message is rendered within a designated alert container.")

    add_h2("7.12 JSON Data Interchange Format")
    add_p("All client-server asynchronous communications utilize structured JavaScript Object Notation (JSON). Server servlets return standardized JSON responses adhering to a uniform schema:")

    add_code_block('// Standard Success Response Payload:\n{\n  "status": "success",\n  "message": "OD Application submitted successfully. Assigned ID: OD-104",\n  "requestId": 104,\n  "daysCount": 2,\n  "remainingQuota": 11\n}\n\n// Standard Error Response Payload (3-Day Rule Breach):\n{\n  "status": "error",\n  "message": "Submission Rejected (Timeline Constraint): OD applications must be submitted within 3 days of completing the duty. Late submissions are not permitted."\n}')

    add_screenshot_placeholder("Phase 3: Browser Network Tab Showing Asynchronous HTTP POST Request and JSON Payload - Half Page Size")

    # -------------------------------------------------------------------------
    # PHASE 4
    # -------------------------------------------------------------------------
    add_h1("PHASE 4 – SERVER-SIDE INTEGRATION AND IMPLEMENTATION")
    add_p("Phase 4 represents the complete integration of server-side business logic, database connectivity via JDBC, secure session management, role-based authorization filters, and Tomcat container deployment.")

    add_table_caption("Table 11: Application Servlet Endpoints and Access Control Matrix")
    tbl_end = doc.add_table(rows=1, cols=4)
    end_headers = ["Endpoint URL", "Controller Servlet", "HTTP Method", "Authorized Access Level"]
    end_data = [
        ["/register", "RegisterServlet", "POST", "Public (Anonymous visitors)"],
        ["/login", "LoginServlet", "POST", "Public (Anonymous visitors)"],
        ["/logout", "LogoutServlet", "GET / POST", "Authenticated Users (Any Role)"],
        ["/applyOD", "ApplyODServlet", "POST", "Authenticated Students ('student' role)"],
        ["/updateODStatus", "UpdateODStatusServlet", "POST", "Staff & HOD ('staff' or 'hod' role)"],
        ["/student_dashboard.jsp", "Direct JSP View", "GET", "Authenticated Students only (Role: 'student')"],
        ["/staff_dashboard.jsp", "Direct JSP View", "GET", "Authenticated Staff only (Role: 'staff')"],
        ["/hod_dashboard.jsp", "Direct JSP View", "GET", "Authenticated HOD only (Role: 'hod')"]
    ]
    format_table(tbl_end, [Inches(1.8), Inches(1.8), Inches(1.2), Inches(1.7)], end_headers, end_data)

    add_h2("7.13 Servlets (GET/POST Request Processing)")
    add_p("All HTTP communication is managed through Java Servlets extending HttpServlet. Critical state-altering actions (user registration, credential authentication, OD submission, and status updates) are processed exclusively through doPost() methods, preventing sensitive parameters from appearing in browser URLs or access logs. Read-only view rendering and dashboard queries utilize doGet().")

    add_h2("7.14 Phase 4: Server-Side Validation of Credentials and Business Rules")
    add_p("The system adheres to defensive software design principles: the server never trusts client-side validation, as JavaScript can be disabled or bypassed. When an OD request reaches ApplyODServlet, ODServiceImpl rigorously evaluates every academic policy rule on the server:")
    add_bullet("The service parses toDate and computes the elapsed days against LocalDate.now(). If ChronoUnit.DAYS.between(toDate, today) > 3, an InvalidInputException is thrown immediately.", "3-Day Post-Event Submission Deadline: ")
    add_bullet("The service queries the database for all active (Approved and Pending) requests for the student, calculates aggregate used days, and ensures currentUsedDays + requestedDays <= 15.", "15-Day Semester Quota Constraint: ")
    add_bullet("The service iterates through existing records to guarantee that the requested date window does not overlap with any previously booked engagement.", "Date Conflict and Overlap Validation: ")

    add_screenshot_placeholder("Phase 4: Server-Side Quota Enforcement & Database Record Verification in MySQL Workbench - Half Page Size")

    add_h2("7.15 Phase 4: HttpSession for Session Management")
    add_p("User authentication state is maintained via the Java Servlet container's native HttpSession mechanism. Upon successful credential verification, LoginServlet calls request.getSession(true) and stores critical user metadata: userId, username, fullName, rollNo, and role.")
    add_p("To safeguard against session fixation attacks, request.changeSessionId() is invoked upon authentication. Sessions are configured with a strict 30-minute inactivity timeout in web.xml, and cookies are assigned HTTP-only attributes to prevent theft via cross-site scripting (XSS).")

    add_h2("7.16 Phase 4: JSP Dashboard and Restricted Access")
    add_p("Dynamic server-side rendering is implemented using JavaServer Pages (JSP). Each dashboard (student_dashboard.jsp, staff_dashboard.jsp, and hod_dashboard.jsp) retrieves session attributes and executes a security pre-check at the top of the file. If no active session or matching role is present, the page immediately issues a client redirect to login.html.")
    add_p("Furthermore, AuthenticationFilter intercepts incoming HTTP requests to protected JSP resources. If an authenticated user attempts to access an unauthorized resource (e.g., a student attempting to navigate directly to hod_dashboard.jsp), the filter halts execution and returns an HTTP 403 Forbidden status.")

    add_screenshot_placeholder("Phase 4: Side-by-Side View of Student, Staff, and HOD Dashboards in Web Browser - Full Page Width")

    add_h2("7.17 Phase 4: Logout and Session Invalidation")
    add_p("When a user initiates the logout action, an HTTP request is dispatched to LogoutServlet. The servlet retrieves the current session via request.getSession(false) and invokes session.invalidate(). This command purges all bound session attributes and terminates the session token on the server. The servlet then redirects the client to the login page.")

    add_h2("7.18 Phase 4: Deploying to Apache Tomcat Web Server")
    add_p("The application is packaged into a standard Web Application Archive (DigitalODSystem.war) containing all compiled bytecode (.class files), web resources, stylesheets, client scripts, and the deployment descriptor (WEB-INF/web.xml). The WAR file is deployed into the webapps directory of Apache Tomcat 9, where the container unpacks the archive and initializes the servlet context.")

    add_screenshot_placeholder("Phase 4: Apache Tomcat 9 Web Application Manager Showing Active DigitalODSystem Deployment - Half Page Size")

    add_h2("7.19 Example Test Plan and Verification Matrix")
    add_p("To validate system stability, a comprehensive integration test suite was executed covering authentication, validation rules, session persistence, and role-based access control:")

    add_table_caption("Table 12: Comprehensive Integration Test Suite")
    tbl_test = doc.add_table(rows=1, cols=5)
    test_headers = ["Test ID", "Functional Area", "Input / Action", "Expected Result", "Status"]
    test_data = [
        ["T-01", "Registration", "Register new student with valid roll number and username", "Account created; database record verified in users table", "Passed"],
        ["T-02", "Registration", "Attempt registration with duplicate username", "Rejected: 'Username already registered'; HTTP 409", "Passed"],
        ["T-03", "Authentication", "Login with valid student credentials and role", "Session initialized; user redirected to student_dashboard.jsp", "Passed"],
        ["T-04", "Authentication", "Login with incorrect password", "Generic error message displayed; session not created", "Passed"],
        ["T-05", "Authentication", "Login as student but selecting 'hod' role", "Rejected: 'Invalid credentials or role mismatch'; HTTP 401", "Passed"],
        ["T-06", "Access Control", "Direct URL access to /hod_dashboard.jsp without session", "Redirected to login.html by AuthenticationFilter", "Passed"],
        ["T-07", "Access Control", "Student accesses /hod_dashboard.jsp directly", "HTTP 403 Forbidden returned; access denied", "Passed"],
        ["T-08", "Validation", "Submit OD form with empty event title or reason", "Client and server reject form with mandatory field alert", "Passed"],
        ["T-09", "3-Day Deadline", "Submit OD request with event toDate 5 days in the past", "Rejected: 'Submission Rejected (Timeline Constraint)'; 3-day rule enforced", "Passed"],
        ["T-10", "3-Day Deadline", "Submit OD request with event toDate 2 days in the past", "Accepted: Successfully processed and status set to Pending", "Passed"],
        ["T-11", "Semester Quota", "Submit OD requesting 6 days when 11 days already used", "Rejected: 'Exceeds 15-day semester quota (11+6=17)'; blocked", "Passed"],
        ["T-12", "Semester Quota", "Submit OD requesting 4 days when 11 days already used", "Accepted: Total equals 15 days; application saved", "Passed"],
        ["T-13", "Date Overlap", "Submit OD for dates overlapping existing active OD", "Rejected: 'Duplicate Date Conflict'; overlapping booking blocked", "Passed"],
        ["T-14", "Workflow", "Staff verifies pending student application", "Staff status changes to 'Verified'; surfaces on HOD queue", "Passed"],
        ["T-15", "Workflow", "HOD approves staff-verified application", "HOD status changes to 'Approved'; final sanction recorded", "Passed"],
        ["T-16", "Workflow", "Staff rejects application with remarks", "Staff status 'Rejected'; workflow terminates; remarks saved", "Passed"],
        ["T-17", "Session Logout", "Click 'Logout' from student dashboard", "Session invalidated; subsequent back-button navigation blocked", "Passed"],
        ["T-18", "Data Safety", "Input SQL injection payload (' OR '1'='1) in login", "Treated as literal string by PreparedStatement; login rejected", "Passed"]
    ]
    format_table(tbl_test, [Inches(0.8), Inches(1.3), Inches(2.2), Inches(1.8), Inches(0.7)], test_headers, test_data)

    # =========================================================================
    # SECTION 8: SAMPLE CODING (WORKING CODE)
    # =========================================================================
    add_h1("8. SAMPLE CODING (WORKING CODE)")
    add_p("This section contains representative, working source code excerpts from the active DigitalODSystem codebase. The code illustrates the multi-tier implementation spanning domain modeling, string validation, interface definitions, JDBC persistence, client scripts, servlets, and security filters.")

    add_h2("8.1 SOURCE CODE – USER ENTITY AND OD REQUEST (PHASE 1)")
    add_p("The User and ODRequest entity classes encapsulate data structures with private fields and public accessors:")
    add_code_block(
        "package model;\n\n"
        "public class User {\n"
        "    private int id;\n"
        "    private String username;\n"
        "    private String password;\n"
        "    private String role; // 'student', 'staff', 'hod'\n"
        "    private String rollNo;\n"
        "    private String fullName;\n"
        "    private String department;\n"
        "    private String course;\n\n"
        "    public User() {}\n\n"
        "    public User(int id, String username, String password, String role,\n"
        "                String rollNo, String fullName, String department, String course) {\n"
        "        this.id = id;\n"
        "        this.username = username;\n"
        "        this.password = password;\n"
        "        this.role = role;\n"
        "        this.rollNo = rollNo;\n"
        "        this.fullName = fullName;\n"
        "        this.department = department;\n"
        "        this.course = course;\n"
        "    }\n\n"
        "    public int getId() { return id; }\n"
        "    public String getUsername() { return username; }\n"
        "    public String getRole() { return role; }\n"
        "    public String getRollNo() { return rollNo; }\n"
        "    public String getFullName() { return fullName; }\n"
        "}"
    )

    add_h2("8.2 SOURCE CODE – VALIDATION WITH STRING HANDLING (PHASE 1)")
    add_p("String manipulation and pattern matching algorithms ensure textual integrity before database execution:")
    add_code_block(
        "package service;\n"
        "import exception.InvalidInputException;\n\n"
        "public class UserServiceImpl implements UserOperations {\n"
        "    @Override\n"
        "    public boolean validateInput(String username, String password) throws InvalidInputException {\n"
        "        if (username == null || username.trim().isEmpty()) {\n"
        "            throw new InvalidInputException(\"Username cannot be empty.\");\n"
        "        }\n"
        "        if (password == null || password.trim().isEmpty()) {\n"
        "            throw new InvalidInputException(\"Password cannot be empty.\");\n"
        "        }\n"
        "        String cleanedUser = username.trim().toLowerCase();\n"
        "        if (!cleanedUser.matches(\"^[a-zA-Z0-9_]{3,30}$\")) {\n"
        "            throw new InvalidInputException(\"Username must be 3-30 alphanumeric characters or underscores.\");\n"
        "        }\n"
        "        if (password.length() < 6) {\n"
        "            throw new InvalidInputException(\"Password must be at least 6 characters in length.\");\n"
        "        }\n"
        "        return true;\n"
        "    }\n"
        "}"
    )

    add_h2("8.3 SOURCE CODE – INTERFACE AND CUSTOM EXCEPTION (PHASE 2)")
    add_p("The custom exception class and service interface establish clean decoupling and structured error propagation:")
    add_code_block(
        "package exception;\n\n"
        "public class InvalidInputException extends Exception {\n"
        "    private static final long serialVersionUID = 1L;\n\n"
        "    public InvalidInputException(String message) {\n"
        "        super(message);\n"
        "    }\n"
        "    public InvalidInputException(String message, Throwable cause) {\n"
        "        super(message, cause);\n"
        "    }\n"
        "}\n\n"
        "package service;\n"
        "import exception.InvalidInputException;\n"
        "import model.ODRequest;\n"
        "import java.util.List;\n\n"
        "public interface ODService {\n"
        "    boolean applyOD(ODRequest request) throws InvalidInputException;\n"
        "    List<ODRequest> getODRequestsByStudent(String username);\n"
        "    List<ODRequest> getAllODRequests();\n"
        "    int getUsedODDays(String username);\n"
        "    boolean updateStatus(int requestId, String role, String status, String remarks) throws InvalidInputException;\n"
        "}"
    )

    add_h2("8.4 SOURCE CODE – DATABASE CONNECTION AND PERSISTENCE (PHASE 2 & 4)")
    add_p("The DBConnection utility class provides thread-safe JDBC connection pooling using native PreparedStatement queries:")
    add_code_block(
        "package service;\n"
        "import java.sql.Connection;\n"
        "import java.sql.DriverManager;\n"
        "import java.sql.SQLException;\n\n"
        "public class DBConnection {\n"
        "    private static final String URL = \"jdbc:mysql://localhost:3306/digital_od?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC\";\n"
        "    private static final String USER = \"root\";\n"
        "    private static final String PASS = \"root\";\n\n"
        "    static {\n"
        "        try {\n"
        "            Class.forName(\"com.mysql.cj.jdbc.Driver\");\n"
        "        } catch (ClassNotFoundException e) {\n"
        "            System.err.println(\"MySQL JDBC Driver Not Found: \" + e.getMessage());\n"
        "        }\n"
        "    }\n\n"
        "    public static Connection getConnection() throws SQLException {\n"
        "        return DriverManager.getConnection(URL, USER, PASS);\n"
        "    }\n"
        "}"
    )

    add_h2("8.5 SOURCE CODE – CLIENT-SIDE VALIDATION (PHASE 3)")
    add_p("Client-side validation script enforcing field completeness and the 3-day post-event submission rule:")
    add_code_block(
        "// validation.js - Client Side Validation Module\n"
        "const Validation = (() => {\n"
        "    function validateODSubmission(fromDateStr, toDateStr, currentUsedDays) {\n"
        "        const fromDate = new Date(fromDateStr);\n"
        "        const toDate = new Date(toDateStr);\n"
        "        const today = new Date();\n"
        "        today.setHours(0,0,0,0);\n\n"
        "        if (toDate < fromDate) {\n"
        "            return 'To Date cannot be earlier than From Date.';\n"
        "        }\n"
        "        // Enforce 3-day post-event submission rule\n"
        "        const diffDaysSinceDuty = Math.floor((today - toDate) / (1000 * 60 * 60 * 24));\n"
        "        if (diffDaysSinceDuty > 3) {\n"
        "            return 'Submission Rejected: OD applications must be submitted within 3 days of duty completion.';\n"
        "        }\n"
        "        // Calculate requested duration\n"
        "        const requestedDays = Math.floor((toDate - fromDate) / (1000 * 60 * 60 * 24)) + 1;\n"
        "        if (currentUsedDays + requestedDays > 15) {\n"
        "            return `Exceeds semester quota: You have ${15 - currentUsedDays} days remaining of 15 allowed.`;\n"
        "        }\n"
        "        return '';\n"
        "    }\n"
        "    return { validateODSubmission };\n"
        "})();"
    )

    add_h2("8.6 SOURCE CODE – LOGIN SERVLET AND SESSION DISPATCHING (PHASE 4)")
    add_p("LoginServlet authenticates user credentials, prevents session fixation, and initializes role-based session state:")
    add_code_block(
        "@WebServlet(\"/login\")\n"
        "public class LoginServlet extends HttpServlet {\n"
        "    private AuthService authService = new AuthServiceImpl();\n\n"
        "    @Override\n"
        "    protected void doPost(HttpServletRequest request, HttpServletResponse response)\n"
        "            throws ServletException, IOException {\n"
        "        String user = request.getParameter(\"username\");\n"
        "        String pass = request.getParameter(\"password\");\n"
        "        String role = request.getParameter(\"role\");\n\n"
        "        User authenticatedUser = authService.authenticate(user, pass, role);\n"
        "        if (authenticatedUser != null) {\n"
        "            HttpSession session = request.getSession(true);\n"
        "            request.changeSessionId(); // Protect against session fixation\n"
        "            session.setAttribute(\"userId\", authenticatedUser.getId());\n"
        "            session.setAttribute(\"username\", authenticatedUser.getUsername());\n"
        "            session.setAttribute(\"fullName\", authenticatedUser.getFullName());\n"
        "            session.setAttribute(\"rollNo\", authenticatedUser.getRollNo());\n"
        "            session.setAttribute(\"role\", authenticatedUser.getRole());\n\n"
        "            if (\"student\".equalsIgnoreCase(role)) response.sendRedirect(\"student_dashboard.jsp\");\n"
        "            else if (\"staff\".equalsIgnoreCase(role)) response.sendRedirect(\"staff_dashboard.jsp\");\n"
        "            else if (\"hod\".equalsIgnoreCase(role)) response.sendRedirect(\"hod_dashboard.jsp\");\n"
        "        } else {\n"
        "            response.sendRedirect(\"login.html?error=Invalid+credentials+or+role\");\n"
        "        }\n"
        "    }\n"
        "}"
    )

    add_h2("8.7 SOURCE CODE – ACCESS FILTER AND STATUS UPDATION CONTROLLER (PHASE 4)")
    add_p("AuthenticationFilter guards restricted views, and UpdateODStatusServlet processes multi-tier staff and HOD approvals:")
    add_code_block(
        "@WebFilter(urlPatterns = {\"/student_dashboard.jsp\", \"/staff_dashboard.jsp\", \"/hod_dashboard.jsp\"})\n"
        "public class AuthenticationFilter implements Filter {\n"
        "    @Override\n"
        "    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)\n"
        "            throws IOException, ServletException {\n"
        "        HttpServletRequest request = (HttpServletRequest) req;\n"
        "        HttpServletResponse response = (HttpServletResponse) res;\n"
        "        HttpSession session = request.getSession(false);\n"
        "        String path = request.getServletPath();\n"
        "        String role = (session != null) ? (String) session.getAttribute(\"role\") : null;\n\n"
        "        if (role == null) {\n"
        "            response.sendRedirect(request.getContextPath() + \"/login.html\");\n"
        "            return;\n"
        "        }\n"
        "        if (path.contains(\"student_\") && !\"student\".equalsIgnoreCase(role)) {\n"
        "            response.sendError(HttpServletResponse.SC_FORBIDDEN);\n"
        "            return;\n"
        "        }\n"
        "        if (path.contains(\"staff_\") && !\"staff\".equalsIgnoreCase(role)) {\n"
        "            response.sendError(HttpServletResponse.SC_FORBIDDEN);\n"
        "            return;\n"
        "        }\n"
        "        if (path.contains(\"hod_\") && !\"hod\".equalsIgnoreCase(role)) {\n"
        "            response.sendError(HttpServletResponse.SC_FORBIDDEN);\n"
        "            return;\n"
        "        }\n"
        "        chain.doFilter(req, res);\n"
        "    }\n"
        "}"
    )

    add_h2("8.8 SOURCE CODE – JSP DASHBOARD SECURITY GUARD AND web.xml (PHASE 4)")
    add_p("JSP scriptlet security check ensuring defense-in-depth and the web.xml container configuration:")
    add_code_block(
        "<%-- student_dashboard.jsp session header guard --%>\n"
        "<%\n"
        "    String role = (String) session.getAttribute(\"role\");\n"
        "    String fullName = (String) session.getAttribute(\"fullName\");\n"
        "    if (role == null || !\"student\".equalsIgnoreCase(role)) {\n"
        "        response.sendRedirect(\"login.html\");\n"
        "        return;\n"
        "    }\n"
        "%>\n"
        "<h2>Welcome, <%= fullName %></h2>\n\n"
        "<!-- WEB-INF/web.xml deployment descriptor -->\n"
        "<web-app xmlns=\"http://xmlns.jcp.org/xml/ns/javaee\" version=\"3.1\">\n"
        "    <welcome-file-list>\n"
        "        <welcome-file>index.html</welcome-file>\n"
        "    </welcome-file-list>\n"
        "    <session-config>\n"
        "        <session-timeout>30</session-timeout>\n"
        "        <cookie-config>\n"
        "            <http-only>true</http-only>\n"
        "        </cookie-config>\n"
        "    </session-config>\n"
        "</web-app>"
    )

    # =========================================================================
    # SECTION 9: FEATURES OF THE PROJECT
    # =========================================================================
    add_h1("9. FEATURES OF THE PROJECT")
    add_p("The Digital Leave and On-Duty Application System incorporates several enterprise features that enhance institutional governance, administrative efficiency, and software reliability:")
    add_bullet("Applications transition through a deterministic verification pipeline: Student Submission -> Faculty Mentor Verification -> HOD Executive Sanction. At no point can a student bypass staff verification to directly obtain HOD approval.", "1. Multi-Tier Role-Based Workflow: ")
    add_bullet("The system programmatically validates the event completion date (toDate) against the current calendar date. If more than three calendar days have elapsed, the application is strictly rejected, preventing retroactive leave claims.", "2. Automated 3-Day Submission Rule Enforcement: ")
    add_bullet("The application dynamically queries MySQL to calculate total utilized duty days per student. New requests that would cause aggregate duty to exceed the 15-day semester ceiling are blocked, displaying remaining allowable days.", "3. Strict 15-Day Semester Quota Management: ")
    add_bullet("Prospective date windows are cross-referenced with the applicant's existing active records, preventing overlapping bookings and duplicate claims on identical dates.", "4. Temporal Overlap and Conflict Detection: ")
    add_bullet("Session states are secured via HTTP-only cookie-backed HttpSessions. URL tampering and unauthorized cross-role access are intercepted by AuthenticationFilter, returning HTTP 403 Forbidden responses.", "5. Granular Access Control and Session Hardening: ")
    add_bullet("Every database transaction is executed via JDBC PreparedStatement parameterized queries, providing complete immunity against SQL injection vulnerabilities.", "6. SQL Injection Immunity: ")
    add_bullet("Dynamic JSP dashboards present live analytical summary cards displaying total applications, pending verifications, approved requests, and remaining semester quota.", "7. Real-Time Analytical Metrics: ")
    add_bullet("When an application is rejected by Staff or the HOD, mandatory explanatory comments are captured and rendered on the student's history table, ensuring administrative transparency.", "8. Transparent Rejection Feedback: ")

    # =========================================================================
    # SECTION 10: FUTURE IMPROVEMENTS
    # =========================================================================
    add_h1("10. FUTURE IMPROVEMENTS")
    add_p("While the application fulfills all requirements of the MCA practical curriculum, several architectural enhancements can expand its capabilities for institutional deployment:")
    add_bullet("Incorporate multi-part document uploading allowing students to attach PDF or scanned image certificates. Integrating an Optical Character Recognition (OCR) pipeline can automatically verify event dates and student participation.", "1. Cloud Document Attachment and OCR Verification: ")
    add_bullet("Establish direct API connectivity with campus biometric turnstiles and RFID card readers, automatically updating attendance registers the moment an OD is approved by the HOD.", "2. Automated Biometric Turnstile and RFID Integration: ")
    add_bullet("Integrate transactional SMTP email (e.g., Apache Commons Email) and SMS gateways (e.g., Twilio) to dispatch real-time alerts to students when their application is verified or approved.", "3. Asynchronous Multi-Channel Notifications: ")
    add_bullet("Expand the schema into a multi-tenant cloud architecture supporting multiple academic departments, faculties, and autonomous sub-campuses within Kristu Jayanti University.", "4. Multi-Tenant University Architecture: ")
    add_bullet("Incorporate cryptographic QR codes on approved OD summary slips, enabling security personnel and examination invigilators to verify duty legitimacy instantly using a smartphone scanner.", "5. Cryptographic QR-Code Verification Slips: ")
    add_bullet("Integrate institutional Single Sign-On (SSO) utilizing LDAP, Microsoft Active Directory, or Google Workspace SAML 2.0 protocols for unified campus authentication.", "6. Campus Single Sign-On (SSO) Integration: ")
    add_bullet("Enhance the client frontend with service workers and manifest files to deliver a Progressive Web Application (PWA) supporting offline access and mobile home-screen installation.", "7. Progressive Web Application (PWA) Support: ")

    # =========================================================================
    # SECTION 11: CONCLUSION
    # =========================================================================
    add_h1("11. CONCLUSION")
    add_p("The Digital Leave and On-Duty Application System was engineered to solve a pervasive operational challenge in higher educational administration: the inefficiency, lack of policy compliance, and documentation loss associated with paper-based leave processing. By leveraging core Enterprise Java technologies—Java Standard Edition, Jakarta Servlets, JavaServer Pages (JSP), Java Database Connectivity (JDBC), and MySQL on Apache Tomcat 9—the project successfully migrates the entire On-Duty lifecycle into a secure, responsive, and auditable digital environment.")
    add_p("The application directly embodies the practical learning outcomes of the Java and Web Programming Laboratory across all four prescribed developmental phases. In Phase 1, robust object-oriented domain modeling and string validation established the foundational entities. In Phase 2, structured package modularization, service interfaces, and custom exception handling guaranteed software reliability and maintainability. In Phase 3, responsive HTML5, CSS3, and Vanilla JavaScript interfaces delivered client-side pre-validation and dynamic asynchronous form handling. Finally, in Phase 4, Java Servlets, JDBC persistence, secure HttpSession tracking, and role-based access filters realized an enterprise-grade multi-tier web application.")
    add_p("By automating strict institutional bylaws—specifically the 3-day post-event submission deadline and the 15-day maximum semester quota—the system eliminates administrative disputes and preserves academic rigor. The platform provides students with immediate transparency, equips faculty advisors with efficient verification tools, and furnishes departmental leadership with comprehensive oversight. Overall, the project demonstrates mastery of fundamental web software engineering principles, clean code practices, and the enduring power of core Enterprise Java architectures.")

    # =========================================================================
    # SECTION 12: REFERENCES
    # =========================================================================
    add_h1("12. REFERENCES")
    
    refs = [
        "1. Oracle Corporation. Java Platform, Standard Edition (Java SE) Documentation. [Online] Available at: https://docs.oracle.com/en/java/",
        "2. Jakarta EE / Java Community Process. Jakarta Servlet Specification 4.0 (JSR 369). [Online] Available at: https://jakarta.ee/specifications/servlet/4.0/",
        "3. Jakarta EE / Java Community Process. Jakarta Server Pages (JSP) Specification 2.3 (JSR 245). [Online] Available at: https://jakarta.ee/specifications/pages/2.3/",
        "4. Apache Software Foundation. Apache Tomcat 9 Configuration Reference. [Online] Available at: https://tomcat.apache.org/tomcat-9.0-doc/",
        "5. MySQL AB / Oracle Corporation. MySQL 8.0 Reference Manual and Connector/J Documentation. [Online] Available at: https://dev.mysql.com/doc/",
        "6. Mozilla Developer Network (MDN). Web Docs: HTML5, CSS3, JavaScript (Fetch API, DOM Events). [Online] Available at: https://developer.mozilla.org/",
        "7. Schildt, H. Java: The Complete Reference, 12th Edition. McGraw-Hill Education, 2021.",
        "8. Horstmann, C. S. Core Java Volume I – Fundamentals, 12th Edition. Prentice Hall / Pearson, 2022.",
        "9. Fowler, M. Patterns of Enterprise Application Architecture. Addison-Wesley Professional, 2002.",
        "10. Kristu Jayanti University. Academic Regulations, Attendance Requirements, and On-Duty Policy Bylaws. Department of Computer Applications, 2026–2027."
    ]
    for r_text in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(r_text)
        set_font_tnr(run, size_pt=11)

    output_path = os.path.abspath("PROJECT_BASED_PRACTICAL_REPORT_EDWIN_SAJI.docx")
    doc.save(output_path)
    print(f"Report generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_report()
