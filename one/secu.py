#encoding=utf-8
from werkzeug.security import generate_password_hash,check_password_hash

ctx="123"
print "明文",123
pwd=generate_password_hash(ctx)
print "密文",pwd
print "是否一致",check_password_hash(pwd, ctx)