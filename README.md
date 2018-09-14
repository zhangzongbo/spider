#### 初学python,根据网上的资料写的一个云音乐评论爬虫

#### 添加了代理池和多线程的支持.[代理池项目地址](https://github.com/zhangzongbo/python_proxy_pool)

#### 代理池fork自 [@jhao104](https://github.com/jhao104/proxy_pool) 的git 项目

#### 抽出了一个独立的downloader,支持超时重试和内容不正确时的重试（把部分格式化逻辑放在了downloader中不太合理，但是为了解决服务器偶尔的异常返回，这里需要优化）

#### 启动myspider.py时需要本地启动了代理池，或者使用网上的接口(http://140.143.143.233/get/ | http://123.207.35.36:5010/get ),或者注掉代理池相关代码
![](https://ws1.sinaimg.cn/large/b20a1329ly1fuoe39nh9jj216i0lqe83.jpg)
