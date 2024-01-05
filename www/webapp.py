import logging  # 导入日志模块
import asyncio  # 导入异步I/O模块
from aiohttp import web  # 导入aiohttp的web模块
def index(request):   # 定义处理请求的函数
	return web.Response(body = b"<h1>Hi, there!</h1>", headers = {"content-type": "text/html"})  # 返回一个包含简单HTML的响应
async def init(loop):  # 使用装饰器定义异步函数,初始化服务器的异步函数
    app = web.Application(loop=loop)  # 创建web应用程序
    app.router.add_route('GET', '/', index)  # 将处理函数绑定到根路由
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)  # 创建服务器
    logging.info('server started at http://127.0.0.1:9000...')  # 记录服务器启动信息
    return srv  # 返回服务器实例
loop = asyncio.get_event_loop()  # 获取事件循环对象
loop.run_until_complete(init(loop))  # 运行初始化函数
loop.run_forever()  # 开始事件循环


async def create_pool(loop, **kw):
    # 记录日志，表示正在创建数据库连接池
    logging.info('create database connection pool...')
    global __pool
    # 创建一个数据库连接池
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),  # 数据库主机，默认为localhost
        port=kw.get('port', 3306),          # 数据库端口，默认为3306
        user=kw['user'],                    # 数据库用户名
        password=kw['password'],            # 数据库密码
        db=kw['db'],                        # 数据库名称
        charset=kw.get('charset', 'utf8'),  # 字符集，默认为utf8
        autocommit=kw.get('autocommit', True),  # 自动提交，默认为True
        maxsize=kw.get('maxsize', 10),      # 连接池最大连接数，默认为10
        minsize=kw.get('minsize', 1),       # 连接池最小连接数，默认为1
        loop=loop                           # 事件循环
    )

async def select(sql, args, size=None):
    log(sql, args)  # 记录日志，调用日志函数记录SQL语句和参数
    global __pool  # 引用全局变量数据库连接池
    # 使用异步上下文管理器获取数据库连接
    with (await __pool) as conn:
        # 在连接上创建一个游标，以字典方式返回结果
        cur = await conn.cursor(aiomysql.DictCursor)
        # 执行SQL语句，使用参数代替占位符
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            # 如果设置了size，获取指定数量的结果集
            rs = await cur.fetchmany(size)
        else:
            # 否则获取所有结果集
            rs = await cur.fetchall()
        await cur.close()  # 关闭游标
        logging.info('rows returned: %s' % len(rs))  # 记录返回行数
        return rs  # 返回结果集


async def execute(sql, args):
    log(sql)  # 记录日志，调用日志函数记录SQL语句
    with (await __pool) as conn:  # 通过异步生成器从连接池获取连接
        try:
            cur = await conn.cursor()  # 从连接上获取游标
            await cur.execute(sql.replace('?', '%s'), args)  # 执行SQL语句，用参数替换占位符
            affected = cur.rowcount  # 获取受影响的行数
            await cur.close()  # 关闭游标
        except BaseException as e:
            raise  # 发生异常时抛出异常
        return affected  # 返回受影响的行数
