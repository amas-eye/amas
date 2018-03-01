# coding=utf-8
"""状态码
"""

CODE_OK = 0
CODE_FAIL = 1000
CODE_NOT_FOUND = 1001
DB_ERROR = 1002
UPDATE_ACCEPTED = 2000 # both single and multiple
UPDATE_FAILED = 2001 # both single and multiple
METRIC_NOT_FOUND = 2002 # single only
INVALID_JSON = 2003 # single only
UPDATE_UNCOMPLETED = 3000 # multiple only
REQUEST_PARAM_INVAILD = 4001 # currently only support query records via key words request
