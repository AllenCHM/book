
1\. 搜索书籍
2\. 获取书籍章节详情
3\. 查看章节内容

---

**1\. 搜索书籍**
###### 接口功能
> 通过关键字搜索书

###### URL
> /api/search

###### HTTP请求方式
> GET

###### 返回格式
> JSON

###### 请求参数
> |参数|必选|类型|说明|
|:-----  |:-------|:-----|-----                               |
|kw    |ture    |string|搜索关键字                          |
|page    |flase    |int   |页数，默认为1|

###### 返回字段
> |返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|   |    |  |
|  | |                       |
| | |                         |

###### 接口示例
> 地址：[http://xxx//api/search?kw="可口可乐"&page=1](http://xxx//api/search?kw="可口可乐"&page=1)
``` javascript
[
    {
        "auth_id": "17",
        "auth_name": "皇权",
        "book_desc": "<div class=\"intro\">&#13;\n<b>&#23567;&#35828;&#20120;&#21476;&#31070;&#22675;&#31616;&#20171;&#65306;</b><br />    &#20120;&#21476;&#31070;&#22675;&#26159;&#30343;&#26435;&#20889;&#30340;&#20185;&#20384;&#20462;&#30495;&#31867;&#23567;&#35828;....&#19968;&#20010;&#33521;&#38596;&#36744;&#20986;&#30340;&#26102;&#20195;&#65292;&#27743;&#23665;&#22914;&#30011;&#65292;&#32654;&#22899;&#22914;&#20113;&#12290;\n    &#19968;&#20010;&#26411;&#26085;&#30340;&#26102;&#31354;&#65292;&#22825;&#24050;&#22833;&#36947;&#65292;&#20154;&#19981;&#22857;&#22825;&#65281;\n    &#19968;&#20010;&#34880;&#19982;&#27882;&#30340;&#19990;&#30028;&#65292;&#19968;&#20301;&#20301;&#19981;&#26429;&#22825;&#39556;&#65292;&#35889;&#20889;&#19968;&#26354;&#36870;&#22825;&#25112;&#27468;&#65281;\n&#21508;&#20301;&#20070;&#21451;&#35201;&#26159;&#35273;&#24471;&#12298;&#20120;&#21476;&#31070;&#22675;&#12299;&#36824;&#19981;&#38169;&#30340;&#35805;&#35831;&#19981;&#35201;&#24536;&#35760;&#21521;&#24744;QQ&#32676;&#21644;&#24494;&#21338;&#37324;&#30340;&#26379;&#21451;&#25512;&#33616;&#21734;&#65281;<b>&#20851;&#38190;&#35789;&#65306;</b>&#20120;&#21476;&#31070;&#22675;&#26368;&#26032;&#31456;&#33410;,&#20120;&#21476;&#31070;&#22675;&#26080;&#24377;&#31383;,&#20120;&#21476;&#31070;&#22675;&#20840;&#25991;&#38405;&#35835;.&#13;\n</div>&#13;\n",
        "book_id": "17491",
        "book_name": "亘古神墓",
        "book_status": "连载中",
        "category": "修真小说",
        "last_update": "13-12-23"
    }
]
```






---

**2\. 获取书籍章节详情**
###### 接口功能
> 通过作者id和书籍id，获取书籍章节详情

###### URL
> /api/book

###### HTTP请求方式
> GET

###### 返回格式
> JSON

###### 请求参数
> |参数|必选|类型|说明|
|:-----  |:-------|:-----|-----                               |
|auth_id    |ture    |string|作者id                          |
|book_id    |ture    |int   |书籍id|

###### 返回字段
> |返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|   |    |  |
|  | |                       |
| | |                         |

###### 接口示例
> 地址：[http://xxx/api/book?auth_id=233&book_id=233697](http://xxx/api/book?auth_id=233&book_id=233697)
``` javascript
[
    {
        "auth_id": "233",
        "book_id": "233697",
        "href": "http://xxxxxxxxxxx/api/book_content/233/233697/51112296.html",
        "id": 51112296,
        "name": "第一章 赚大发了!"
    },
    {
        "auth_id": "233",
        "book_id": "233697",
        "href": "http://xxxxxxxxx/api/book_content/233/233697/51112297.html",
        "id": 51112297,
        "name": "第二章 要你去死行不行"
    },
]
```





---

**3\. 获取书籍某章内容详情**
###### 接口功能
>

###### URL
> /api/book_content/<auth_id>/<book_id>/<content_id>.html

###### HTTP请求方式
> GET

###### 返回格式
> html

###### 请求参数
> |参数|必选|类型|说明|
|:-----  |:-------|:-----|-----                               |
|    |    ||                          |


###### 返回字段
> |返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|   |    |  |
|  | |                       |
| | |                         |

###### 接口示例
> 地址：[http://xxxxxxxxx/api/book_content/233/233697/51112296.html](http://xxxxxxxxx/api/book_content/233/233697/51112296.html)
``` javascript
<div>
</div>
```