from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.db import connection
from .models import SESSION_WINDOW,INTERACTION_OUT,PALETTES
from datetime import datetime,timedelta
import requests


@api_view(['POST'])
def whatsapp_bot_receive_msg(request):
    data = request.data
    channel = data['channel'] or None
    appDetails = data['appDetails'] or None
    events = data['events'] or None
    eventContent = data['eventContent'] or None
    from_chat= eventContent['message']['from']
    opening_keywords = ['Hello','Hii','#']
    body_text= eventContent['message']['text']['body']
    time_stamp = events['timestamp']
    cursor = connection.cursor()
    palettes_text_call = '''SELECT * FROM public.app_palettes where p_text like 'Welcome%'
    '''
    cursor.execute(palettes_text_call)
    palette_table_fun = cursor.fetchall()
    now = datetime.now()
    timestamp1 = datetime.timestamp(now)
    current_timestamp = str(timestamp1)[:-7]
    cursor = connection.cursor()
    data = f'''select * from public.app_session_window  where wa_number = '{from_chat}' order by id desc limit 1 
'''
    cursor.execute(data)
    session_window_table = cursor.fetchall()

    if session_window_table:
        print('From no exist in Table--------------------------')
        now = datetime.now()
        timestamp1 = datetime.timestamp(now)
        current_timestamp = str(timestamp1)[:-7]
        timestamp = events['timestamp']
        date_time = datetime.fromtimestamp(int(timestamp))
        from_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

        current_Date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        diff = datetime.strptime(current_Date_time, datetimeFormat) \
               - datetime.strptime(from_date_time, datetimeFormat)

        print("Difference:", diff)
        hours = diff.days * 24 + diff.seconds // 3600
        print('Hours:', hours)
        if hours > 24:
            print('Hours is more then 24-----------------------------------------')
            insert_new_session = SESSION_WINDOW(wa_number=from_chat,start_timestamp=time_stamp,
                                                updated_timestamp=time_stamp)
            insert_new_session.save()
            for palette in palette_table_fun:
                text_message = palette[4]
                f = message_process(request, from_chat, text_message)
                if f:
                    interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id, l_palette_id=palette[9],
                                                               sent_time=current_timestamp)
                    interaction_table_insert.save()
        else:
            print('Hours is less then or equal to 24 hours')
            if str(body_text) in opening_keywords:
                print('Opening Keyword Found---------------------')
                for i in session_window_table:
                    update_session_table = f'''UPDATE public.app_session_window SET updated_timestamp = '{i[3]}'
                                                                       WHERE id = '{i[0]}';
                    '''
                    cursor.execute(update_session_table)
                    for palette in palette_table_fun:
                        text_message = palette[4]
                        f = message_process(request, from_chat, text_message)
                        if f:
                            interaction_table_insert = INTERACTION_OUT(session_id=i[0],
                                                                       l_palette_id=palette[9],
                                                                       sent_time=current_timestamp)
                            interaction_table_insert.save()
            else:
                print("Opening Keyword is not Found-------------")

                for data in session_window_table:
                    print('Check Text found in app_palette_structure================ ')
                    id =data[0]
                    search_paletteid_interaction_table=f'''
                    SELECT l_palette_id FROM public.app_interaction_out where session_id='{id}' 
                    order by id desc limit 1 ;
                    '''
                    cursor.execute(search_paletteid_interaction_table)
                    palette_id =cursor.fetchall()
                    if palette_id:
                        p_rplc = str(palette_id).replace("[('","")
                        interaction_table_palette_id = str(p_rplc).replace("',)]", "")
                        palette_structure_table =f'''
                        SELECT * FROM public.app_palette_structure where p_id='{interaction_table_palette_id}' 
                            and response_text='{body_text}';
                        '''
                        cursor.execute(palette_structure_table)
                        palette_structure = cursor.fetchall()
                        if palette_structure:
                            for call_back_id in palette_structure:

                                palette_t_p_text = f'''
                                SELECT p_text FROM public.app_palettes where p_id = '{call_back_id[2]}'
                                '''
                                cursor.execute(palette_t_p_text)
                                find_p_text = cursor.fetchall()
                                try:
                                    for p_text_palettes in find_p_text:
                                        text_msg_palette = p_text_palettes[0]
                                        print('Message  ',text_msg_palette)
                                        f = message_process(request, from_chat, text_msg_palette)
                                        if f:
                                            interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                       l_palette_id=call_back_id[2],
                                                                                       sent_time=current_timestamp)
                                            interaction_table_insert.save()
                                            update_session_table = f'''UPDATE public.app_session_window SET
                                                updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                               '''
                                            cursor.execute(update_session_table)
                                except:
                                    text_msg_palette = "Data is Blank Please select another no"
                                    f = message_process(request, from_chat, text_msg_palette)
                                    if f:
                                        for i in palette_table_fun:
                                            interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                       l_palette_id=i[9],
                                                                                       sent_time=current_timestamp)
                                            interaction_table_insert.save()
                        else:
                            print('palette_structure Data not found-------')
                            palette_table_search_p_id = f'''
                                                   SELECT p_text FROM public.app_palettes 
                                                    where p_id='{interaction_table_palette_id}'
                                                   '''
                            cursor.execute(palette_table_search_p_id)
                            p_t_p_text = cursor.fetchall()
                            for text in p_t_p_text:
                                p_text =text[0]
                                invalid_msg_add ="Sorry your response was not recognised. Please try again."
                                invalid_msg_text =invalid_msg_add + '\n' + p_text
                                print(invalid_msg_text,'invalid_msg_text')

                                f = message_process(request, from_chat, invalid_msg_text)

                                if f:
                                    interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                               l_palette_id=interaction_table_palette_id,
                                                                               sent_time=current_timestamp)
                                    interaction_table_insert.save()
                                    update_session_table = f'''UPDATE public.app_session_window SET
                                                                                    updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                                                                   '''
                                    cursor.execute(update_session_table)








    else:
        print('From no does not exist in Table--------------------------')
        insert_new_session = SESSION_WINDOW(wa_number=from_chat, start_timestamp=time_stamp,
                                            updated_timestamp=time_stamp)
        insert_new_session.save()
        if palette_table_fun:
            for i in palette_table_fun:
                text_message = i[4]
                f = message_process(request, from_chat,text_message)
                if f:
                    for i in palette_table_fun:
                        interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id, l_palette_id=i[9],
                                                                   sent_time=current_timestamp)
                        interaction_table_insert.save()
    return HttpResponse("Done")


def message_process(request,to_number, text_msg):

    headers = {'Content-Type': 'application/json',
               'Authentication': 'Bearer 0gkFJiymhPixyzaKJFQYZw=='}
    json = {
             "message":{
             "channel":"WABA",
             "content":{
             "preview_url":'false',
             "text":text_msg,
             "type":"TEXT"
             },
             "recipient":{
             "to":to_number,
             "recipient_type":"individual",
             "reference":{
             "cust_ref":"Some Customer Ref",
             "messageTag1":"Message Tag Val1",
             "conversationId":"Some Optional Conversation ID"
             }
             },
             "sender":{
             "from":"917760686668"
             },
             "preferences":{
             "webHookDNId":"1001"
             }
             },
             "metaData":{
             "version":"v1.0.9"
             }
            }
    response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", json=json, headers=headers)

    return HttpResponse(response)