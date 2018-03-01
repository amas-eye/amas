#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to reply to our follower according to
the message they send to us.
"""

import xml.etree.ElementTree as ET


def parse_xml(xml_data):
    if not xml_data:
        return None
    data = ET.fromstring(xml_data)
    msg_type = data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(data)
    if msg_type == 'image':
        return ImageMsg(data)
    if msg_type == 'voice':
        return VoiceMsg(data)
    if msg_type in ('video', 'shortvideo'):
        return VideoMsg(data)
    if msg_type == 'location':
        return LocationMsg(data)
    if msg_type == 'link':
        return LinkMsg(data)

    # Receive a event push from wechat, i.e. user press some menu
    # or scan QR code, everything exclude sending us a msg.
    if msg_type == 'event':
        event = data.find('Event').text
        event_key = data.find('EventKey').text
        if event == 'subscribe' and event_key.startswith('qrscene_'):
            # It is a new follower who scan a parametric QR code
            return NewFollowerFromParametricQRCodeEventMsg(data)
        if event == 'CLICK':  # in this situation we only support click to
            #arrange a unqiue url to user from wechat web page
            # Follwer click the menu
            if event_key == 'try_argus':
                return NewTrialEventMsg(data)
            else:
                return MenuClickEventMsg(data)
        if event == 'TEMPLATESENDJOBFINISH':
            # Wechat response after we trying to send template msg.
            return TemplateSendJobEventMsg(data)
        else:
            return UnSupportedMsg(data)
    else:
        return UnSupportedMsg(data)


class UnSupportedMsg:
    def __init__(self, data):
        self.to_username = data.find('ToUserName').text
        self.from_username = data.find('FromUserName').text
        self.create_time = data.find('CreateTime').text
        self.msg_type = data.find('MsgType').text


class Msg:
    def __init__(self, data):
        self.to_username = data.find('ToUserName').text
        self.from_username = data.find('FromUserName').text
        self.create_time = data.find('CreateTime').text
        self.msg_type = data.find('MsgType').text
        self.msg_id = data.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, data):
        try:
            super().__init__(data)
            self.content = data.find('Content').text.encode('utf-8')
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class ImageMsg(Msg):
    def __init__(self, data):
        try:
            self.content = data.find('Content').text.encode('utf-8')
            self.pic_url = data.find('PicUrl').text
            self.media_id = data.find('MediaId').text
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class VoiceMsg(Msg):
    def __init__(self, data):
        try:
            super()._init_(data)
            self.format = data.find('format').text
            self.media_id = data.find('MediaId').text
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class VideoMsg(Msg):
    def __init__(self, data):
        try:
            super()._init_(data)
            self.thumb_media_id = data.find('ThumbMediaId').text
            self.media_id = data.find('MediaId').text
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class LinkMsg(Msg):
    def __init__(self, data):
        try:
            super()._init_(data)
            self.title = data.find('Title').text
            self.description = data.find('Description').text
            self.url = data.find('Url').text
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class LocationMsg(Msg):
    def __init__(self, data):
        try:
            super()._init_(data)
            self.latitude = data.find('Location_X').text
            self.longtitude = data.find('Location_Y').text
            self.scale = data.find('Scale').text
            self.Label = data.find('Label').text
        except AttributeError as e:
            print('XML fields may be wrong, check out please.', e)


class EventMsg:
    def __init__(self, data):
        self.to_username = data.find('ToUserName').text
        self.from_username = data.find('FromUserName').text
        self.create_time = data.find('CreateTime').text
        self.msg_type = data.find('MsgType').text
        self.event = data.find('Event').text


class NewFollowerFromParametricQRCodeEventMsg(EventMsg):
    def __init__(self, data):
        super().__init__(data)
        self.event_key = data.find('EventKey').text
        self.ticket = data.find('Ticket').text


class MenuClickEventMsg(EventMsg):
    def __init__(self, data):
        super().__init__(data)
        self.event_key = data.find('EventKey')


class TemplateSendJobEventMsg(EventMsg):
    def __init__(self, data):
        super().__init__(data)
        self.msg_id = data.find('MsgID')
        self.status = data.find('Status')


class NewTrialEventMsg(MenuClickEventMsg):
    def __init__(self, data):
        super().__init__(data)
