`！！！工程初步立项中，本页面可能有重大变动！！！`
# Universal Config Interface
**Universal Config Interface 统一配置接口（UCI）致力于解决当今配置文件普遍存在的以下问题：**

1. 尽管配置文件的实质内容基本相同，但其格式五花八门。
>- 传统的 INI
>- 经典的 XML
>- 通用的 JSON
>- 直观的 YAML
>- 年轻的 TOML

2. 缺乏直观的、图形化的方式来辅助配置文件的编写。
>  `setting1=true`
> - [x] setting2
> 
> setting2 明显比 setting1 更适合用户。

3. 配置文件中的具体设置项缺乏强有力的约束，软件开发者需要为此编写代码，对设置项进行有效性检测。
> 配置文件中需要一个*邮箱地址*，但一个小白用户在这里**错误地**填写了他的*手机号。这时如果软件不检测其有效性，直接读取配置文件内容并直接用于发送邮件，就会出现问题。

---
# 特性
## 1. Universal Format
>广泛的格式支持

- [x] TOML
- [x] YAML
- [x] JSON
- [x] XML
- [ ] INI

## 2. Config View
>直观的用户界面

- [ ] FastAPI
- [ ] Sanic
- [ ] Material Design
- [ ] AwesomeFont

## 3. Interface Manipulation
>规范的操作接口
- [ ] arrow 时间及日期
- [ ] furl URL字符串
- [ ] ipaddress IP地址


# 技术

UCI 以 Python 为开发语言，选取 JSON 作为核心格式，辅以 JSON Schema 进行约束。

>考虑到配置文件的内容一般相对简单，故而**当前版本暂未将性能作为重点考量的方面**。

核心的基本工作方式是以对应的解码器将配置文件转换为通用的 Python dict 对象，在需要时再利用编码器输出。

~~`XD 好吧我承认这些都是为了偷懒`~~

