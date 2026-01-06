from dependency_container import Container


def seed():
    container = Container()
    role_service = container.role_service()
    user_service = container.user_service()
    session = container.db_session()

    # Get or create roles
    admin_role = role_service.get_by_name('ADMIN')
    if not admin_role:
        admin_role = role_service.create_role({'name': 'ADMIN', 'description': 'ADMIN role'})
        print('Created role: ADMIN')
    else:
        print('Role already exists: ADMIN')

    lecturer_role = role_service.get_by_name('LECTURER')
    if not lecturer_role:
        lecturer_role = role_service.create_role({'name': 'LECTURER', 'description': 'LECTURER role'})
        print('Created role: LECTURER')
    else:
        print('Role already exists: LECTURER')

    # Get or create admin user
    admin = user_service.get_by_username('admin')
    if not admin:
        admin = user_service.create_user({
            'username': 'admin',
            'email': 'admin@example.com',
            'full_name': 'Admin User',
            'password': 'password123',
            'is_active': True
        })
        print('Created admin user')
    else:
        print('Admin user already exists')

    # Get or create lecturer user
    lecturer = user_service.get_by_username('lecturer')
    if not lecturer:
        lecturer = user_service.create_user({
            'username': 'lecturer',
            'email': 'lecturer@example.com',
            'full_name': 'Lecturer User',
            'password': 'password123',
            'is_active': True
        })
        print('Created lecturer user')
    else:
        print('Lecturer user already exists')

    # Attach roles if missing
    from infrastructure.models.user_role_model import UserRole

    if admin and admin_role:
        exists = session.query(UserRole).filter_by(user_id=admin.id, role_id=admin_role.id).first()
        if not exists:
            try:
                session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
                session.commit()
                print('Assigned ADMIN role to admin user')
            except Exception:
                session.rollback()
    
    if lecturer and lecturer_role:
        exists = session.query(UserRole).filter_by(user_id=lecturer.id, role_id=lecturer_role.id).first()
        if not exists:
            try:
                session.add(UserRole(user_id=lecturer.id, role_id=lecturer_role.id))
                session.commit()
                print('Assigned LECTURER role to lecturer user')
            except Exception:
                session.rollback()


if __name__ == '__main__':
    seed()
