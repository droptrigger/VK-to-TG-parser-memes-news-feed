import re
import vk_api
from bot.data.config import TOKEN_VK

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk = vk_session.get_api()


async def getID(id):
    if '[' in id:
        res = re.search(r'\d+', id).group()
        return res
    elif 'vk.com' in id:
        res = id.split('/')
        res = res[len(res) - 1]
        try:
            int(res)
            return res
        except:
            res_no_id = res.split('id')
            try:
                int(res_no_id)
                return res_no_id
            except:
                user_get = vk.utils.resolveScreenName(screen_name=f'{res}')
                res = user_get['object_id']
                return res
    elif 'https://' in id:
        res = id.split('/')
        res = res[len(res) - 1]
        try:
            int(res)
            return res
        except:
            res_no_id = res.split('id')
            try:
                int(res_no_id)
                return res_no_id
            except:
                user_get = vk.utils.resolveScreenName(screen_name=f'{res}')
                res = user_get['object_id']
                return res
    elif '@' in id:
        res = id.split('@')
        res = res[len(res) - 1]
        try:
            int(res)
            return res
        except:
            res_no_id = res.split('id')
            try:
                int(res_no_id)
                return res_no_id
            except:
                user_get = vk.utils.resolveScreenName(screen_name=f'{res}')
                res = user_get['object_id']
                return res
    else:
        return False
