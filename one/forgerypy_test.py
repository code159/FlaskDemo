#encoding=utf-8
'''
    生成随机数据：
    forgery括了地理位置、日期、网络、名称等大量虚拟生成算法
'''
import forgery_py

# 地理信息(城市)
print forgery_py.address.city()
# 随机颜色
print forgery_py.basic.hex_color()
# 时间
print forgery_py.date.date(True)
# 电子邮箱
print forgery_py.internet.email_address()
# 姓名
print forgery_py.name.full_name()
# 公司
print forgery_py.name.company_name()
# 简介
print forgery_py.lorem_ipsum.sentence()