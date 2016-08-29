import json

decodejson = json.loads('{"name":"haha"}')

print(decodejson)

def getCategoryId(url):
    idx = url.index("categoryId=") + 11
    id = url[idx:]
    return id
    
url = "http://android.myapp.com/myapp/category.htm?orgame=1&categoryId=-10"
categoryId = getCategoryId(url)
print(categoryId)


for index in [0,1,2,3,4]:
    url = "http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=%s&pageSize=20&pageContext=%d" % (categoryId,40 + index*20)
    print(url)