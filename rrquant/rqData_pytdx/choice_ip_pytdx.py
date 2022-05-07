# coding:utf-8
#
import time
from concurrent import futures
from pytdx.hq import TdxHq_API
from pytdx.config.hosts import hq_hosts

def ping(ip, port=7709, multithread=False):
    api = TdxHq_API(multithread=multithread)
    success = False
    starttime = time.time()
    try:
        with api.connect(ip, port, time_out=1):
            #x = api.get_security_count(0)
            #x = api.get_index_bars(7, 1, '000001', 800, 100)
            x = api.get_security_bars(7, 0, '000001', 800, 100)
            if x:
                success = True

    except Exception as e:
        success = False

    endtime = time.time()
    return (success, endtime - starttime, ip, port)


def search_best_tdx():
    def ping2(host):
        return ping(host[0], host[1], host[2])

    hosts = [(host[1], host[2], True) for host in hq_hosts]
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(ping2, hosts, timeout=2)
    x = [i for i in res if i[0] == True]
    x.sort(key=lambda item: item[1])
    return x


if __name__ == '__main__':
    import time
    starttime = time.time()

    x = search_best_tdx()
    for i in x:
        print(i)
    print(len(x))
    print(len(hq_hosts))

    endtime = time.time()
    print("\nTotal time:")
    print("%.2fs" % (endtime - starttime))
    print("%.2fm" % ((endtime - starttime) / 60))
