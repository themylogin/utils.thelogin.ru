#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import dbus.mainloop.glib
import gobject
import os.path
import re
import simplejson

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

desktop_dbus = dbus.bus.BusConnection("tcp:host=192.168.0.3,port=55555")
PurpleObject = desktop_dbus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
PurpleInterface = dbus.Interface(PurpleObject, "im.pidgin.purple.PurpleInterface")

PURPLE_MESSAGE_SEND = 0x0001
PURPLE_MESSAGE_RECV = 0x0002

def update():
    def process_message_text(text):
        return re.sub('<[^<]+?>', '', text)

    result = []
    for conversation_id in PurpleInterface.PurpleGetConversations():
        if PurpleInterface.PurpleConversationHasFocus(conversation_id):
            buddy = unicode(PurpleInterface.PurpleConversationGetTitle(conversation_id))
            incoming_messages = []
            for message_id in PurpleInterface.PurpleConversationGetMessageHistory(conversation_id):
                flags = PurpleInterface.PurpleConversationMessageGetFlags(message_id)

                if flags & PURPLE_MESSAGE_SEND:
                    break

                if flags & PURPLE_MESSAGE_RECV:
                    incoming_messages.append({
                        "time"  : int(PurpleInterface.PurpleConversationMessageGetTimestamp(message_id)),
                        "text"  : process_message_text(unicode(PurpleInterface.PurpleConversationMessageGetMessage(message_id))),
                    })

            if len(incoming_messages) > 0:
                incoming_messages.reverse()
                result.append({
                    "buddy"             : buddy,
                    "has_focus"         : True,
                    "incoming_messages" : incoming_messages,
                })

        unseen_count = PurpleInterface.PurpleConversationGetUnseen(conversation_id)
        if unseen_count > 0:            
            buddy = unicode(PurpleInterface.PurpleConversationGetTitle(conversation_id))
            incoming_messages = []
            handled_messages = 0
            for message_id in PurpleInterface.PurpleConversationGetMessageHistory(conversation_id):
                flags = PurpleInterface.PurpleConversationMessageGetFlags(message_id)

                if flags & PURPLE_MESSAGE_RECV:
                    incoming_messages.append({
                        "time"  : int(PurpleInterface.PurpleConversationMessageGetTimestamp(message_id)),
                        "text"  : process_message_text(unicode(PurpleInterface.PurpleConversationMessageGetMessage(message_id))),
                    })

                handled_messages += 1
                if handled_messages >= unseen_count:
                    break

            if len(incoming_messages) > 0:
                incoming_messages.reverse()
                result.append({
                    "buddy"             : buddy,
                    "incoming_messages" : incoming_messages,
                })

    open(os.path.join(os.path.dirname(__file__), "index.json"), "w").write(simplejson.dumps(result))
    return True

update()

desktop_dbus.add_signal_receiver(lambda conversation, type: update(), dbus_interface="im.pidgin.purple.PurpleInterface", signal_name="ConversationUpdated")

loop = gobject.MainLoop()
gobject.timeout_add(60 * 1000, update)
loop.run()
