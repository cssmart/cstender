from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.db import connection
from .models import SESSION_WINDOW,INTERACTION_OUT,PALETTES
from datetime import datetime,timedelta
import requests
import cx_Oracle
from rest_framework.response import Response

@api_view(['POST'])
def whatsapp_bot_receive_msg(request):
    '''
    Chat bot integration
    :param request:
    :return:
    '''
    data = request.data
    channel = data['channel'] or None
    appDetails = data['appDetails'] or None
    events = data['events'] or None
    eventContent = data['eventContent'] or None
    from_chat= eventContent['message']['from']
    opening_keywords = ['#']
    body_text= eventContent['message']['text']['body']
    time_stamp = events['timestamp']
    cursor = connection.cursor()
    palettes_text_call = '''SELECT * FROM public.app_palettes where p_text like 'Welcome%'
    '''  # Welcome row call
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
                file = open(f"MesageResponses/{from_chat}.txt", "w")
                file.write(text_message)
                file.close()
                f = message_process(request, from_chat, text_message)
                if f:
                    interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id, l_palette_id=palette[8],
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
                        file = open(f"MesageResponses/{from_chat}.txt", "w")
                        file.write(text_message)
                        file.close()
                        f = message_process(request, from_chat, text_message)
                        if f:
                            interaction_table_insert = INTERACTION_OUT(session_id=i[0],
                                                                       l_palette_id=palette[8],
                                                                       sent_time=current_timestamp)
                            interaction_table_insert.save()
            else:
                print("Opening Keyword is not Found-------------")
                for data in session_window_table:
                    id =data[0]
                    print('pickup current  session is : --',id)
                    search_paletteid_interaction_table=f'''
                    SELECT l_palette_id FROM public.app_interaction_out where session_id='{id}' 
                    order by id desc limit 1 ;
                    '''
                    print('Check Session id in interaction table')
                    cursor.execute(search_paletteid_interaction_table)
                    palette_id =cursor.fetchall()
                    if palette_id:
                        p_rplc = str(palette_id).replace("[('","")
                        interaction_table_palette_id = str(p_rplc).replace("',)]", "")
                        print('Check input_parameter_type in app_palette================ ')
                        print('interaction_table_palette_id :---',interaction_table_palette_id)
                        palette_table_check_input_type = f'''
                          SELECT input_parameter_type FROM public.app_palettes where p_id='{interaction_table_palette_id}';
                          '''
                        cursor.execute(palette_table_check_input_type)
                        palette_table_data_input_type = cursor.fetchall()
                        print('Palette table input parameter : -',palette_table_data_input_type)
                        for input_type_text in palette_table_data_input_type:
                            if input_type_text[0] == 'Fixed':
                                print('input_type_text is : --', input_type_text[0])
                                palette_structure_table =f'''
                                SELECT * FROM public.app_palette_structure where p_id='{interaction_table_palette_id}' 
                                    and response_text='{body_text}';
                                '''
                                cursor.execute(palette_structure_table)
                                palette_structure = cursor.fetchall()
                                print('palette_structure table',palette_structure)
                                if palette_structure:
                                    for call_back_id in palette_structure:
                                        palette_t_p_text = f'''
                                        SELECT p_text, p_type, function_id FROM public.app_palettes where p_id = '{call_back_id[2]}'
                                        '''
                                        cursor.execute(palette_t_p_text)
                                        find_p_text = cursor.fetchall()
                                        for check_data in find_p_text:
                                            if check_data[1] == 'Standard':
                                                print("Type is Standard")
                                                text_msg_palette = check_data[0]
                                                print('Message  ', text_msg_palette)
                                                file = open(f"MesageResponses/{from_chat}.txt", "w")
                                                file.write(text_msg_palette)
                                                file.close()
                                                try:
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
                                                        print('Data Stored Successfully')
                                                except:
                                                    text_msg_palette = "Data is Blank Please select another no"
                                                    f = message_process(request, from_chat, text_msg_palette)
                                                    if f:
                                                        for i in palette_table_fun:
                                                            interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                                       l_palette_id=i[8],
                                                                                                       sent_time=current_timestamp)
                                                            interaction_table_insert.save()
                                            if check_data[1] == 'Function':
                                                print('Type is a function in palette')
                                                palette_functionid = check_data[2]
                                                function_table_call = f'''
                                        SELECT executable FROM public.app_function where f_id = '{palette_functionid}'
                                            '''
                                                cursor.execute(function_table_call)
                                                function_table_call_parameters = cursor.fetchall()
                                                for exce_query in function_table_call_parameters:
                                                    query_execute = str(exce_query).replace("mobile_no", from_chat)
                                                    a = str(query_execute).replace("('", "")
                                                    function_query_execute = str(a).replace("',)", "")
                                                    function_query_ = function_receive_data(function_query_execute)
                                                    print('Function Executable query : ', function_query_)
                                                    file = open(f"MesageResponses/{from_chat}.txt", "w")
                                                    file.write(function_query_)
                                                    file.close()
                                                    f = message_process(request, from_chat, function_query_)
                                                    if f:
                                                        interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                                   l_palette_id=interaction_table_palette_id,
                                                                                                   sent_time=current_timestamp)
                                                        interaction_table_insert.save()
                                                        print('interaction_table====', interaction_table_insert)
                                                        update_session_table = f'''UPDATE public.app_session_window SET
                                                         updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                                '''
                                                        cursor.execute(update_session_table)

                                else:
                                    '''In palette structure table, response text not found'''
                                    print('In palette structure response text not found')
                                    palette_table_search_p_id = f'''
                                           SELECT p_text FROM public.app_palettes 
                                            where p_id='{interaction_table_palette_id}'
                                           '''
                                    cursor.execute(palette_table_search_p_id)
                                    p_t_p_text = cursor.fetchall()
                                    for text in p_t_p_text:
                                        p_text = text[0]
                                        invalid_msg_add = "Sorry your response was not recognised. Please try again."
                                        invalid_msg_text = invalid_msg_add + '\n' + p_text
                                        print(invalid_msg_text, '=========invalid_msg_text')
                                        file = open(f"MesageResponses/{from_chat}.txt", "w")
                                        file.write(invalid_msg_text)
                                        file.close()

                                        f = message_process(request, from_chat, invalid_msg_text)

                                        if f:
                                            interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                       l_palette_id=interaction_table_palette_id,
                                                                                       sent_time=current_timestamp)
                                            interaction_table_insert.save()
                                            print(interaction_table_insert,'ooooooooooooooooooooooooooooooooo')
                                            update_session_table = f'''UPDATE public.app_session_window SET
                                            updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                       '''
                                            cursor.execute(update_session_table)
                                            print(('End proces----------------------'))

                            elif input_type_text[0] == 'Variable':
                                print(input_type_text[0],'99999999999999999----------------------------------')
                                palette_structure_table_check_id = f'''
                                SELECT * FROM public.app_palette_structure where p_id='{interaction_table_palette_id}'; 
                                                               '''
                                cursor.execute(palette_structure_table_check_id)
                                palette_structure = cursor.fetchall()
                                print(palette_structure, '==============================================')
                                if palette_structure:
                                    for call_back_id in palette_structure:
                                        palette_t_p_text = f'''
                                        SELECT p_text, p_type, function_id FROM public.app_palettes where p_id = '{call_back_id[2]}'
                                        '''
                                        cursor.execute(palette_t_p_text)
                                        find_p_text = cursor.fetchall()
                                        print(find_p_text, 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                                        for check_data in find_p_text:
                                            text_msg_palette = check_data[0] or 'None'
                                            print('Message  ', text_msg_palette)
                                            file = open(f"MesageResponses/{from_chat}.txt", "w")
                                            file.write(text_msg_palette)
                                            file.close()
                                            if check_data[1] == 'Standard':
                                                print(check_data[1], 'fffffffffffffffffffffffffffffffffffffffff')
                                                try:
                                                    f = message_process(request, from_chat, text_msg_palette)
                                                    if f:
                                                        interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                                   l_palette_id=
                                                                                                   call_back_id[2],
                                                                                                   sent_time=current_timestamp)
                                                        interaction_table_insert.save()
                                                        update_session_table = f'''UPDATE public.app_session_window SET
                                                            updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                                           '''
                                                        cursor.execute(update_session_table)
                                                        print(cursor, 'lllllllllllllllllllllllllllllllllllllllllll')
                                                except:
                                                    text_msg_palette = "Data is Blank Please select another no"
                                                    f = message_process(request, from_chat, text_msg_palette)
                                                    if f:
                                                        for i in palette_table_fun:
                                                            interaction_table_insert = INTERACTION_OUT(
                                                                session_id=id,
                                                                l_palette_id=i[8],
                                                                sent_time=current_timestamp)
                                                            interaction_table_insert.save()
                                            if check_data[1] == 'Function':
                                                print('Type is a function in palette =====================')
                                                palette_functionid = check_data[2]
                                                print(palette_functionid, 'dddddddddddddddd')

                                                function_table_call = f'''
                                                  SELECT executable FROM public.app_function where f_id = '{palette_functionid}'
                                                  '''
                                                cursor.execute(function_table_call)
                                                function_table_call_parameters = cursor.fetchall()
                                                for exce_query in function_table_call_parameters:
                                                    query_execute = str(exce_query).replace("mobile_no", from_chat)
                                                    a =str(query_execute).replace("('","")
                                                    function_query_execute =str(a).replace("',)","")
                                                    print(function_query_execute,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                                                    function_query_ = function_receive_data(function_query_execute)

                                                    file = open(f"MesageResponses/{from_chat}.txt", "w")
                                                    file.write(function_query_)
                                                    file.close()
                                                    f = message_process(request, from_chat, function_query_)
                                                    if f:
                                                        interaction_table_insert = INTERACTION_OUT(session_id=id,
                                                                                                   l_palette_id=interaction_table_palette_id,
                                                                                                   sent_time=current_timestamp)
                                                        interaction_table_insert.save()
                                                        print('interaction_table====',interaction_table_insert)
                                                        update_session_table = f'''UPDATE public.app_session_window SET
                                                          updated_timestamp = '{current_timestamp}' WHERE id = '{id}';
                                                                         '''
                                                        cursor.execute(update_session_table)
                                                        print(cursor,'eeeeeeeeeeeeeeeeeeeeeee')
                            else:
                                print('input_type_text is None, pending ==================')

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
                            file = open(f"MesageResponses/{from_chat}.txt", "w")
                            file.write(invalid_msg_text)
                            file.close()

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
                print(text_message,'text msg============')
                file = open(f"MesageResponses/{from_chat}.txt", "w")
                file.write(text_message)
                file.close()
                f = message_process(request, from_chat,text_message)
                print('Payload===', f)
                if f:
                    for i in palette_table_fun:
                        interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id, l_palette_id=i[8],
                                                                   sent_time=current_timestamp)
                        interaction_table_insert.save()
                        print(interaction_table_insert,'inter=========')
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

    return response


def function_receive_data(function_query_execute):
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525',service_name='SANDBOX')
    connection_oracle = cx_Oracle.connect(user=r'apps',
                                          password='apps1234',
                                          dsn=dsn_tns, encoding="UTF-8")
    cursor_conn = connection_oracle.cursor()
    query = f'''
                    {function_query_execute}
                                                      '''
    cur = cursor_conn.execute(query)
    executable_data = cur.fetchall()
    return executable_data
