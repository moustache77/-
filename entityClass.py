# 联系人类
class ContactPerson:
    # 联系人类的属性均为私有属性，使用getter，setter来操作这些属性
    def __init__(self, weChatId, realName, phoneNumber, sex, defaultCate, oCategory="无"):
        self.__weChatId = weChatId  # 微信号
        self.__relName = realName  # 姓名
        self.__phoneNumber = phoneNumber  # 手机号
        self.__sex = sex  # 性别
        self.__defaultCate = defaultCate  # 默认分类(汉字首字母)
        self.__oCategory = oCategory  # 自定义标签分类

    @property
    def weChatId(self):
        return self.__weChatId

    @property
    def realName(self):
        return self.__relName

    @property
    def phoneNumber(self):
        return self.__phoneNumber

    @property
    def sex(self):
        return self.__sex

    @property
    def defaultCate(self):
        return self.__defaultCate

    @property
    def oCategory(self):
        return self.__oCategory

    @oCategory.setter
    def oCategory(self, oCategory):
        self.__oCategory = oCategory

    @defaultCate.setter
    def defaultCate(self, defaultCate):
        self.__defaultCate = defaultCate

    @weChatId.setter
    def weChatId(self, weChatId):
        self.__weChatId = weChatId

    @realName.setter
    def realName(self, realName):
        self.__relName = realName

    @phoneNumber.setter
    def phoneNumber(self, phoneNumber):
        self.__phoneNumber = phoneNumber

    @sex.setter
    def sex(self, sex):
        self.__sex = sex

    def getDefaultLetter(self):
        return ord(self.__defaultCate)

    # 打印联系人对象的部分属性
    def toString(self):
        return "{微信号: " + self.weChatId + "\t" + "姓名: " + self.realName + "\t" + "手机号: " \
               + self.phoneNumber + "\t" + "性别: " + self.sex + "}"


# 通讯录类
class AddressBook:
    def __init__(self):
        self.__people = []  # 联系人列表
        self.__bestFriends = []  # 亲密朋友列表

    @property
    def people(self):
        return self.__people

    @property
    def bestFriends(self):
        return self.__bestFriends

    @people.setter
    def people(self, people):
        self.__people = people

    @bestFriends.setter
    def bestFriends(self, bestFriends):
        self.__bestFriends = bestFriends
