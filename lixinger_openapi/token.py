# -*- coding: utf-8 -*-
'''
token全局管理
'''
import os
import base64

__token__ = None

def set_token(token, write_token = True):
    '''
    加载token
    '''
    global __token__
    __token__ = token
    if write_token:
        token_cfg = os.getcwd() + '/token.cfg'
        import base64
        encrypted_token = base64.b64encode(token.encode()).decode()
        # 修复文件权限问题
        with open(token_cfg, 'w') as f:
            f.write(encrypted_token)
        os.chmod(token_cfg, 0o600)  # 设置仅用户可读写

def get_token():
    '''
    获取token
    '''
    global __token__
    if __token__ is None:
        token_cfg = os.getcwd() + '/token.cfg'
        if os.path.exists(token_cfg):
            with open(token_cfg, 'r') as f:
                encrypted_token = f.read().strip()
            __token__ = base64.b64decode(encrypted_token).decode()
    return __token__
