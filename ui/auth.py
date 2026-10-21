# 文件：ui/auth.py
# UI 层：登录认证与角色访问控制的装饰器
# 供路由使用，实现 FR09 / NFR03 的「基于角色访问控制」。

from functools import wraps

from flask import redirect, session, url_for


def login_required(view):
    """要求已登录：未登录则重定向到登录页。"""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("ui.login"))
        return view(*args, **kwargs)

    return wrapped


def role_required(*roles):
    """要求已登录且角色在允许列表中；否则拒绝访问。"""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("ui.login"))
            if session.get("role") not in roles:
                return "403 无权限访问", 403
            return view(*args, **kwargs)

        return wrapped

    return decorator
