from enum import Enum


class EventType(Enum):
    START_REQUEST = 'StartRequest'
    BACKEND_CONNECT = 'BackendConnect'
    BACKEND_REQUEST = 'BackendRequest'
    BACKEND_OK = 'BackendOk'
    BACKEND_ERROR = 'BackendError'
    START_MERGE = 'StartMerge'
    START_SEND_RESULT = 'StartSendResult'
    FINISH_REQUEST = 'FinishRequest'
