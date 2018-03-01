#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class Msg(object):
    def __init__(self):
        pass

    def send(self):
        return 'success'


class TextMsg(Msg):
    def __init__(self, to_user_name, from_user_name, content):
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_time = int(time.time())
        self.content = content

    def send(self):
        xml_data = f'''
        <xml>
        <ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
        <CreateTime>{self.create_time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{self.content}]]></Content>
        </xml>
        '''

        return xml_data


class ImageMsg(Msg):
    def __init__(self, to_user_name, from_user_name, media_id):
        self.to_username = to_user_name
        self.from_user_name = from_user_name
        self.create_time = int(time.time())
        self.media_id = media_id

    def send(self):
        xml_data = f'''
        <xml>
        <ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
        <CreateTime>{self.create_time}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{self.media_id}]]></MediaId>
        </Image>
        </xml>
        '''

        return xml_data


class EventMsg(Msg):
    """Basically copy from TextMsg."""

    def __init__(self, to_user_name, from_user_name, content):
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_time = int(time.time())
        self.content = content

    def send(self):
        xml_data = f'''
        <xml>
        <ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
        <FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
        <CreateTime>{self.create_time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{self.content}]]></Content>
        </xml>
        '''

        return xml_data


class TrialEventMsg(EventMsg):
    def __init__(self, to_user_name, from_user_name, url):
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_time = int(time.time())
        self.url = url
        self.msg_type = 'news'
        self.article_count = 1
        self.articles = 'Nihao'
        self.title = '欢迎试用Argus大数据平台监控系统'
        self.description = '欢迎体验'
        self.pic_url = 'https://m.baidu.com/static/index/plus/plus_logo.png'

    def send(self):
        xml_data = f'''
            <xml>
                <ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
                <CreateTime>{self.create_time}</CreateTime>
                <MsgType><![CDATA[{self.msg_type}]]></MsgType>
                <ArticleCount>{self.article_count}</ArticleCount>
                <Articles>
                    <item>
                        <Title>{self.title}</Title>
                        <Description>{self.description}</Description>
                        <PicUrl>{self.pic_url}</PicUrl>
                        <Url>{self.url}</Url>
                    </item>
                </Articles>
            </xml>
        '''

        return xml_data

