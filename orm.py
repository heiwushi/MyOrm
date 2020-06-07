import aiomysql
import asyncio
import copy
#from contextlib import asynccontextmanager

pool = None

class Field(object):
    def __init__(self, field_name):
        pass


class IntegerField(Field):
    pass


class StringField(Field):
    pass


async def create_pool(loop, host, port, user, password, db, charset='utf8', maxsize=10, minsize=1):
    print('create database connection pool...')
    global pool
    pool = await aiomysql.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db,
        charset=charset,
        maxsize=maxsize,
        minsize=minsize,
        loop=loop,
        autocommit=True
    )


class Model(object):



    def __init__(self, **kwargs):

        if hasattr(self.__class__, '__table__'):
            self.table = self.__class__.__table__
        else:
            self.table = self.__class__.__name__
        self.mapping = copy.deepcopy(kwargs)
    #
    # def __getattr__(self, key):
    #     return self.mapping[key]
    #
    #
    # def __setattr__(self, key, value):
    #     self.mapping[key] = value


    # @staticmethod
    # def convert_arg_to_str(x):
    #     if isinstance(x, str):
    #         return '\''+x+'\''
    #     else:
    #         return str(x)


    async def save(self):
        global __pool
        params = []
        args = []
        for k,v in self.__class__.__dict__.items():
            if isinstance(v, Field):
               params.append(k)
               args.append(self.mapping[k])
        sql = "insert into {table} ({params}) values ({args})".format(table=self.table, params=','.join(params), args=','.join(["%s"]*len(args)))
        print(sql, args)
        with (await pool) as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            await cur.close()

    @classmethod
    async def select(cls):
        fields = []
        for k, v in cls.__dict__.items():
            if isinstance(v, Field):
                fields.append(k)

        def gen_model(item):
            args = {}
            for i, f in enumerate(fields):
                args[f] = item[i]
            return cls(**args)

        sql = "select {fields} from {table}".format(fields=','.join(fields), table=cls.__table__)
        print(sql)
        with (await pool) as conn:
            cur = await conn.cursor()
            await cur.execute(sql)
            r = await cur.fetchall()
            await cur.close()
        return tuple(map(gen_model, r))


