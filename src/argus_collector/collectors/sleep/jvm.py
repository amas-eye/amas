# coding=utf-8
"""
这个模块是用于采集支撑Hadoop平台组件的底层的JVM的基本数据
采用JMX方式进行采集，采集参数如下
- hadoop.jvm.GcCount
  - hadoop.jvm.GcTimeMillis
  - hadoop.jvm.LogFatal
  - hadoop.jvm.LogError
  - hadoop.jvm.LogWarn
  - hadoop.jvm.ThreadsBlocked
  - hadoop.jvm.ThreadsWaiting
  - hadoop.jvm.GcCountConcurrentMarkSweep
  - hadoop.jvm.GcTimeMillisConcurrentMarkSweep
  - hadoop.jvm.NonHeapMemoryUsage
  - hadoop.jvm.HeapMemoryUsage
  - hadoop.jvm.OpenFileDescriptorCount
  - hadoop.jvm.AvailableProcessors

"""



# def main():
#     return 0
#
#
#
#
#
#
#
#
#
#
# if __name__ == "__main__":
#     main()