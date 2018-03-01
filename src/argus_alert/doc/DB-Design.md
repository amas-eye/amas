# 表设计

## 配置表

- 表名：config:xxx
- 类型：哈希表
- 4张表：默认/开发/测试/生产
    - config:default
    - config:dev
    - config:test
    - config:prod
- 元素：
    - 与bootstrap.py配置字段一致
    
    
## 告警策略
    

### 策略表
- 表名：strategy
- 类型：列表
- 元素：
    - id

### 策略属性
- 表名：strategy:[id]
- 类型：哈希表
- 元素：
    - name
    - type（基本告警/复杂告警...）
    - create_time
    - update_time
    - create_user
    - expr(tsd query string)
    - metric
    - aggregate（聚合方法）
    - start_time
    - end_time
    - sample（取样方法）
    - comparison（>,<,=之类的）
    - threshold（阈值）
    - check_interval（单位：秒）
    - on_off（1代表on，0代表off）
    - level（1-2-3，代表低-中-高）
    - notify
    - recover
    - tag
    - group（策略组）


### 状态管理(状态变化即触发告警)
- 表名：```strategy:[id]:state```
- 类型：有序集合
- 元素：
    - <timestamp> 
    - <state info> [OK|ALERT]@<timestamp>


- 表名：```strategy:[id]:[group]:state```
- 类型：有序集合
- 元素：
    - <timestamp> 
    - <state> [OK|ALERT]@<timestamp>__INFO__<info>

- 表名：```strategy:[id]:[group]:state:info```
- 类型：哈希表
- 元素： 
   - <timestamp>: <info>
    

### 通知处理
- 表名：strategy:notify
- 类型：列表
- 元素：
    - id


- 表名：strategy:notify:[id]
- 类型：哈希表
- 元素：
    - msg_template
    - msg_to
    - db[default]
        - MongoDB
        - HBase
    - wechat
    - mail
    - api
    - ...

### 自愈行为
- 表名：strategy:recover
- 类型：列表
- 元素：
    - id

 
- 表名：strategy:recover:[id]
- 类型：哈希表
- 元素：
    - script
    - callback
        
        
        
## 通知队列

- 告警事件
    - notice:*
    - db/wechat/mail/api/...各种通知方式对应一个topic发布渠道
    - 订阅端起对应topic的通知处理worker
    - 发布端、订阅端都可以做告警收敛
    - 每一个发布的消息，都是json序列化的字符串，包含了告警事件的详细内容
- 操作指令
    - cmd:*
    - 重载告警策略，topic为cmd:reload_strategy


# Redis持久化策略

- AOF
- BGREWRITEAOF（每天）


# 告警历史数据持久化设计

Redis默认保存一段时间内的告警数据，超过一个月(时间段可配置)的数据会异步进行持久化。  
- 存储选型一：本地文件系统
- 存储选型二：写HBase
- 存储选型三：写Elasticsearch

# 性能数据存储
## 队列
- 表名：_manager:task
- 类型：哈希表
- 元素：
    - queue_size


# 用户数据存储（Web）
- 存储选型：
    - MongoDB
    - PostgreSQL
    - Redis
- MongoDB用户存储
    - database: argus-web
        - collection：users
            + _id
            + username (unique)
            + password (hash+salt)
            + create_time
            + update_time
            + is_admin (true/false)
            + group_name
            + email
            + cell_phone
            + wechat_id
            + api
        - collection: groups
            +  _id
            + group_name (unique)
        - 监控视图...
    - database: argus-alert
        - collection: history_state
        - collection: history_notify            