# 导入所需模块
import logging
import asyncio
from aiohttp import web

# 配置日志记录级别为 INFO
logging.basicConfig(level=logging.INFO)

# 处理 HTTP 请求的函数
async def index(request):
    # 返回 HTTP 响应，内容为 "<h1>Hi, there!</h1>"，类型为 HTML
    return web.Response(body=b"<h1>Hi, there!</h1>", headers={"content-type": "text/html"})

# 初始化函数，用于创建服务器
async def init():
    # 创建 web 应用程序实例
    app = web.Application()
    
    # 添加路由规则，将 GET 请求映射到 index 函数处理
    app.router.add_route('GET', '/', index)
    
    # 创建服务器并绑定到指定的地址和端口
    srv = await asyncio.get_event_loop().create_server(app.make_handler(), '127.0.0.1', 9000)
    
    # 记录服务器启动信息到日志
    logging.info('Server started at http://127.0.0.1:9000...')
    
    return srv

# 运行初始化函数
asyncio.run(init())
