﻿﻿﻿﻿﻿﻿﻿﻿
# 南方科技大学2019年春计算机创新实验

组员：陈德缘，卢致睿，杨宇杰
## 更新日志
* 2019.5.02 完成了所有系，部分提高自动化程度
* 2019.4.25 修改了不合理的命名，部分系提高自动化程度
* 2019.4.23 更新环境学院
* 2019.4.20 更新海洋系，计系
* 2019.4.14 根据余老师的建议，使用scrapy框架重构了整个爬虫,并增加了备份功能
* 2019.4.03 再次修改了输出
* 2019.3.30 修复了电子系一些奇奇怪怪的时间问题
* 2019.3.21 应甲方要求，修改输出结构，统一时间输出
* 2019.3.20 更新电子系、材料系，完善结构，修复一个bug
* 2019.3.19 更新地空系
* 2019.3.18 更新化学系，完善整体结构，提出共用部分作为头文件，修改Error_message.txt结构以利于debug
## 使用须知
### run.bat
- 双击改文件即可重运行所有爬虫，如果需要单独运行，请在命令行下输入:

> scrapy crawl Math
>
>Math should be replaced by the spiders name


- python版本为3.7.0
- 需求scrapy扩展，如果没有，请运行

> pip install scrapy

- 测试环境为Windows 10 家庭中文版
- 对于每一个系，会生成一个的csv文件，如**Math.csv**

## 联系我
如果有什么使用问题，或者出现错误，请联系我

> QQ 654826118
>
> Mail 11612814@mail.sustech.edu.cn
































