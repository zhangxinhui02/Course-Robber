# 选课脚本

适用于某重庆门大学选课系统的选课脚本，可配置较复杂的选课条件，助你选到心仪的课程。

![CQUPT](https://mikumikumi.oss-cn-chengdu.aliyuncs.com/mikumikumi.pic/1688063698093.jpeg.jpeg)

---

## 特色

- 使用YAML文件配置脚本，可读性好，易于编辑。

- 支持按课程名选择、优先按老师选择、强制按老师选择、课程类型范围指定、选课服务器指定、随机休眠避免被请去喝茶、预选课与候选课休眠时间分别指定。

- 代码分层分包、面向对象编写。

- 容器化打包。

## 使用方法

提供直接使用和Docker部署两种方法。使用之前请保证你的设备连接了CQUPT内网。

### 直接使用

首先保证你的操作系统上安装了Python3和Git。

```shell
git clone https://github.com/zhangxinhui02/Course-Selection-Script.git
cd Course-Selection-Script/Src
python -m pip install -r requirements.txt
cd config
```

按自己的需求修改`Course-Selection-Script/Src/config`目录下的`config.yaml`文件。

```shell
cd ..
# 回到Course-Selection-Script/Src目录
python main.py
```

### Docker部署

新建一个空文件夹`Volume-CourseSelectionScript`用于存储配置文件并挂载到容器。

进入此文件夹，新建`config.yaml`文件夹。将[示例配置文件](https://github.com/zhangxinhui02/Course-Selection-Script/blob/main/Src/config/config.yaml)的内容复制到此文件中并按需修改。

```shell
# 回到Volume-CourseSelectionScript目录
docker run -v .:/app/config zhangxinhui02/course-selection-script:latest
```

## 注意事项

- Cookies不要泄露给别人。

- 选课信息采用dict类型存储。

  键名为要选的课程的完整名称，对应的字符串值指定了如何选择老师。

  1. 空字符串表示不指定老师，只要能选到这门课就好。

  2. 字符串中填入老师的名字，表示要选这门课就只选这位老师的课，如果选不到就不选了。
     
     可以填入多位老师的名字，以空格分隔，表示选这些老师中任意一者的课，如果都选不到就不选了。

  3. 字符串中填入老师的名字，名字前紧跟一个星号`*`，表示优先选这位老师的这门课，如果选不到就去选其他老师的这门课。
     
     可以填入多位老师的名字加星号，以空格分隔，表示优先选这些老师的课，如果都选不到就去选其他老师的这门课。

  4. 上述2和3项是相冲突的，即字符串值内不能既有带星号的名字又有不带星号的名字。如果出现了这种情况，只考虑不带星号的名字。

- 课程类型指定了脚本启动时获取课程列表所能获取到的类型，默认的四个值涵盖了所有类型的正常课程，即脚本可以尝试选择所有课程，因此一般无需修改。分别对应：专业必修课、交叉通识课（人文社科）、交叉通识课（自然科学）、重修。

  如果删除了某一类型，则脚本启动时获取课程列表就无法获取这一类型的课程，因此也就无法匹配选择到这一类型的课程。

- 时间间隔范围的设置是为了避免连续高频率的提交造成的网络负担过重，同时也是为了减小由于大量流量而被校方注意到的概率。脚本会在时间范围内取一随机浮点值，在两次提交操作之间等待。

  1. 当选课正式开始之前，脚本会以较低频率循环尝试获取课程列表，此时的时间间隔范围采用较大的`sleep_range`。

  2. 一旦成功获取到了课程列表，表示已经开放选课，此时脚本按配置文件处理筛选课程，得出应提交的课程数据，随后遍历提交这些课程数据，称为“预选”，此时的时间间隔范围采用较小的`prefer_sleep_range`以抢课。

  3. 遍历完成之后若存在失败的选课，基本是由于课程冲突、学分不够或人数已满造成的。此时脚本会以较低频率循环遍历尝试重选这些失败的课程（等待别人退课），称为“候补”，此时的时间间隔范围采用较大的`sleep_range`。

  调整时间间隔就可以控制提交选课的速度。如果设置过低的时间间隔导致大量非正常流量，有很大可能会被校方打击。

---

此脚本仅供学习交流之用，出现问题作者不承担任何责任。

可能存在未发现的bug，校方接口可能发生变动，由此可能导致无法自动选课，故请不要过于依赖本脚本，出现任何选课失误作者概不负责。

开源协议：[MIT License](https://github.com/zhangxinhui02/Course-Selection-Script/blob/master/LICENSE)