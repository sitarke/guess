import signal
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from start import Start
from 面灵气喵 import botpush

app = FastAPI()
# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/data")
async def root():
    return botpush()

@app.get("/bet/{red_blue}")
async def execute_bet_game(red_blue: str):
    try:
        # 逻辑代码
        last_bet_result, current_execute_res, base64_res = Start.main(red_blue)
    except Exception as e:
        # 记录异常信息
        console.error(f"Error executing bet game for item {red_blue}: {e}")
        # 构造错误响应
        return {"code": 500, "message": "An error occurred while processing the request."}, 500
    
    # 构造成功返回结果
    response_data = {
        "code": 200,
        "last_bet_result": last_bet_result,
        "current_execute_res": current_execute_res,
        "base64_res": base64_res
    }
    return response_data

# 处理信号，优雅地关闭服务
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    Start.stop_event.set()  # 设置停止事件
    sys.exit(0)

def main():
    """ 主入口函数 """
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    # 设置 Uvicorn 服务器参数
    uvicorn.run(app, host="0.0.0.0", port=3300)

if __name__ == "__main__":
    main()