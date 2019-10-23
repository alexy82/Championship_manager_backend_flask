import logging

import configs
from app.core.managers.token import get_info_token
from app.core.models.user import User
from app.core.managers.role import get_all_role_by_user_id
from app.core.managers.permission import get_all_permission_by_user_id
from app.core.managers.user_team import is_leader, is_manager, get_teams_by_user
from app.core.managers.user_status import get_user_status_by_id
from app.core.utils.constants import UserStatuses

LOGGER = logging.getLogger('main')


def validate_access_token(data):
    resp = get_info_token(data)
    if resp is None:
        LOGGER.error('User doesn\'t have permission access to our system.')
        return None

    user_data = {
        'email': resp.get('email'),
    }
    our_user_info = User.update(user_data)
    if our_user_info is None:
        LOGGER.error('User doesnt exist in system')
        return None

    wrapped_resp = resp.copy()
    wrapped_resp['user_id'] = our_user_info.id
    wrapped_resp['is_leader'] = is_leader(our_user_info.id)
    wrapped_resp['is_manager'] = is_manager(our_user_info.id)
    wrapped_resp['roles'] = get_all_role_by_user_id(
        user_id=our_user_info.id)
    wrapped_resp['permission'] = get_all_permission_by_user_id(
        user_id=our_user_info.id)
    user_teams = get_teams_by_user(our_user_info.id)
    wrapped_resp['team_ids'] = [team.get('id') for team in user_teams] \
        if user_teams is not None else []
    if our_user_info.email in configs.REVIEW_NATION_DEBT_USERS:
        wrapped_resp['order_review_debt'] = 1

    user_team_statuses = get_user_status_by_id(our_user_info.id)
    wrapped_resp['status'] = user_team_statuses.get('status') if user_team_statuses is not None \
        else UserStatuses.OFFLINE

    return wrapped_resp
