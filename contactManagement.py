from entityClass import ContactPerson, AddressBook
from utils import getFirstLetter
import csv
import time, re


# 微信通讯录管理类
class ContactManagement:
    def __init__(self):
        self.addressBook = None
        # 为了测试方便，加入三个自定义标签
        self.labels = ["家人", "同学", "朋友"]

    # 进入系统强制创建通讯录
    def createList(self):
        print("欢迎使用微信通讯录系统")
        print("请先创建通讯录（1:是  输入其他任意键:否）")
        if input() == "1":
            # 实例化通讯录
            self.addressBook = AddressBook()
            print("通讯录已创建完毕")
            # sample 1-7为测试数据，为了调试程序
            sample1 = ContactPerson("skdaq_wwlsk", "久久", "18717039092", "男", "J", "同学")
            self.addressBook.people.append(sample1)
            sample2 = ContactPerson("kdsdals", "蛙蛙", "15116039732", "男", "W")
            self.addressBook.people.append(sample2)
            sample3 = ContactPerson("sdalskd", "张伟", "13317039077", "男", "Z", "同学")
            self.addressBook.people.append(sample3)
            sample4 = ContactPerson("salsk_d", "豪哥", "19117079532", "男", "H", "朋友")
            self.addressBook.people.append(sample4)
            sample5 = ContactPerson("sk_daqskd", "林一", "14110390320", "女", "L")
            self.addressBook.people.append(sample5)
            sample6 = ContactPerson("dkjdkja", "林新", "17887039034", "男", "L")
            self.addressBook.people.append(sample6)
            sample7 = ContactPerson("qqqghq__", "林新", "16091296087", "女", "L", "家人")
            self.addressBook.people.append(sample7)
            time.sleep(0.7)
            # 建立通讯录后，进入主菜单
            self.openMenu()
            print("-----------------")
        else:
            print("感谢使用!")
            return

    # 主菜单
    def openMenu(self):
        while True:
            print("------------------微信通讯录系统---------------------")
            print("1.添加联系人")
            print("2.删除联系人")
            print("3.查找联系人")
            print("4.显示微信通讯录的内容")
            print("5.分类管理联系人")
            print("6.退出系统")
            index = input("请选择：")
            if index == "1":
                self.addPerson()
            elif index == "2":
                self.deletePerson()
            elif index == "3":
                self.searchPerson()
            elif index == "4":
                self.findAll()
            elif index == "5":
                self.categoryPerson()
            elif index == "6":
                print("感谢使用,再见!")
                return
            else:
                print("sb，选数字还不会")
                time.sleep(0.7)

    # 添加联系人
    def addPerson(self):
        print("-" * 20)
        index = input("1.手动添加 2.外部导入\n")
        if index == "1":
            self.addPersonByHand()
        elif index == "2":
            self.addImportPerson()
        else:
            print("输入错误!")
            time.sleep(0.5)
            return

    # 手动添加联系人
    def addPersonByHand(self):
        print("----------添加联系人------------")
        weChatId = input("请输入对方微信Id：（6-20位字母、数字、下划线，数字下划线不开头）\n")
        # 校验输入的微信号是否已经存在列表中
        while weChatId == self.addressBook.people[self.searchPersonByIdWithParam(weChatId)].weChatId:
            print("微信号已存在")
            weChatId = input("请输入对方微信Id：")
            # 使用正则表达式校验微信号格式是否正确
            while re.match("^[a-zA-Z]\w{5,19}$", weChatId) is None:
                print("微信号输入不正确，请重新输入!")
                weChatId = input("请输入对方微信Id：")
        while re.match("^[a-zA-Z]\w{5,19}$", weChatId) is None:
            print("微信号输入不正确，请重新输入!")
            weChatId = input("请输入对方微信Id：")
            while weChatId == self.addressBook.people[self.searchPersonByIdWithParam(weChatId)].weChatId:
                print("微信号已存在")
                weChatId = input("请输入对方微信wId：")
        realName = input("请输入对方姓名：")
        # 正则表达式校验姓名是否正确（2-4个汉字）
        while re.match("^[\u4e00-\u9fa5]{2,4}$", realName) is None:
            print("姓名输入不正确，请重新输入!")
            realName = input("请输入对方姓名：")
        # 获得第一个汉字的首字母
        defaultCate = getFirstLetter(realName)
        phoneNumber = input("请输入对方手机号：(+86) ")
        # 正则表达式校验手机号是否正确
        while re.match("^[1][3-9]([0-9]{9})$", phoneNumber) is None:
            print("手机号格式不正确，请重新输入!")
            phoneNumber = input("请输入对方手机号：(+86) ")
        sex = input("请输入对方性别：(男或女) ")
        # 正则表达式校验性别是否正确
        while re.match("^(男|女)$", sex) is None:
            print("性别输入不正确，请重新输入!")
            sex = input("请输入对方性别：")
        contactPerson = ContactPerson(weChatId, realName, phoneNumber, sex, defaultCate)
        # 放入通讯录联系人列表
        self.addressBook.people.append(contactPerson)
        print("添加成功!")
        time.sleep(0.5)

    # 从外部导入添加联系人
    def addImportPerson(self):
        try:
            csv_reader = csv.reader(open("data/data.csv"))
            for row in csv_reader:
                cp = ContactPerson(row[0], row[1], row[2], row[3], getFirstLetter(row[1]))
                if row[0] == self.addressBook.people[self.searchPersonByIdWithParam(row[0])].weChatId:
                    print("微信号" + row[0] + "已经导入")
                    continue
                self.addressBook.people.append(cp)
            print("已经全部导入!")
            time.sleep(0.5)
            self.findAll()
        except:
            print("读取失败!")
            time.sleep(0.5)

    # 按姓名的首字母对联系人列表冒泡排序
    def sortByLetter(self):
        people = self.addressBook.people
        for i in range(len(people) - 1, -1, -1):
            for j in range(i):
                if people[j].getDefaultLetter() > people[j + 1].getDefaultLetter():
                    people[j], people[j + 1] = people[j + 1], people[j]
        return people

    # 删除联系人
    def deletePerson(self):
        if len(self.addressBook.people) == 0:
            print("当亲通讯录暂无联系人，请先添加联系人")
            time.sleep(0.5)
            return
        n = input("输入你要删除的学生查询方式:\n1:按微信号查找 2.按姓名查找")
        if n == "1":
            index = self.searchPersonByID()
        elif n == "2":
            index = self.searchPersonByName()
        else:
            print("输入错误!")
            time.sleep(0.5)
            return
        if index == -1:
            return
        del self.addressBook.people[index]
        print("删除成功!")
        time.sleep(0.5)
        self.findAll()

    # 查找联系人
    def searchPerson(self):
        if len(self.addressBook.people) == 0:
            print("当亲通讯录暂无联系人，请先添加联系人")
            time.sleep(0.5)
            return
        n = input("1.根据微信号搜索 2.根据姓名搜索\n")
        if n == "1":
            index = self.searchPersonByID()
        elif n == "2":
            index = self.searchPersonByName()
        else:
            print("输入错误!")
            time.sleep(0.5)
            return
        if index == -1:
            return
        contactPerson = self.addressBook.people[index]
        print(contactPerson.toString())
        time.sleep(0.5)

    # 根据微信号查找联系人，顺序查找算法
    def searchPersonByID(self):
        weChatId = input("请输入要查询的微信号: ")
        for i in range(len(self.addressBook.people)):
            if self.addressBook.people[i] is None:
                print("通讯录为空")
                return -1
            if weChatId == self.addressBook.people[i].weChatId:
                return i
        print("对不起，没有找到相应的联系人")
        time.sleep(0.5)
        return -1

    # 根据微信号查找联系人，ID自动传入
    def searchPersonByIdWithParam(self, weChatId):
        for i in range(len(self.addressBook.people)):
            if weChatId == self.addressBook.people[i].weChatId:
                return i
        return 0

    # 根据姓名查找联系人
    def searchPersonByName(self):
        name = input("请输入要查询的姓名: ")
        arr = len(self.addressBook.people) * [False]
        count = 0
        index = -1
        for i in range(len(self.addressBook.people)):
            if self.addressBook.people[i] is None:
                print("通讯录为空")
                return -1
            if name == self.addressBook.people[i].realName:
                arr[i] = True
                count += 1
        if count == 0:
            print("对不起，没有找到相应的联系人")
            time.sleep(0.5)
        elif count == 1:
            for i in range(len(arr)):
                if arr[i]:
                    index = i
                    break
        else:
            print("符合条件的联系人如下: ")
            for i in range(len(self.addressBook.people)):
                if arr[i]:
                    cp = self.addressBook.people[i]
                    print(cp.toString())
            print("请选择上面符合条件的微信号")
            index = self.searchPersonByID()
        return index

    # 显示通讯录所有内容
    def findAll(self):
        if len(self.addressBook.people) == 0:
            print("当前通讯录为空,请添加联系人!")
            return
        print("-" * 100 + "\n特别关心：")
        # 显示特别关心分类的所有内容
        self.getSpecFriends()
        people = self.sortByLetter()
        flag = people[0].defaultCate
        print("*" * 100)
        print("默认分类：")
        print("# " + flag + ":")
        for i in people:
            if i.defaultCate != flag:
                print("# " + i.defaultCate + ":")
            print(i.toString())
            flag = i.defaultCate
        print("*" * 100)
        print("自定义标签：")
        # 显示自定义分类的所有内容
        self.getSpecList()

    # 分类管理
    def categoryPerson(self):
        print("1.自定义标签分类 2.特别关心分类管理 ")
        n = input("请选择：")
        if n == "1":
            self.categoryByYourself()
        elif n == "2":
            self.adminSpec()
        else:
            print("输入错误!")
            time.sleep(0.5)
            return

    # 特别关心分类管理
    def adminSpec(self):
        people = self.addressBook.people
        n = input("1.添加特别关心 2.移除特别关心 3.查看特别关心 ")
        if n == "1":
            print("联系人姓名可在通讯录中查看")
            index = self.searchPersonByName()  # 查找联系人
            if index == -1:
                return
            self.addressBook.bestFriends.append(people[index])  # 将找到的联系人放入特别关心
            print("添加成功!")
            time.sleep(0.5)
        elif n == "2":
            if len(self.addressBook.bestFriends) == 0:
                print("还没有特别关心联系人")
                time.sleep(0.5)
                return
            print("特别关心如下：")
            for i in range(len(self.addressBook.bestFriends)):
                print(self.addressBook.bestFriends[i].toString())
            weChatId = input("请输入要移除特别关心分类的微信号：")
            for i in range(len(self.addressBook.bestFriends)):
                if self.addressBook.bestFriends[i].weChatId == weChatId:
                    del self.addressBook.bestFriends[i]
                    print("移除成功!")
                    time.sleep(0.5)
                    self.findAll()
                    break
        elif n == "3":
            self.getSpecFriends()
        else:
            print("输入错误!")
            time.sleep(0.5)

    # 显示所有特别关心分类
    def getSpecFriends(self):
        if len(self.addressBook.bestFriends) == 0:
            print("无特别关心联系人")
            time.sleep(0.5)
            return
        for i in range(len(self.addressBook.bestFriends)):
            print(self.addressBook.bestFriends[i].toString())

    # 自定义分类
    def categoryByYourself(self):
        n = input("1.添加操作 2.移除操作 3.查看分类标签和联系人 ")
        if n == "1":
            self.addCateLabel()
        elif n == "2":
            self.deleteCateLabel()
        elif n == "3":
            self.getSpecList()
        else:
            print("输入错误!")
            time.sleep(0.5)

    # 显示所有自定义标签以及对应的联系人
    def getSpecList(self):
        if len(self.labels) == 0:
            print("无")
            time.sleep(0.5)
            return
        for la in self.labels:
            print("# " + la + ":")
            for i in range(len(self.addressBook.people)):
                if self.addressBook.people[i].oCategory == la:
                    print(self.addressBook.people[i].toString())

    # 自定义标签添加操作
    def addCateLabel(self):
        n = input("1.新建标签 2.将联系人加入指定标签 ")
        if n == "1":
            labelName = input("请输入标签名：")
            while labelName in self.labels:
                print("该标签已存在")
                labelName = input("请重新输入标签名：")
            self.labels.append(labelName)
            print("创建成功!")
            time.sleep(0.5)
        elif n == "2":
            if len(self.labels) == 0:
                print("还没有创建标签哦")
                time.sleep(0.5)
                return
            print("已创建的标签如下：")
            for c in self.labels:
                print(c)
            la = input("请选择一个标签 ")
            while la not in self.labels:
                print("标签输入错误,请重新输入!")
                la = input("请选择一个标签 ")
            index = self.searchPersonByName()
            if index == -1:
                return
            self.addressBook.people[index].oCategory = la
            print("添加成功!")
            time.sleep(0.5)
        else:
            print("输入错误!")
            time.sleep(0.5)

    # 自定义标签删除操作
    def deleteCateLabel(self):
        n = input("1.删除标签 2.将联系人移出指定标签 ")
        if n == "1":
            if len(self.labels) == 0:
                print("还没有创建标签哦")
                time.sleep(0.5)
                return
            print("已创建的标签如下：")
            for c in self.labels:
                print(c)
            labelName = input("请输入要删除的标签名：")
            if labelName not in self.labels:
                print("标签不存在!")
                time.sleep(0.5)
                return
            choice = input("删除标签可能会删除自定义分组，确认继续删除吗? \n1.是  任意输入.否 ")
            if choice == "1":
                for i in range(len(self.addressBook.people)):
                    if self.addressBook.people[i].oCategory == labelName:
                        self.addressBook.people[i].oCategory = "无"
                self.labels.remove(labelName)
                print("删除标签成功!")
                time.sleep(0.5)
                self.getSpecList()
            else:
                return
        elif n == "2":
            if len(self.labels) == 0:
                print("还没有创建标签哦")
                time.sleep(0.5)
                return
            print("已创建的标签如下：")
            for c in self.labels:
                print(c)
            la = input("请选择一个标签: ")
            while la not in self.labels:
                print("标签输入错误,请重新输入!")
                la = input("请选择一个要删除的标签 ")
            index = self.searchPersonByName()
            if index == -1:
                return
            self.addressBook.people[index].oCategory = "无"
            print("从自定义标签中删除成功!")
            time.sleep(0.5)
            self.getSpecList()
        else:
            print("输入错误!")
            time.sleep(0.5)
