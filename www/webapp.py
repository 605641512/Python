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

