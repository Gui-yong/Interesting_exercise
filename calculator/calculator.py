import re
import logging


class Calculator:
    def __init__(self):
        self.logger = self.log()
        self.logger.info("进入计算器")
        print("欢迎使用计算器，请遵循以下规范:")
        print("\t1.只支持加减乘除：+ - * / 的简单运算，不支持分号、根号等运算")
        print("\t2.使用英文输入法的括号：(), 不支持中括号、大括号等")
        self.run()

    def run(self):
        while True:
            x = input("请输入待计算的表达式，或者输入quit退出计算器: ")
            self.logger.info("输入：{}".format(x))
            x = x.strip()  # 首先删除输入字符串中的空格
            if x == "quit":  # 是否退出
                self.logger.info("退出计算器")
                break
            if self.check(x):  # 是否输入有误
                continue

            res = self.calculate(x)  # 计算
            print("结果：{}".format(res))
            self.logger.info("结果：{}".format(res))

    def calculate(self, x):
        while re.search("\(([^\(\)])+\)", x):  # 如果有括号，先计算括号里面的
            res = re.search("\(([^\(\)])+\)", x)  # 匹配最内层括号
            x = x.replace(res.group(0), self.calculate_(re.sub("[\(\)]", "", res.group())))  # 计算最内层括号的结果，并替换
            # print(x)
        return self.calculate_(x)

    def calculate_(self, x):
        while re.search("\d+\*[\+\-]", x):  # 这一步是找出*-或*+，如4*(25-25*-15.0-90*135.0)就会计算出错, 替换成4*(25--25*15.0-90*135.0)
            s = re.search("\d+\*[\+\-]", x).group()
            s_ = s[-1] + s[:-1]
            x = x.replace(s, s_)

        while re.search("\+\-|\-\+", x):  # 将+—或-+替换成-
            x = re.sub("\+\-|\-\+", "-", x)
        while re.search("\+\+|\-\-", x):  # 将++或--替换成+
            x = re.sub("\+\+|\-\-", "+", x)
        return self.addition_and_subtraction(x)

    def addition_and_subtraction(self, x):  # 加减，包括连加连减
        operator = re.findall("[\+\-]", x)
        start_operator = re.match("[\+\-]", x)  # 匹配是否以正负号开始，如 -90*60
        if (len(operator) < 1) or ((len(operator) == 1) and start_operator):  # 如果是以正负号开始，且只有一个元素类似-90*60
            x = self.multiply_and_divide(x)
            return x
        x_split = re.split("[\+\-]", x)

        if start_operator:  # 以正负号开始
            x_ = x.replace(start_operator.group(), "", 1)
            x_split = re.split("[\+\-]", x_)
            operator = re.findall("[\+\-]", x_)
            x_split[0] = start_operator.group() + x_split[0]

        for i in range(len(x_split)):
            x_split[i] = self.multiply_and_divide(x_split[i])

        while len(operator) > 0:
            if operator[0] == "+":
                s = float(x_split[0]) + float(x_split[1])
            else:
                s = float(x_split[0]) - float(x_split[1])
            del x_split[0: 2]
            x_split.insert(0, "{}".format(s))
            del operator[0]
        return x_split[0]

    def multiply_and_divide(self, x):  # 处理乘除，包括连乘连除，如：-45*55*68/58
        while True:
            operator = re.findall("[\*/]", x)
            if len(operator) < 1:
                break
            x_split = re.split("[\*/]", x)
            if operator[0] == "*":
                x = x.replace(x_split[0] + operator[0] + x_split[1], "{}".format(float(x_split[0]) * float(x_split[1])))
            else:
                x = x.replace(x_split[0] + operator[0] + x_split[1], "{}".format(float(x_split[0]) / float(x_split[1])))
        return x

    def check(self, x):
        """
        检查输出字符串是否有误，能判断的错误类型如下：
        1.出现除数字，加减乘除、小括号之外的字符
        2.多输入了几个运算符：如++，———，***
        3.左右括号的数目不匹配
        4.有对括号内为空
        """
        ss = ["[^0-9\+\-\*/\(\)\.]", "\-{2,}", "\+{2,}", "\*{2,}", "/{2,}", "\.{2,}"]  # 错误的字符合集
        for s in ss:
            res = re.search(s, x)
            if res:
                print("输入错误，请检查：{}".format(res.group()))
                self.logger.info("结果：输入错误，请检查：{}".format(res.group()))
                return True

        if len(re.findall("\(", x)) != len(re.findall("\)", x)):  # 判断左右括号的数目是否相等
            print("输入错误，请检查左右括号的数目")
            self.logger.info("结果：输入错误，请检查左右括号的数目")
            return True

        if re.search("\(\)", x):  # 判断是否有空的括号
            print("输入有误，有一对括号的内容为空")
            self.logger.info("结果：输入有误，有一对括号的内容为空")
            return True

        return False

    def log(self):  # 定义日志记录
        logger = logging.getLogger()  # 定义logger
        logger.setLevel(logging.INFO)  # 设置level
        file_handler = logging.FileHandler("calculator.txt", encoding="utf-8")  # 定义FileHandler，文件操作
        formatter = logging.Formatter("%(asctime)s %(filename)s [%(lineno)d] %(message)s")  # 定义Formatter
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger


if __name__ == '__main__':
    cal = Calculator()
