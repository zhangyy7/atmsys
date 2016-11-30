# atm-shop
## 简介
这是一个ATM和SHOP的组合程序，shop在结算的时候调用ATM的消费接口，ATM本身是个完整的程序，不需要调用shop
***
## 依赖环境
* Python3.5.2
* arrow：终端或命令行下执行pip3 -install arrow
***
## 运行方法：
终端或命令行下cd到程序主目录，运行python index.py
***
## 目录结构
### modules
此目录放的是业务逻辑模块,包含2个子目录credit和shopping
#### credit
此目录放的是信用卡相关的模块,包含admin、system和users三个模块
##### admin
此模块包含管理员相关的功能：创建信用卡账户、删除账户、修改账户。
##### system
此模块包含系统相关的功能：记录信用卡操作流水、计息、出账。
##### users
此模块包含信用卡用户的相关功能：取现、消费、转账、登陆、还款、存款、查账单

### utils
此目录包含一个工具模块utils，主要功能为提供通用的工具函数，主要提供如下几个功能：
* 加载json格式的文件，返回对象
* 打开文件，返回文件句柄
* 将json格式的对象dump到文件
* 将数字型的字符串转换成数字
* 判断文件是否存在，若不存在则创建文件
* 以md5方式加密字符串
* 获取上个月的今天
* 一个通用的装饰器

### db
此目录包含了信用卡和商城2个系统的数据文件，如账户信息、流水文件等。

### conf
此目录包含配置文件settings和一个模板文件templates
* settings：账单日、利率等参数
* templates：各个功能在终端展示的文字模板

### api
此目录是对modules层里面的功能做了一次封装，便于外部调用
* credit_api：对modules层的credit模块进行封装
* shopping: 对modules层的shopping模块进行封装

### bin
此目录包含了如何调用api的逻辑
* credit：实现了调用credit_api的逻辑
* shopping：实现了调用shopping_api的逻辑
* main：实现了将credit和shopping结合

### index.py
这个是程序入库文件，程序运行只能运行这个文件。

