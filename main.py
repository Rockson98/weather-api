#!/usr/bin/env python3
"""
天气查询API主入口文件
"""

from tianqi_webtool.server import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Render 部署支持 - 动态端口配置
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    uvicorn.run(app, host=host, port=port)
