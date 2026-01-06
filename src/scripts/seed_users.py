from dependency_container import Container


def seed():
    container = Container()
    role_service = container.role_service()
    user_service = container.user_service()

    # Create roles if they don't exist
    for role_name in ('ADMIN', 'LECTURER'):
        if not role_service.get_by_name(role_name):
            role_service.create_role({'name': role_name, 'description': f'{role_name} role'})
            print(f"Created role: {role_name}")
        else:
            print(f"Role already exists: {role_name}")

    # Create admin user
    admin_exists = user_service.get_by_username('admin')
    if not admin_exists:
        user_service.create_user({
            'username': 'admin',
            'email': 'admin@example.com',
            'full_name': 'Admin User',
            'password': 'password123',
            'is_active': True
        })
        print('Created admin user')
    else:
        print('Admin user already exists')

    lecturer_exists = user_service.get_by_username('lecturer')
    if not lecturer_exists:
        lecturer = user_service.create_user({
            'username': 'lecturer',
            'email': 'lecturer@example.com',
            'full_name': 'Lecturer User',
            'password': 'password123',
            'is_active': True
        })
        print('Created lecturer user')
    else:
        lecturer = user_service.get_by_username('lecturer')
        print('Lecturer user already exists')

    # Attach roles (if possible)
    session = container.db_session()
    from infrastructure.models.user_role_model import UserRole

    admin_role = role_service.get_by_name('ADMIN')
    if admin and admin_role:
        try:
            session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
            session.commit()
            print('Assigned ADMIN role to admin user')
        except Exception:
            session.rollback()

    lecturer_role = role_service.get_by_name('LECTURER')
    if lecturer and lecturer_role:
        try:
            session.add(UserRole(user_id=lecturer.id, role_id=lecturer_role.id))
            session.commit()
            print('Assigned LECTURER role to lecturer user')
        except Exception:
            session.rollback()


if __name__ == '__main__':
    seed()
