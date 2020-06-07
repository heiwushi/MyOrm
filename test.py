from orm import create_pool, Model, IntegerField, StringField
import asyncio
loop = asyncio.get_event_loop()

class User(Model):
    # 定义类的属性到列的映射：
    __table__ = 'User'
    uid = IntegerField('uid')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


async def main():
    await create_pool(host='127.0.0.1', port=3306, user="root", password='a123', db="orm", loop=loop)
    user1 = User(uid=1, name="user1", email="xxx@sina.com", password='123456')
    await user1.save()
    user2 = User(uid=2, name="user2", email="xxxxaa@qq.com", password='qqqqqqq')
    await user2.save()
    user_list = await User.select()
    for user in user_list:
        print(user.mapping)

loop.run_until_complete(main())
