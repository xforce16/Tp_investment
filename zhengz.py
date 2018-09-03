import re

url='https://www.qichacha.com/firm_f1c5372005e04ba99175d5fd3db7b8fc.html'
href = re.search(r"_(.*)\.", url).group(0)
href1 = href.replace("_","").replace(".","")
print(href1)

text = '{"success":{"results":[{"columns":["value"],"data":[{"graph":{"nodes":[{"id":"45722246","labels":["Company"],"properties":{"keyNo":"c7f10d1209b075d7e2943df4b2bb97cc","registCapi":"100000.0","name":"\u82cf\u5dde\u7eaa\u6e90\u6e90\u661f\u80a1\u6743\u6295\u8d44\u5408\u4f19\u4f01\u4e1a(\u6709\u9650\u5408\u4f19)","econKind":"\u6709\u9650\u5408\u4f19\u4f01\u4e1a","hasImage":false,"status":"\u5728\u4e1a"}},{"id":"55433993","labels":["Company"],"properties":{"keyNo":"f24c7c973dff8630029c82d9b7247357","registCapi":"2000.0","name":"\u5317\u4eac\u641c\u72d7\u4fe1\u606f\u670d\u52a1\u6709\u9650\u516c\u53f8","econKind":"\u5176\u4ed6\u6709\u9650\u8d23\u4efb\u516c\u53f8","hasImage":true,"status":"\u5728\u4e1a"}},{"id":"62850010","labels":["Person"],"properties"'
print(text)