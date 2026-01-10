from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.syllabus_service import SyllabusService
from services.user_service import UserService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/stats')

@dashboard_bp.route('/', methods=['GET'])
@inject
def get_stats(syllabus_service: SyllabusService = Provide[Container.syllabus_service], user_service: UserService = Provide[Container.user_service]):
    syllabuses = syllabus_service.list_syllabuses() or []
    users = user_service.list_users() or []

    total_syllabuses = len(syllabuses)
    total_users = len(users)

    # Group by status
    stats_by_status = {
        'Approved': 0,
        'Pending': 0,
        'Draft': 0,
        'Returned': 0
    }
    for s in syllabuses:
        status = getattr(s, 'status', None) or getattr(s, 'state', None) or 'Draft'
        # Normalize
        if status.upper() in ('APPROVED',):
            stats_by_status['Approved'] += 1
        elif 'PENDING' in status.upper():
            stats_by_status['Pending'] += 1
        elif status.upper() in ('RETURNED', 'REJECTED'):
            stats_by_status['Returned'] += 1
        else:
            stats_by_status['Draft'] += 1

    return jsonify({
        'total_syllabuses': total_syllabuses,
        'total_users': total_users,
        'by_status': stats_by_status
    }), 200
