# 同济大学 人工智能
# 2151406刘卓明
# 开发时间：2022/11/17 18:47

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import matplotlib

colors_all = ["purple", "red", "forestgreen", "skyblue", "pink", "yellow", "chocolate", "greenyellow", "khaki", "aqua"]


class DictDatabase:
    len_of_DictDatabase = 0
    dic_total = []  # 创建空列表，列表中的每个元素是字典

    def __init__(self):
        self.len_of_DictDatabase = 0
        self.dic_total = list(dict() for i in range(self.len_of_DictDatabase))

    # 第一部分：基本操作
    def add(self, new_dic):
        """
        功能：增加元素
        :param new_dic: 形式为字典，是增添的元素
        """
        self.len_of_DictDatabase += 1
        self.dic_total.append(new_dic)

    def delete(self, arg1, arg2):
        """
        删除元素
        :param arg1: 是某个属性
        :param arg2: 属性对于的值
        """
        for obj in self.dic_total:
            for key_obj in obj:
                if key_obj == arg1 and obj[key_obj] == arg2:
                    self.dic_total.remove(obj)
                    self.len_of_DictDatabase -= 1
                    break

    def update(self, arg1, arg2, arg3):
        """
        用于更新某元素的值
        :param arg1: 某个属性
        :param arg2: 该属性对应的值
        :param arg3: 要修改的内容，形式为字典
        """
        new_dict = dict(arg3)  # 将第三个参数保存在了一个新的字典中
        new_list = list(new_dict.keys())  # keys的作用是将key全取出来
        num = 0
        sign = 0
        for obj in self.dic_total:
            for key_obj in obj:
                if key_obj == arg1 and obj[key_obj] == arg2:  # 找到对应的人,这里默认修改的人只有一个人
                    sign = num
                    break
            num += 1
        for i in self.dic_total[sign]:
            for j in new_list:
                if j == i:
                    self.dic_total[sign][i] = new_dict[j]

    def replace(self, arg1, arg2, arg3):
        """
        用于替换某元素的值
        :param arg1:某个属性
        :param arg2:该属性对应的值
        :param arg3: 要替换的内容，形式为字典
        """
        new_dict = arg3
        num = 0
        for obj in self.dic_total:
            for key_obj in obj:
                if key_obj == arg1 and obj[key_obj] == arg2:  # 找到对应的人
                    self.dic_total[num] = new_dict
                    break
            num += 1

    def find(self, arg1, arg2):
        """
        查找具体的某个元素
        :param arg1: 某个属性
        :param arg2: 该属性对应的值
        """
        num = 0
        for obj in self.dic_total:
            for key_obj in obj:
                if key_obj == arg1 and obj[key_obj] == arg2:
                    print(self.dic_total[num])
                    break
            num += 1

    def count(self):
        """
        :return: 返回数据库现有元素的个数
        """
        return self.len_of_DictDatabase

    def show(self, list_assign=[]):
        """
        呈现当前的数据库
        可以选择全部呈现或者是呈现某些列
        利用DataFrame实现，也可以选择呈现某些行（本函数暂未实现）
        :param list_assign: 可选参数，可以选择要查看的列，将键以列表形式输入即可
        """
        df = pd.DataFrame(self.dic_total, columns=list(self.dic_total[0].keys()))
        df.index = df.index + 1
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)

        if list_assign == []:
            print(df)
        else:
            print(df[list_assign])

    def save(self, work_file):
        """
        将数据存储到文件中
        :param work_file: 文件名
        """
        df = pd.DataFrame(self.dic_total, columns=list(self.dic_total[0].keys()))
        df.index = df.index + 1  # 让索引从1开始
        df.to_csv(work_file)

    def load(self, work_file):
        """
        用于读取文件中的数据
        :param work_file: 文件名称
        """
        dic_total = []
        df = pd.read_csv(work_file, index_col=0)  # 将csv文件读取为DataFrame形式.index_col=0保证了不会读取索引列
        # 将DataFrame转为字典形式一共有6种
        self.dic_total = df.to_dict(orient="records")  # 将DataFrame形式转化为元素为字典的列表
        self.len_of_DictDatabase = len(self.dic_total)

    # 第二部分：数值处理
    def getvalues(self, arg1, orderby=""):
        # 函数说明
        """
        用于获取数据库中所有dict的某一个属性的值
        :param arg1:是要获取的key，返回值是一个numpy的array，里面包含了数据库里所有记录中的该key的值
        :param orderby:用于指明是否要根据另一个属性的值来排序,返回的结果是一个n*2的numpy的array，
        :return:当没有第二个参数时,返回一维数组，有第二个参数时候，返回二维数组
        """
        # 分两种情况，就是有没有参数的情况，下面是没有参数的情况，返回的是一个n*1的数组
        # 获取的数组是各个字典中键arg1对应的值
        if orderby == "":
            ans = np.array([])
            for obj in self.dic_total:
                # 寻找指定的键值
                for items in obj:
                    if items == arg1:
                        ans = np.append(ans, obj[items])
            return ans
        # 下面是有参数的情况
        else:
            # 新建两个列表，第一个列表用于存放arg1对应的值，第二个列表用于存放键orderby对应的值
            ans = []
            order_ans = []
            # 下面的列表mid_dic是dic_total的copy，为了保证不改变原先的列表
            mid_dic = self.dic_total.copy()
            """
            sorted函数返回值是一个列表，其功能是对序列（列表、元组、字典、集合、还包括字符串）进行排序。
            第一个参数是迭代对象，key是用来比较，reverse代表升序还是降序
            L=[('b',2),('a',1),('c',3),('d',4)]
            sorted(L, cmp=lambda x,y:cmp(x[1],y[1]))   # 利用cmp函数
            [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
            sorted(L, key=lambda x:x[1])               # 利用key，此处是指x的第一个元素
            [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
            对于key，冒号前的是用于比较的（键），冒号后的则是键对应的值
            """
            mid_dic = sorted(mid_dic, key=lambda item: item[orderby], reverse=True)  # 根据orderby降序排序

            for obj in mid_dic:
                for items in obj:
                    if items == arg1:
                        # 将键arg1对于的元素值放入列表ans中
                        ans.append(obj[items])

                for items_order in obj:
                    if items_order == orderby:
                        # 将键orderby对于的元素放入列表order_ans中
                        order_ans.append(obj[items_order])
            # 将两个列表转换为了n*2的数组
            return np.array([order_ans, ans])

    def get_stat(self, arg1):
        # 函数说明
        """
        用于统计所有dict中某一个属性的最小值、最大值、平均值
        :param arg1:需要参与统计的属性
        :return:返回一个dict，其中包含min、max、avg三个属性
        """
        # 先利用getvalue函数将指定属性的值放在一个数组中便于处理
        ar = self.getvalues(arg1)
        # 数组中就有求最大最小平均值的函数
        x_max = ar.max()
        x_min = ar.min()
        x_avg = ar.mean()
        list_1 = ['max', 'min', 'avg']
        list_2 = [x_max, x_min, x_avg]

        return dict(zip(list_1, list_2))

    # 第三部分：绘图
    def plotLine(self, arg_X, arg_Y):
        """
        指定两个属性（属性对应的值都是数值）分别作为横轴和纵轴，绘制曲线图。例如，数据库里存有一年内每天的气温，下面的代码将画出气温随天数的变化曲线。
        :param arg_X:横轴的名称，对应的值是数值
        :param arg_Y:纵轴的名称，对应的值是数值
        """
        # 解决中文显示异常的问题以及设置画布大小和底色
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(7, 4), facecolor="lightblue")
        X, Y = self.getvalues(arg_X), self.getvalues(arg_Y)
        plt.plot(X, Y, color="blue", linewidth=1.0, label="Blue", linestyle="--", marker='.')
        plt.xlabel(arg_X, loc='right')
        plt.ylabel(arg_Y, loc='top', rotation=0)
        plt.title(arg_Y + "随" + arg_X + "变化折线图", size=15, y=1.05)
        for a, b in zip(X, Y):
            plt.text(a, b, b, ha="right", va="baseline")
        plt.xticks(X)
        plt.subplots_adjust(left=0.1, right=0.98)
        plt.show()

    def plotBars(self, arg_X, arg_Y):
        """
        这个函数是用来绘制柱形图的，
        例如，数据库里存有每个国家的名字和人口数量，下面的代码将绘制柱状图，反映每个国家人口数量的多少。
        :param arg_X:X轴的名称，对应的值是字符串
        :param arg_Y:Y轴的名称，对应的值是数值
        :return:
        """
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(10, 5), facecolor="lightblue")
        X, Y = self.getvalues(arg_X), self.getvalues(arg_Y)
        plt.xlabel(arg_X)
        colors = ["red"] * len(arg_X)
        for i in range(len(arg_X)):
            colors[i] = colors_all[i % 10]
        for a, b in zip(X, Y):
            plt.text(a, b, int(b), ha="center", va="bottom")  # x,y文本所在位置，s为显示内容，ha水平对齐方式，va垂直对齐方式
        plt.title(arg_Y + "分数统计图", size=15, y=1.05)
        plt.bar(X, Y, width=0.5, color=colors)
        plt.title("参与统计总人数为:" + str(self.len_of_DictDatabase), y=1.05, size=12, loc='left')
        plt.show()

    def plotPie(self, arg_1, arg_list):
        # 函数说明
        """
        绘制饼状图，反映该属性的值位于每个区段的百分比。
        例如，数据库里存着每位同学的成绩分数，下面的代码将画出位于各个分数区间的人数
        :param arg_1:是一个属性（属性对应的值是数值）
        :param arg_list:代表了统计区段的分隔点
        """
        # 解决中文显示异常的问题以及设置画布大小和底色
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(6, 5), facecolor="lightblue")

        num = len(arg_list) + 1
        data = self.getvalues(arg_1)
        labels = [''] * num
        new_data = []
        colors = ["red"] * num
        explode = [0] * num
        explode[0] = 0.1  # 突出显示一下最低分数段的人

        # 这个循环是为了统计出各分数段的人数

        for i in range(len(arg_list)):
            if i == 0:
                new_data.append(np.count_nonzero(data < arg_list[i]))
            else:
                low = (np.count_nonzero(data < arg_list[i - 1]))
                hign = (np.count_nonzero(data < arg_list[i]))
                new_data.append(hign - low)
        new_data.append(np.count_nonzero(data >= arg_list[len(arg_list) - 1]))

        # 各个扇形的颜色划定

        for i in range(num):
            colors[i] = colors_all[i % 10]

        # 下面的部分是为了标明各个扇形的标签

        for i in range(num):
            if i == 0:
                labels[i] = str(0) + '-' + str(arg_list[0]) + '分'
            elif i == num - 1:
                if arg_list[i - 1] == 100:
                    labels[i] = '100分'
                else:
                    labels[i] = str(arg_list[i - 1]) + '-100分'
            else:
                labels[i] = str(arg_list[i - 1]) + '-' + str(arg_list[i]) + '分'

        plt.title(arg_1 + "各分数段人数统计", size=15)
        plt.title("参与统计总人数为:" + str(self.len_of_DictDatabase), y=0, size=12, loc='left')
        plt.pie(new_data, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', startangle=90,
                counterclock=False)
        plt.show()

    def plotPoints3D(self, name1, name2, name3, name4=''):
        # 函数说明
        """
        绘制三维图
        :param name1:x轴属性
        :param name2:y轴属性
        :param name3:z轴属性
        :param name4:可选参数，决定前三个参数是否要根据第四个元素来涂色
        """
        # 创建Axes3D主要有两种方式，一种是利用关键字projection='3d'来实现(此处采用了这种做法）
        # 另一种则是通过从mpl_toolkits.mplot3d导入对象Axes3D来实现，目的都是生成具有三维格式的对象Axes3D
        # 设置图像的大小，背景色，边框等属性
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(6, 5), facecolor="lightblue", edgecolor="black", frameon=True)
        rect = [0, 0.1, 0.9, 0.8]
        ax = plt.axes(rect, projection='3d')

        X = np.array(self.getvalues(name1).tolist())  # tolist()将矩阵转化为列表
        Y = np.array(self.getvalues(name2).tolist())
        Z = np.array(self.getvalues(name3).tolist())
        Q = self.getvalues(name4).tolist()
        if name4 == "":
            ax.scatter3D(X, Y, Z)
        else:
            im = ax.scatter3D(X, Y, Z, c=Q, cmap="rainbow", marker='o')
            fig.colorbar(im, format=matplotlib.ticker.FuncFormatter(lambda x, pos: int(x)), fraction=0.05, pad=0.11)

        # 自己添加的部分，指是否画出折线、曲面图
        # axis.plot3D(X,Y,Z,'gray') # 画出空间折线
        # X_1,Y_1=np.meshgrid(X, Y)
        # Z_1 = X*0+Y*0+Z
        # ax.plot_surface(X_1,Y_1,np.expand_dims(Z_1, axis=0), cmap="rainbow") # 需要将z扩展成二维
        plt.title(name1 + '-' + name2 + '-' + name3 + "三维图", size=15)
        plt.xlabel(name1)
        plt.ylabel(name2)
        ax.set_zlabel(name3)
        plt.show()


