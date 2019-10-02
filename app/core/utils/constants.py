from http import HTTPStatus


class InternalErrorCode:
    UNAUTHORIZED = 8
    INTERNAL_SERVER_ERROR = 1
    BAD_REQUEST = 2
    SUCCESS = 0
    NOT_FOUND = 14
    CONFLICT = 15


mapping_internal_codes = {
    HTTPStatus.UNAUTHORIZED: InternalErrorCode.UNAUTHORIZED,
    HTTPStatus.BAD_REQUEST: InternalErrorCode.BAD_REQUEST,
    HTTPStatus.OK: InternalErrorCode.SUCCESS,
    HTTPStatus.NOT_FOUND: InternalErrorCode.NOT_FOUND,
    HTTPStatus.CONFLICT: InternalErrorCode.CONFLICT,
    HTTPStatus.INTERNAL_SERVER_ERROR: InternalErrorCode.INTERNAL_SERVER_ERROR
}

mapping_ops_channel_role = {
    2: 'Online Leader',
    4: 'Agent Leader'
}

mapping_om_statuses = {
    'DRAFT': 'WAITING-PROCESS',
    'SUCCESS': 'PROCESSED',
    'CANCELLED-DRAFT': 'CANCELLED-DRAFT',
    'CANCELLED': 'CANCELLED'
}

mapping_channel = {
    1: 'SHOWROOM',
    2: 'ONLINE',
    3: 'Telesale',
    4: 'AGENT',
    5: 'VNSHOP'
}


class TeamStatus:
    ACTIVE = 1
    INACTIVE = 0


permissions = {
    'order_area_transferring': 'order_area_transferring',
    'order_process': 'order_process',
    'order_review_debt': 'order_review_debt',
    'order_cancel': 'order_cancel',
}


class CacheTimeout:
    LO_LIST_REGION = 300
    CLIENT_TOKEN = 900
    LIST_SALESMEN = 600


class UserStatuses:
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2


class OrphanOrderStatus:
    IN_PROCESSED = 1
    NO_PROCESSED = 0


class CacheKey:
    LIST_SALESMEN = 'list_salesmen'
    ORDER_PROCESSING_BY_USER = 'order_processing_by_user'
