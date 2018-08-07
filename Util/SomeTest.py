import sys
from LogHandler import LogHandler
from Downloader import Downloader
sys.path.append('..')
from myspider import get_proxy
log = LogHandler('test', file=False)

down = Downloader()

log.info(down.user_agent)
i = 0
while (i < 100):
    data = down.getData(
        url="http://music.163.com/api/v1/resource/comments/R_SO_4_386538?limit=20&offset=18520")
    log.info('time: %s, data len: %s' % (i, len(data)))
    i = i + 1
