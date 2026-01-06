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
        user_service.create_user({
            'username': 'lecturer',
            'email': 'lecturer@example.com',
            'full_name': 'Lecturer User',
            'password': 'password123',
            'is_active': True
        })
        print('Created lecturer user')
    else:
        print('Lecturer user already exists')


if __name__ == '__main__':
    seed()
