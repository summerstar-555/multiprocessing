"""
    Pool类
    Pool类可以提供指定数量的进程供用户调用，当有新的请求提交到Pool中时，如果池还没有满，就会创建一个新的进程来执行请求。如果池满，请求就会告知先等待，直到池中有进程结束，
　　 才会创建新的进程来执行这些请求。 
　　 下面介绍一下multiprocessing 模块下的Pool类下的几个方法：
　　1、apply()
　　　　函数原型：apply(func[, args=()[, kwds={}]])
　　　　该函数用于传递不定参数，同python中的apply函数一致，主进程会被阻塞直到函数执行结束（不建议使用，并且3.x以后不在出现）。
　　2、apply_async
　　　　函数原型：apply_async(func[, args=()[, kwds={}[, callback=None]]])
　　　　与apply用法一致，但它是非阻塞的且支持结果返回后进行回调。
　　3、map()
 　　　　函数原型：map(func, iterable[, chunksize=None])
　　　　Pool类中的map方法，与内置的map函数用法行为基本一致，它会使进程阻塞直到结果返回。 
　　　　注意：虽然第二个参数是一个迭代器，但在实际使用中，必须在整个队列都就绪后，程序才会运行子进程。
　　4、map_async()
　　　　函数原型：map_async(func, iterable[, chunksize[, callback]])
　　　　与map用法一致，但是它是非阻塞的。其有关事项见apply_async。
　　5、close()
　　　　关闭进程池（pool），使其不在接受新的任务。
　　6、terminal()
　　　　结束工作进程，不在处理未处理的任务。
　　7、join()
　　　　主进程阻塞等待子进程的退出， join方法要在close或terminate之后使用。
"""

# map的使用
"""
from multiprocessing import Pool
import time
def f(x):
    return x + x
# 需要注意是，在Windows上要想使用进程模块，就必须把有关进程的代码写if __name__ == ‘__main__’ :语句的下面，才能正常使用Windows下的进程模块。Unix/Linux下则不需要。
if __name__ == '__main__':  # 测试后发现如果不加上这句话就会报错
    now = time.time()
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3, 4, 5, 6]))
    print(f'总共用时{time.time() - now}')
"""

# apply_async的使用
"""
import multiprocessing
import time


def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end,", msg)


if __name__ == "__main__":
    # 这里设置允许同时运行的的进程数量要考虑机器cpu的数量，进程的数量最好别小于cpu的数量，
    # 因为即使大于cpu的数量，增加了任务调度的时间，效率反而不能有效提高
    pool = multiprocessing.Pool(processes=3)
    item_list = ['processes1', 'processes2', 'processes3', 'processes4', 'processes5', ]
    count = len(item_list)
    for item in item_list:
        msg = "hello %s" % item
        # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        pool.apply_async(func, (msg,))

    pool.close()
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
"""


# Queue(队列)的使用
"""
from multiprocessing import Process, Queue


def f(q):
    q.put('X' * 10)         # 将10个'x'字符放进这个队列


queue = Queue()
f(queue)
list1 = list(queue.get())         # 队列queue里的内容放到list1里面
print(list1)
"""

# 使用多进程并显示所涉及的各个进程ID
"""
from multiprocessing import Process
import os


def info(title):
    print('title:', title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    print('进程1')
    info('main line')
    p = Process(target=f, args=('bob',))
    print('进程2')
    p.start()
    p.join()
"""

# 使用多进程一个输出hello，一个输出world
"""
from multiprocessing import Process


def print_msg(msg: str):
    while 1:
        print(msg)


if __name__ == "__main__":
    msg1 = 'hello'
    msg2 = 'world'
    p1 = Process(target=print_msg, args=(msg1, ))       # 这里的args需要注意，args这个参数是一个类似于元组的东西
    p2 = Process(target=print_msg, args=(msg2, ))
    p1.start()
    p2.start()
"""

# 主进程、子进程与join方法的使用
"""
from multiprocessing import Process
import time


def child_process():
    while 1:  # 3.这里加上循环之后会发现不会运行主进程，也就是使用join方法之后主进程会等待子进程里面所有的内容运行完再运行
        time.sleep(1)       # 5.将子进程也挂起1秒，达到一种“同时运行”的效果
        print('这是子进程')


if __name__ == '__main__':
    p = Process(target=child_process)
    p.start()  # 1.这里选择start但是依旧不会先运行子进程，而是默认选择先运行主进程
    # p.join()        # 2.当这里加上join方法之后会优先运行子进程
    while 1:
        time.sleep(1)  # 4.这里主进程被挂起了，然后就运行了子进程
        print('这是主进程')
"""