# 菜单函数
def menu():
    print("""
                1.增加元素
                2.删除元素
                3.更新元素
                4.替换元素
                5.查找元素
                6.元素个数
                7.存储到文件
                8.读取文件
                a.getvalues
                b.getStat
                x.绘制折线图
                y.绘制柱形图
                z.绘制饼图
                d.绘制3D图                
                q.显示当前的数据库
                0.退出
                """)
    ddb = DictDatabase()
    while 1:
        print("请选择需要的功能：")
        prime = input()
        if prime == '0':
            break
        elif prime == '1':
            print("请输入增加的元素（以字典形式，为方便处理，请把学号以数字输入，不要带引号")
            ddb.add(json.loads(input()))
        elif prime == '2':
            print("请输入要删除的元素（某个键及其的值）")
            ddb.delete(input(), input())
        elif prime == '3':
            print("请输入要更新的元素，前两个参数为某个键及其的值，第三个参数请以字典的形式输入，为要更新的内容")
            ddb.update(input(), input(), json.loads(input()))
        elif prime == '4':
            print("请输入要替换的元素，前两个参数为某个键及其的值，第三个参数请以字典的形式输入，为要替换的元素")
            ddb.replace(input(), input(), json.loads(input()))
        elif prime == '5':
            print("请输入要查找的元素，两个参数为某个键及其的值")
            a = input()
            b = input()
            print(a + "为" + b + "的人的信息为：")
            ddb.find(a, b)
        elif prime == '6':
            print("元素的总个数为：", ddb.count())
        elif prime == '7':
            print("请输入保存的文件名")
            ddb.save(input())
        elif prime == '8':
            print("请输入文件名称")
            ddb.load(input())

        elif prime == 'a':
            print("请输入需要统计的属性（以及orderby）")
            ddb.getvalues(input(), input())  # 此处注意，如果只输入一个参数时候，第二个多敲一下回车
        elif prime == 'b':
            print("请输入需要查看的属性")
            a = input()
            print(a + "的最大值、最小值、平均值为：")
            print(ddb.get_stat(a))

        elif prime == 'x':
            print("请输入横轴和纵轴对应的属性")
            ddb.plotLine(input(), input())
        elif prime == 'y':
            print("请输入对应的属性")
            ddb.plotBars(input(), input())
        elif prime == 'z':
            print("请输入需要统计的属性以及分数区间分隔点，分隔点请以列表形式输入")
            ddb.plotPie(input(), eval(input()))
        elif prime == 'd':
            print("请依次输入三个轴的属性（以及第四个属性）")
            ddb.plotPoints3D(input(), input(), input(), input())

        elif prime == 'q':
            print("当前的数据库为：")
            ddb.show()


