# 創建adapter.py目的是為了解決當使用者註冊時，即使密碼不合法
# Allauth 也會先把 username 寫進資料庫（創建 User instance）
# 然後報錯「密碼不符合」，但是 username 已經被搶先佔住了
# 下一次就不能用了的可能性
# 為了避免掉寫416f

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_username


class SafeSignupAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        只有當密碼、欄位都通過驗證時，才真正儲存 user。
        """
        # 強制 username 小寫（你需要的功能）
        username = form.cleaned_data.get("username")
        if username:
            user_username(user, username.lower())

        # 在 super().save_user 之前，不執行 commit
        user = super().save_user(request, user, form, commit=False)

        # 如果全部驗證都成功才真的儲存到 DB
        if commit:
            user.save()
        return user
