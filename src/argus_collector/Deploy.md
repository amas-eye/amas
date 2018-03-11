# 采集器及采集管理网关的部署

采集管理网关与采集器可以不在同一台机器上，一个集群中只需一个采集管理网关即可（以防failover，可以多部署一个）

## 采集管理网关的部署
0. 检查系统时间是否正确
1. 把argus_collector 添加到系统的PYTHONPATH中
2. 使用nohup python app.py --start & 进行后台启动（或使用supervisor进行启动）

## 采集器部署(建议使用系统自带的python2环境),采集器是基于tcollector进行修改
0. 检查系统时间是否正确
1. 把argus_collector添加到系统的PYTHONPATH中
2. 需要修改conf/settings.py中的以下几项：
   0. OPEN_TSDB_HOST & OPEN_TSDB_PORT
   1. AGENT_MANAGER_HOSTi & AGENT_MANAGER_PORTi & AGENT_MANAGER_TOTAL (这里i 是有几个这样的就依次递增)
   2. PUSH_STATUS_FREQUEMCY  (发送的频率)
   3. LOG_FILE 日志文件的放置位置，使用绝对路径。如果不进行配置默认放在argus_collector/logs/collector.log中
3. 在argus_collector/collectors中通过创建数字为名称的文档进行检查频率的控制，单位为秒，此目录下sleep目录有预先写好的采集器，可以根据需求进行使用
4. 使用以下命令 进行启动
   ```
   ./tcollector start
   ```

