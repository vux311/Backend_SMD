import sys
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import json

# --- CẤU HÌNH ĐƯỜNG DẪN IMPORT ---
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# --- IMPORT MODULES ---
try:
    from infrastructure.databases.mssql import session, engine, Base
    from infrastructure.models import (
        User, Role, UserRole, Faculty, Department, Program, ProgramOutcome,
        Subject, AcademicYear, Syllabus, SyllabusClo, SyllabusMaterial,
        TeachingPlan, AssessmentScheme, AssessmentComponent, Rubric
    )
    # Import thêm bảng phụ nếu cần
    from infrastructure.models.workflow_state_model import WorkflowState
except ImportError as e:
    print(f"❌ Lỗi Import: {e}")
    sys.exit(1)

# ----------------------------------------

def hash_password(password: str) -> str:
    """Hash password using werkzeug.generate_password_hash"""
    return generate_password_hash(password)

def seed_all():
    print("🌱 Bắt đầu nạp dữ liệu mẫu (Seeding)...")
    
    # 1. Tạo Tables
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️ Cảnh báo tạo bảng: {e}")

    try:
        # --- 2. ROLES ---
        print("... Seeding Roles")
        roles_data = {
            "Admin": "Quản trị hệ thống",
            "Lecturer": "Giảng viên",
            "Head of Dept": "Trưởng bộ môn",
            "Academic Affairs": "Phòng đào tạo",
            "Student": "Sinh viên"
        }
        role_objs = {}
        for name, desc in roles_data.items():
            role = session.query(Role).filter_by(name=name).first()
            if not role:
                role = Role(name=name, description=desc)
                session.add(role)
            role_objs[name] = role
        session.flush()

        # --- 3. FACULTY & DEPARTMENT ---
        print("... Seeding Faculty & Departments")
        faculty = session.query(Faculty).filter_by(code="CNTT").first()
        if not faculty:
            faculty = Faculty(code="CNTT", name="Công nghệ thông tin")
            session.add(faculty)
            session.flush()

        depts_data = [
            {"code": "CNPM", "name": "Kỹ thuật phần mềm"},
            {"code": "KHMT", "name": "Khoa học máy tính"},
            {"code": "HTTT", "name": "Hệ thống thông tin"}
        ]
        dept_objs = {}
        for d in depts_data:
            dept = session.query(Department).filter_by(code=d["code"]).first()
            if not dept:
                dept = Department(code=d["code"], name=d["name"], faculty_id=faculty.id)
                session.add(dept)
            dept_objs[d["code"]] = dept
        session.flush()

        # --- 4. USERS ---
        print("... Seeding Users")
        users_data = [
            {"u": "admin", "n": "Quản Trị Viên", "r": "Admin", "d": None},
            {"u": "gv1", "n": "Nguyễn Văn A", "r": "Lecturer", "d": "CNPM"},
            {"u": "gv2", "n": "Trần Thị B", "r": "Lecturer", "d": "KHMT"},
            {"u": "hod1", "n": "TS. Lê Văn C", "r": "Head of Dept", "d": "CNPM"},
            {"u": "aa1", "n": "Phòng Đào Tạo", "r": "Academic Affairs", "d": None},
            {"u": "sv1", "n": "Sinh Viên Test", "r": "Student", "d": "CNPM"},
        ]
        
        user_objs = {}
        default_pass = hash_password("123456")

        for u in users_data:
            user = session.query(User).filter_by(username=u["u"]).first()
            dept_id = dept_objs[u["d"]].id if u["d"] else None
            if not user:
                user = User(
                    username=u["u"],
                    email=f"{u['u']}@ut.edu.vn",
                    full_name=u["n"],
                    password_hash=default_pass,
                    department_id=dept_id,
                    is_active=True
                )
                session.add(user)
                session.flush()

                # Gán Role
                if u["r"] in role_objs:
                    user_role = UserRole(user_id=user.id, role_id=role_objs[u["r"]].id)
                    session.add(user_role)
            else:
                # Ensure seeded test users have werkzeug-hashed passwords (migrate old bcrypt hashes)
                user.password_hash = default_pass
                # Ensure role assignment exists
                existing_role = session.query(UserRole).filter_by(user_id=user.id).first()
                if not existing_role and u["r"] in role_objs:
                    user_role = UserRole(user_id=user.id, role_id=role_objs[u["r"]].id)
                    session.add(user_role)

            user_objs[u["u"]] = user
        session.flush()

        # --- 5. PROGRAMS ---
        print("... Seeding Programs")
        prog = session.query(Program).filter_by(name="Kỹ sư Phần mềm").first()
        if not prog:
            prog = Program(department_id=dept_objs["CNPM"].id, name="Kỹ sư Phần mềm", total_credits=150)
            session.add(prog)
            session.flush()
            
            plos = [
                ("PLO1", "Áp dụng kiến thức toán học"),
                ("PLO2", "Phân tích và thiết kế hệ thống"),
                ("PLO3", "Kỹ năng lập trình chuyên sâu")
            ]
            for code, desc in plos:
                session.add(ProgramOutcome(program_id=prog.id, code=code, description=desc))
        session.flush()

        # --- 6. ACADEMIC YEAR ---
        print("... Seeding Academic Years")
        ay = session.query(AcademicYear).filter_by(code="2025-2026").first()
        if not ay:
            ay = AcademicYear(
                code="2025-2026", 
                start_date=date(2025, 9, 1), 
                end_date=date(2026, 6, 30)
            )
            session.add(ay)
        session.flush()

        # --- 7. SUBJECTS ---
        print("... Seeding Subjects")
        # Chú ý: Cấu trúc Subject đã thay đổi (name_vi, name_en, credit_theory...)
        subjects_data = [
            {"code": "IT001", "vi": "Nhập môn Lập trình", "en": "Intro to Programming", "cr": 3},
            {"code": "SE101", "vi": "Công nghệ Phần mềm", "en": "Software Engineering", "cr": 4},
            {"code": "WEB01", "vi": "Lập trình Web", "en": "Web Development", "cr": 3},
        ]
        subj_objs = {}
        for s in subjects_data:
            subj = session.query(Subject).filter_by(code=s["code"]).first()
            if not subj:
                subj = Subject(
                    department_id=dept_objs["CNPM"].id,
                    code=s["code"],
                    name_vi=s["vi"],
                    name_en=s["en"],
                    credits=s["cr"],
                    credit_theory=s["cr"],     # Mặc định lý thuyết = tổng tín chỉ (ví dụ đơn giản)
                    credit_practice=0,
                    credit_self_study=s["cr"] * 2
                )
                session.add(subj)
            subj_objs[s["code"]] = subj
        session.flush()

        # --- 8. SYLLABUS ---
        print("... Seeding Syllabus")
        
        if "WEB01" in subj_objs and "gv1" in user_objs:
            web_subj = subj_objs["WEB01"]
            lecturer = user_objs["gv1"]
            
            existing_syl = session.query(Syllabus).filter_by(subject_id=web_subj.id).first()
            if not existing_syl:
                # FIX LỖI: Không truyền 'description' vì model không có cột này
                syl = Syllabus(
                    subject_id=web_subj.id,
                    program_id=prog.id,
                    academic_year_id=ay.id,
                    lecturer_id=lecturer.id,
                    status="Approved",
                    version="1.0",
                    # Lưu JSON vào cột Text
                    time_allocation=json.dumps({"theory": 30, "practice": 15, "self_study": 90}), 
                    prerequisites="Tin học đại cương",
                    publish_date=datetime.now(),
                    is_active=True
                )
                session.add(syl)
                session.flush()

                # 8.1 CLOs (SyllabusClo CÓ cột description)
                clos = [
                    SyllabusClo(syllabus_id=syl.id, code="CLO1", description="Hiểu kiến thức cơ bản về Web"),
                    SyllabusClo(syllabus_id=syl.id, code="CLO2", description="Vận dụng ReactJS xây dựng UI"),
                    SyllabusClo(syllabus_id=syl.id, code="CLO3", description="Triển khai ứng dụng lên Vercel")
                ]
                session.add_all(clos)
                session.flush()

                # 8.2 Teaching Plan
                plans = [
                    TeachingPlan(syllabus_id=syl.id, week=1, topic="Tổng quan Web", activity="Giảng lý thuyết", assessment="Điểm danh"),
                    TeachingPlan(syllabus_id=syl.id, week=2, topic="HTML & CSS", activity="Code demo", assessment="Bài tập về nhà"),
                ]
                session.add_all(plans)

                # 8.3 Materials
                materials = [
                    SyllabusMaterial(syllabus_id=syl.id, type="Main", title="Giáo trình Lập trình Web", author="Nguyễn Văn A"),
                ]
                session.add_all(materials)

                # 8.4 Assessment Scheme
                scheme = AssessmentScheme(syllabus_id=syl.id, name="Đánh giá quá trình", weight=50)
                session.add(scheme)
                session.flush()

                comp = AssessmentComponent(scheme_id=scheme.id, name="Đồ án giữa kỳ", weight=50)
                session.add(comp)
                session.flush()
                
                # Rubric
                rubric = Rubric(
                    component_id=comp.id, 
                    criteria="Giao diện đẹp", 
                    max_score=10, 
                    description_level_pass="Đẹp", 
                    description_level_fail="Xấu"
                )
                session.add(rubric)

        session.commit()
        print("✅ Đã nạp dữ liệu thành công! (Seed Completed)")

    except Exception as e:
        session.rollback()
        print(f"❌ Có lỗi xảy ra: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    seed_all()