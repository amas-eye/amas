# coding=utf-8
"""
简易smtp服务器, 收到信后就丢弃
需要对host和port进行配置
"""
import asyncore
import threading
from smtpd import SMTPChannel, SMTPServer

try:
    from gevent import monkey
    from gevent import sleep

    monkey.patch_all()
    print("support gevent")
except ImportError:
    pass

host = "192.168.202.102"
port = 10025


class MyChannel(SMTPChannel):
    # LMTP "LHLO" command is routed to the SMTP/ESMTP command
    def __init__(self, server, conn, addr, smtpid):
        SMTPChannel.__init__(self, server, conn, addr)
        self.smtpid = smtpid
        self.datalen = 0

    def smtp_EHLO(self, arg):
        if isinstance(self._SMTPChannel__greeting, str):
            self._SMTPChannel__greeting = 0
            self.push("250­CMEXPN")
            self.smtp_HELO(arg)

    def smtp_CMEXPN(self, arg):
        self.push("250 %s" % arg)

    def smtp_MAIL(self, arg):
        SMTPChannel.smtp_MAIL(self, arg)

    def smtp_RCPT(self, arg):
        SMTPChannel.smtp_RCPT(self, arg)

    def smtp_DATA(self, arg):
        SMTPChannel.smtp_DATA(self, arg)

    def collect_incoming_data(self, data):
        SMTPChannel.collect_incoming_data(self, data)
        self.datalen += len(data)
        self.datalen += 1
        # if (self._SMTPChannel__state == SMTPChannel.DATA):
        #     print data
        #     n=0
        #     print "[%d] has recv data %d.need sleep %ds" % (self.smtpid,self.datalen,n)
        #     time.sleep(n)


class MySmtpSvr(SMTPServer):
    def __init__(self, localaddr, remoteaddr):
        print("listen smtp in ", localaddr)
        SMTPServer.__init__(self, localaddr, remoteaddr)
        self.nAcceptCnt = 0
        self.lock = threading.Lock()

    def process_message(self, peer, mailfrom, rcpttos, data):
        pass

    def handle_accept(self):
        conn, addr = self.accept()
        nCnt = 0
        with self.lock:
            self.nAcceptCnt += 1
            nCnt = self.nAcceptCnt
        print('Accept client[{}] {}'.format(nCnt, addr))
        channel = MyChannel(self, conn, addr, nCnt)


if __name__ == "__main__":
    server = MySmtpSvr((host, port), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        server.close()