# 测试所有的功能
def trial():
    ddb = DictDatabase()
    ddb.load("grade.csv")  # 导入数据
    print('成绩列表如下')
    ddb.show()  # 显示一下目前的数据库
    ddb.add({'id': 20190017, 'name': '旺财', 'age': 15, '高数': 99,
             '线代': 90, '模电': 72, '概率论': 77,
             '马原': 93, '离散': 50, '数据结构': 59})  # 增加元素
    print('增添了一位同学')
    ddb.show()  # 显示一下目前的数据库
    ddb.delete('name', '张三')  # 删除元素
    print('张三同学转专业了，删除掉')
    ddb.show()  # 显示一下目前的数据库
    print('修改了李华同学的成绩')
    ddb.update('name', '李华', {'数据结构': 89})  # 更新元素
    ddb.show()  # 显示一下目前的数据库
    print("高数满分的同学的信息为：")
    ddb.find('高数', 100)  # 查找高数满分的人
    print("元素个数为：")
    print(ddb.count())  # 统计元素个数
    print("将学号为007的同学换成了023的")

    # 此处特别特别注意，从csv文件读取出来的学号，而自己输入的是字符串类型（有引号的）这可能会导致寻找不到的问题，
    # 所以为了不出现bug，全改成数字类型
    ddb.replace('id', 20190007, {'id': 20190023,
                                 'name': '李龙', 'age': 23, '高数': 73, '线代': 80,
                                 '模电': 75, '概率论': 82, '马原': 90,
                                 '离散': 74, '数据结构': 78})  # 替换元素
    ddb.show()
    ddb.save("update.csv")  # 将修改后的数据库存到新文件中

    print("模电成绩如下：")
    print(ddb.getvalues("模电"))  # 打印出所有模电的成绩
    print("根据数据结构排的模电成绩")
    print(ddb.getvalues("模电", "数据结构"))  # 根据数据结构排的模电成绩
    print("离散的最大，最小，以及平均分")
    print(ddb.get_stat("离散"))  # 返回离散的最大，最小，以及平均分

    ddb.plotBars("name", "概率论")  # 画出不同同学的概率论成绩的条形图
    ddb.plotPie("线代", [60, 70, 80, 90])  # 画出线代的各个分数段的饼图，并突出显示不及格的
    dds = DictDatabase()
    dds.load("tianqi.csv")
    dds.plotLine("日期", "温度")  # 画出天气随温度变化的折线图

    ddb.plotPoints3D("高数", "线代", "离散", "概率论")  # 画出三维图，根据第四个元素赋予颜色


# 想要交互时可去掉菜单函数前面的注释符号
# menu()
trial()

# 未完待续
