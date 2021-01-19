from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.db import connection
from .models import SESSION_WINDOW, INTERACTION_OUT, PALETTE_TABLE, WHATSAPP_MAIL, \
    General_configuration_chatbot, PALETTE_STRUCTURE, INTERACTION_IN_TABLE, abc
from datetime import datetime, timedelta
import requests
import cx_Oracle
from .forms import ERP_CONNECTION_FORM, General_configuration_chatbot_form, Whatsapp_Settings_Form, \
    PALETTES_Form, PALETTE_STRUCTURE_Form, MYSQL_CONNECTION_FORM, \
    SQL_CONNECTION_FORM, Palette_document_send, Palette_video_send, Palette_image_send, \
    Palette_location_send, Palette_text_send, ABC
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template.loader import get_template
import psycopg2
import time as t1
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import mysql.connector
# import pyodbc
import ast
import base64


def erp_order(request):
    if request.method == 'POST':
        order_no = request.POST['order_no']
        order_date = request.POST['order_date']
        order_amount = request.POST['order_amount']
        customer_name = request.POST['customer_name']
        customer_no = request.POST['customer_no']
        headers = {"Content-Type": "application/json",
                   "Authorization": "Basic YTY2YTllMGMtYjNlOC00NDQzLTljYTgtNGY3YTEyMTlmYzBkOjEzYjdlYzUxLTU5MmEtNDA3Ni05ZjE1LTJmMzA2YmQ0MDI3OQ==",
                   "api-version": "2.0"
                   }
        text = f'''Dear {customer_name},

Your order number {order_no} dated {order_date} fot amount INR {order_amount} has been booked into the system.
Thank you for your business!

Regards
KARAM'''
        json = {
            "channel": "whatsapp",
            "source": "+13253077759",
            "destination": [
                f"+{customer_no}"
            ],
            "content": {
                "text": text}
        }
        response = requests.post("https://api.karix.io/message/", json=json, headers=headers)
    return render(request, 'erp_order_entry_form.html')


@api_view(['POST'])
def whatsapp_chatbot(request):
    data = request.data
    data1 = data['data']
    type = data['type']
    body_text = data1['content']['text'] or None
    channel = data1['channel'] or None
    from_chat = data1['source']
    to_no = data1['destination']
    api_version = data1['api_version']
    created_date = data1['created_time']
    d = created_date.replace('Z', '')
    time_stamp = t1.mktime(datetime.strptime(d, "%Y-%m-%dT%H:%M:%S").timetuple())
    timestamp = str(time_stamp)[:-2]
    msg_id = data['uid']
    opening_keywords = ['#']
    number_list = ['+918393944951', '+918800518850', '+918800477798', '+918826644050']
    if from_chat in number_list:
        cursor = connection.cursor()
        palettes_text_call = '''SELECT id, p_name, p_type, active, p_text, user_auth_req, function_id,
                     session_id, p_id, input_parameter_type, "attachmentType", caption, "contentType", "fileLink",
                      filename, latitude, longitude, mime_type, palette_category, encoded_data
            	FROM public.app_palette_table where p_name like 'Welcome%'
                    '''  # Welcome row call
        cursor.execute(palettes_text_call)
        palette_table_fun = cursor.fetchall()
        create_record_incoming_msg = INTERACTION_IN_TABLE(msg_id=msg_id, from_no=from_chat, to_no=to_no,
                                                          timestamp=timestamp, type=type,
                                                          date=created_date)
        create_record_incoming_msg.save()
        now = datetime.now()
        timestamp1 = datetime.timestamp(now)
        current_timestamp = str(timestamp1)[:-7]
        cursor = connection.cursor()
        data = f'''select id, wa_number, start_timestamp, updated_timestamp
        from public.app_session_window  where wa_number = '{from_chat}' 
        order by id desc limit 1 
        '''
        cursor.execute(data)
        session_window_table = cursor.fetchall()
        if session_window_table:
            now = datetime.now()
            timestamp1 = datetime.timestamp(now)
            current_timestamp = str(timestamp1)[:-7]
            # timestamp = events['timestamp']
            date_time = datetime.fromtimestamp(int(timestamp))
            from_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
            current_Date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.strptime(current_Date_time, datetimeFormat) \
                   - datetime.strptime(from_date_time, datetimeFormat)

            hours = diff.days * 24 + diff.seconds // 3600
            if hours > 24:
                insert_new_session = SESSION_WINDOW(wa_number=from_chat, start_timestamp=timestamp,
                                                    updated_timestamp=timestamp)
                insert_new_session.save()
                for palette in palette_table_fun:
                    p_id = palette[8]
                    f = palette_drawing_function(request, p_id, to_no, from_chat, '')
                    if f.status_code == 200 or f.status_code == 202:
                        interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id,
                                                                   l_palette_id=p_id,
                                                                   sent_time=current_timestamp)
                        interaction_table_insert.save()
            else:
                if str(body_text) in opening_keywords:
                    for i in session_window_table:
                        update_session_table = f'''UPDATE public.app_session_window SET updated_timestamp = '{i[3]}'
                                                                                      WHERE id = '{i[0]}';
                                   '''
                        cursor.execute(update_session_table)
                        for palette in palette_table_fun:
                            p_id = palette[8]
                            f = palette_drawing_function(request, p_id, to_no, from_chat, '')
                            if f.status_code == 200 or f.status_code == 202:
                                interaction_table_insert = INTERACTION_OUT(session_id=i[0],
                                                                           l_palette_id=p_id,
                                                                           sent_time=current_timestamp)
                                interaction_table_insert.save()
                else:
                    for data in session_window_table:
                        session_id = data[0]
                        search_paletteid_interaction_table = f'''
                        SELECT l_palette_id FROM public.app_interaction_out where session_id='{session_id}' 
                        order by id desc limit 1 ;
                        '''
                        cursor.execute(search_paletteid_interaction_table)
                        palette_id = cursor.fetchall()
                        p_rplc = str(palette_id).replace("[('", "").replace("',)]", "")
                        interaction_table_palette_id = str(p_rplc)
                        if interaction_table_palette_id:
                            palette_table_check_input_type = f'''
                              SELECT input_parameter_type FROM public.app_palette_table where p_id='{interaction_table_palette_id}';
                              '''
                            cursor.execute(palette_table_check_input_type)
                            palette_table_data_input_type = cursor.fetchall()
                            for input_type_text in palette_table_data_input_type:
                                if input_type_text[0] == 'Fixed':
                                    palette_structure_table = f'''
                                    SELECT  id, p_id, callback_p_id, response_text FROM public.app_palette_structure 
                                    where p_id='{interaction_table_palette_id}' 
                                        and response_text='{body_text}';
                                    '''
                                    cursor.execute(palette_structure_table)
                                    palette_structure = cursor.fetchall()
                                    if palette_structure:
                                        for callback_id in palette_structure:
                                            call_back_id = callback_id[2]
                                            f = palette_drawing_function(request, call_back_id, to_no, from_chat, '')
                                            if f.status_code == 200 or f.status_code == 202:
                                                interaction_table_insert = INTERACTION_OUT(session_id=session_id,
                                                                                           l_palette_id=call_back_id,
                                                                                           sent_time=current_timestamp)
                                                interaction_table_insert.save()
                                                update_session_table = f'''UPDATE public.app_session_window SET
                                                                        updated_timestamp = '{current_timestamp}'
                                                                        WHERE id = '{session_id}';
                                                                         '''
                                                cursor.execute(update_session_table)
                                    else:
                                        '''In palette structure table, response text not found'''
                                        palette_table_search_p_id = f'''
                                               SELECT p_id FROM public.app_palette_table 
                                                where p_id='{interaction_table_palette_id}'
                                               '''
                                        cursor.execute(palette_table_search_p_id)
                                        p_t_p_id = cursor.fetchall()
                                        for p_id in p_t_p_id:
                                            pal_id = p_id[0]
                                            error_fun_call = f'''SELECT p_id FROM public.app_palette_table 
                                                    where p_name='Error';
                                                    '''
                                            cursor.execute(error_fun_call)
                                            error_data = cursor.fetchall()

                                            error_p_id = str(error_data).replace("[('", '').replace("',)]", "")

                                            error_fun = palette_drawing_function(request, str(error_p_id), to_no,
                                                                                 from_chat, '')

                                            f = palette_drawing_function(request, pal_id, to_no, from_chat, '')

                                            if f.status_code == 200 or f.status_code == 202:
                                                interaction_table_insert = INTERACTION_OUT(session_id=session_id,
                                                                                           l_palette_id=interaction_table_palette_id,
                                                                                           sent_time=current_timestamp)
                                                interaction_table_insert.save()
                                                update_session_table = f'''UPDATE public.app_session_window SET
                                                updated_timestamp = '{current_timestamp}' WHERE id = '{session_id}';
                                                           '''
                                                cursor.execute(update_session_table)

                                elif input_type_text[0] == 'Variable':
                                    input_variable = body_text
                                    palette_structure_table_check_id = f'''
                                    SELECT callback_p_id 
                                    FROM public.app_palette_structure 
                                    where p_id='{interaction_table_palette_id}'; 
                                                                   '''
                                    cursor.execute(palette_structure_table_check_id)
                                    palette_structure = cursor.fetchall()
                                    if palette_structure:
                                        for call_back_id in palette_structure:
                                            p_callback_id = call_back_id[0]
                                            f = palette_drawing_function(request, p_callback_id, to_no, from_chat,
                                                                         input_variable)
                                            if f.status_code == 200 or f.status_code == 202:
                                                interaction_table_insert = INTERACTION_OUT(session_id=session_id,
                                                                                           l_palette_id=p_callback_id,
                                                                                           sent_time=current_timestamp)
                                                interaction_table_insert.save()
                                                update_session_table = f'''UPDATE public.app_session_window SET
                                                                                             updated_timestamp = '{current_timestamp}' WHERE id = '{session_id}';
                                                                                                            '''
                                                cursor.execute(update_session_table)
                                else:
                                    input_type_text[0] = None
        else:
            insert_new_session = SESSION_WINDOW(wa_number=from_chat, start_timestamp=timestamp,
                                                updated_timestamp=timestamp)
            insert_new_session.save()
            if palette_table_fun:
                for i in palette_table_fun:
                    p_id = i[8]
                    f = palette_drawing_function(request, p_id, to_no, from_chat, '')
                    if f.status_code == 200 or f.status_code == 202:
                        interaction_table_insert = INTERACTION_OUT(session_id=insert_new_session.id,
                                                                   l_palette_id=p_id,
                                                                   sent_time=current_timestamp)
                        interaction_table_insert.save()
        return HttpResponse("Done")
    else:
        return JsonResponse({'Message': 'Number does not exist in list'})


def palette_drawing_function(request, p_id, to_number, from_chat, text_message):
    headers = {"Content-Type": "application/json",
               "Authorization": "Basic YTY2YTllMGMtYjNlOC00NDQzLTljYTgtNGY3YTEyMTlmYzBkOjEzYjdlYzUxLTU5MmEtNDA3Ni05ZjE1LTJmMzA2YmQ0MDI3OQ==",
               "api-version": "2.0"
               }
    cursor = connection.cursor()
    palettes_fun_call = f'''SELECT id, p_name, p_type, active, p_text, user_auth_req, function_id,
                 session_id, p_id, input_parameter_type, "attachmentType", caption, "contentType", "fileLink",
                  filename, latitude, longitude, mime_type, palette_category, encoded_data,label,address
        	FROM public.app_palette_table where p_id = '{p_id}'
                '''
    cursor.execute(palettes_fun_call)
    palette_call_functionality = cursor.fetchall()
    for p in palette_call_functionality:
        palatte_category = p[18]
        if palatte_category == 'text':
            p_type = p[2]
            if p_type == 'Standard':
                TYPE = 'TEXT'
                TEXT_MSG = p[4]
                file = open(f"MesageResponses/{from_chat}.txt", "w")
                file.write(TEXT_MSG)
                file.close()
                content = f''' "text" : "{TEXT_MSG}"
                '''
                Content_Json = content.strip()
            elif p_type == 'Function':
                palette_function_id = p[6]
                function_table_call = f'''SELECT executable, connection_type
                FROM public.app_function
                where f_id = '{palette_function_id}'
                                                         '''
                cursor.execute(function_table_call)
                function_table_call_parameters = cursor.fetchall()
                for exce_query in function_table_call_parameters:
                    if exce_query[1] == 'oracle':
                        if text_message:
                            query_execute = str(exce_query[0]).replace("input_variable", text_message)
                            a = str(query_execute).replace("('", "")
                            function_query_execute = str(a).replace("',)", "")
                            TEXT_MSG_ = function_receive_data(function_query_execute)
                            file = open(f"MesageResponses/{from_chat}.txt", "w")
                            file.write(str(TEXT_MSG_))
                            file.close()
                            TEXT_MSG = str(TEXT_MSG_)
                            content = "text" + ':' + TEXT_MSG
                            Content_Json = content.strip()
                        else:
                            query_execute = str(exce_query[0]).replace("mobile_no", from_chat)
                            a = str(query_execute).replace("('", "")
                            function_query_execute = str(a).replace("',)", "")
                            TEXT_MSG_ = function_receive_data(function_query_execute)
                            file = open(f"MesageResponses/{from_chat}.txt", "w")
                            file.write(str(TEXT_MSG_))
                            file.close()
                            TEXT_MSG = str(TEXT_MSG_)
                            content = "text" + ':' + TEXT_MSG
                            Content_Json = content.strip()

        elif palatte_category == 'location':
            latitude = p[15]
            longitude = p[16]
            label = p[20]
            address = p[21]
            file = open(f"MesageResponses/{from_chat}.txt", "w")
            file.write(longitude)
            file.close()
            content = f'''
                  "location" : {
            "longitude": {longitude},
                  "latitude":{latitude},
                  "label": "{label}",
                  "address": "{address}!"
                            }
                        '''
            Content_Json = content.strip()

        elif palatte_category == 'media':
            URL = p[13]
            caption = p[11]
            json1 = {
                "channel": "whatsapp",
                "source": "+13253077759",
                "destination": [
                    f"{from_chat}"
                ],
                "content": { "media": {
                          "url":URL,
                          "caption": caption
                        }
                            }
            }
            response = requests.post("https://api.karix.io/message/", json=json1, headers=headers)
            print(response, 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
            return response


        json = {
            "channel": "whatsapp",
            "source": "+13253077759",
            "destination": [
                f"{from_chat}"
            ],
            "content": { Content_Json
                         }
        }
        print(json,'xxxxxxxx')
        json_replace = str(json).replace('"', "'").replace("''", "'").replace("'", '"')
        json_data = ast.literal_eval(json_replace)
        print(json_data,'xxxxxxxxwwwwwwwwwwwwww')
        response = requests.post("https://api.karix.io/message/", json=json_data, headers=headers)
        print(response,'cccccccccccccccccccccc')
        return response


@api_view(['POST'])
def genric_api_call(request):
    data = request.data
    #
    TO_NUMBER = data['TO_NUMBER']
    TEXT = data['TEXT']
    URL = data['URL']
    CAPTION = data['CAPTION']
    ATTACHMENT_TYPE = data['ATTACHMENT_TYPE']
    FILE_NAME = data['FILE_NAME']
    MIME_TYPE = data['MIME_TYPE']
    TYPE = data['TYPE']
    # TEMPLATE_NAME = data['TEMPLATE_NAME']
    LOCATION_NAME = data['LOCATION_NAME']
    LOCATION_ADDRESS = data['LOCATION_ADDRESS']
    longitude = data['longitude']
    latitude = data['latitude']
    # parameterValues = data['parameterValues']
    # parameterValues = ast.literal_eval(parameterValues)

    # while ("null" in parameterValues):
    #     parameterValues.remove("null")
    # parameter_values = {i: parameterValues[i] for i in range(0, len(parameterValues))}
    try:
        data = open(URL, "rb").read()
        encoded = base64.b64encode(data)
    except:
        encoded = None

    headers = {'Content-Type': 'application/json',
               'Authentication': 'Bearer gbGdau3EbVNJCCxd0BxNfg=='}
    json = {
        "message": {
            "channel": "WABA",
            "content": {
                "preview_url": 'false',
                "type": TYPE,
                # "type":"TEXT_or_ATTACHMENT_or_TEMPLATE_LOCATION",
                "text": TEXT,
                "attachment": {
                    "type": ATTACHMENT_TYPE,
                    "attachment_id": "attachment123",
                    "mimeType": MIME_TYPE,
                    # "mimeType": "application/pdf",
                    "fileName": FILE_NAME,
                    "caption": CAPTION,
                    "attachmentData": encoded
                },
                "location": {
                    "longitude": longitude,
                    "latitude": latitude,
                    "name": LOCATION_NAME,
                    "address": LOCATION_ADDRESS
                },
                # "template":{
                #     "templateId":TEMPLATE_NAME,
                #     "parameterValues":parameter_values
                # }
            },
            "recipient": {
                "to": TO_NUMBER,
                "recipient_type": "individual",
                "reference": {
                    "cust_ref": "Some Customer Ref",
                    "messageTag1": "Message Tag Val1..5",
                    "conversationId": "Some Optional Conversation ID"
                }
            },
            "sender": {
                "name": "Optional Name",
                "from": "919999567202"
            },
            "preferences": {
                "webHookDNId": "WEB HOOK Configured ID to recieve DN "
            }
        },
        "metaData": {
            "version": " v1.0.9"
        }
    }
    response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", json=json,
                             headers=headers)
    return HttpResponse(response)


@api_view(['POST'])
def media(request):
    data = request.data

    TO_NUMBER = data['TO_NUMBER']
    URL = data['URL']
    CAPTION = data['CAPTION']
    TYPE = data['TYPE']
    data = open(URL, "rb").read()
    encoded = base64.b64encode(data)
    # f = open('pic.txt','w')
    # f.read(encoded)
    # f.close()

    headers = {'Content-Type': 'application/json',
               'Authentication': 'Bearer gbGdau3EbVNJCCxd0BxNfg=='}
    json = {
        "message": {
            "channel": "WABA",
            "content": {
                "type": "ATTACHMENT",
                "attachment": {
                    "type": TYPE,
                    "caption": CAPTION,
                    "mimeType": "image/jpeg",
                    "attachmentData": encoded
                }
            },
            "recipient": {
                "to": TO_NUMBER,
                "recipient_type": "individual",
                "reference": {
                    "cust_ref": "Some Customer Ref",
                    "messageTag1": "Message Tag Val1",
                    "conversationId": "Some Optional Conversation ID"
                }
            },
            "sender": {
                "from": "919999567202"
            },
            "preferences": {
                "webHookDNId": "1001"
            }
        },
        "metaData": {
            "version": "v1.0.9"
        }
    }
    response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", timeout=30, json=json,
                             headers=headers)
    return HttpResponse(response)


@api_view(['POST'])
def location(request):
    data = request.data

    TO_NUMBER = data['TO_NUMBER']
    ADDRESS = data['ADDRESS']
    SEARCH_NAME = data['SEARCH_NAME']

    headers = {'Content-Type': 'application/json',
               'Authentication': 'Bearer gbGdau3EbVNJCCxd0BxNfg=='}
    json = {

        "message": {
            "channel": "WABA",
            "content": {
                "preview_url": 'false',
                "type": "LOCATION",
                "location": {
                    "longitude": 77.6109,
                    "latitude": 12.9379,
                    "name": SEARCH_NAME,
                    "address": ADDRESS
                }
            },
            "recipient": {
                "to": TO_NUMBER,
                "recipient_type": "individual"
            },
            "sender": {
                "from": "919999567202"
            },
            "preferences": {
                "webHookDNId": "1001"
            }
        },
        "metaData": {
            "version": "v1.0.9"
        }
    }
    response = requests.post("https://rcmapi.instaalerts.zone/services/rcm/sendMessage", timeout=5, json=json,
                             headers=headers)
    return HttpResponse(response)


@login_required
def home_page(request):
    return render(request, 'home.html')


def multiple_connection_form(request):
    return render(request, 'multiple_connection.html')


def erp_connection(request):
    form = ERP_CONNECTION_FORM(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        ip = form.cleaned_data['ip']
        port = form.cleaned_data['port']
        service_name = form.cleaned_data['service_name']
        try:
            dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
            connection_oracle = cx_Oracle.connect(user=username,
                                                  password=password,
                                                  dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
        except:
            return HttpResponse('invalid username/password, login denied')
        return HttpResponse('Connection Established ')
    return render(request, 'erp_connection_form.html', {'form': form})


def mysql_function(request):
    form = MYSQL_CONNECTION_FORM(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        user = form.cleaned_data['username']
        password = form.cleaned_data['password']
        host = form.cleaned_data['ip']
        port = form.cleaned_data['port']
        try:
            cnx = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password)

            # Get a cursor
            cur = cnx.cursor()
        except:
            return HttpResponse('invalid username/password, login denied')
        return HttpResponse('Connection Established ')
    return render(request, 'mysql_connection_form.html', {'form': form})


def General_configuration_form_view(request):
    form = General_configuration_chatbot_form(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        session_hour = form.cleaned_data['session_hour']
        keyword = form.cleaned_data['keyword']
        form.save()
        return HttpResponse('Done')
    return render(request, 'general_configuration_view_form.html', {'form': form})


def whatsapp_settings_form_view(request):
    form = Whatsapp_Settings_Form(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        mobile_no = form.cleaned_data['mobile_no']
        key = form.cleaned_data['key']
        form.save()
        return HttpResponse('Done')
    return render(request, 'whatsapp_settings_view_form.html', {'form': form})


def palette_form_view(request):
    form = PALETTES_Form(request.POST or None)

    if form.is_valid():
        data = form.save(commit=False)
        p_id = form.cleaned_data['p_id']
        p_name = form.cleaned_data['p_name']
        p_type = form.cleaned_data['p_type']
        active = form.cleaned_data['active']
        input_parameter_type = form.cleaned_data['input_parameter_type']
        user_auth_req = form.cleaned_data['user_auth_req']
        function_id = form.cleaned_data['function_id']
        palette_category = form.cleaned_data['palette_category']
        palette_store = PALETTE_TABLE(p_id=p_id, p_name=p_name, p_type=p_type, active=active,
                                      input_parameter_type=input_parameter_type, user_auth_req=user_auth_req,
                                      function_id=function_id, palette_category=palette_category,
                                      )

        palette_store.save()
        cursor = connection.cursor()
        palette_category_call = f'''SELECT id FROM public.app_palette_table 
                where p_id='{palette_store}' order by id desc limit 1 ;
                '''
        cursor.execute(palette_category_call)
        palette_table_id = cursor.fetchall()
        da = str(palette_table_id).replace('[(', '').replace(',)]', '')
        return redirect(f'/Palette_category/{da}')
    palette_data = PALETTE_TABLE.objects.all().order_by('-p_id')
    # content_type_id = request.GET.get('content_type')
    # cities = Attachment_Type.objects.filter(content_type=content_type_id).order_by('attachment_type')
    return render(request, 'palette_view_form.html', {'form': form, 'palette_data': palette_data})


def delete_palette(request, **kwargs):
    palette_row = get_object_or_404(PALETTE_TABLE, pk=kwargs['pk'])
    PALETTE_TABLE.objects.filter(p_id=palette_row).delete()
    return redirect('/palette')


def edit_palette(request, **kwargs):
    new_item = get_object_or_404(PALETTE_TABLE, pk=kwargs['pk'])
    queryset = PALETTE_TABLE.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(p_id=i.p_id, p_name=i.p_name, p_type=i.p_type, active=i.active,
                               input_parameter_type=i.input_parameter_type,
                               user_auth_req=i.user_auth_req, function_id=i.function_id,
                               palette_category=i.palette_category)
    form = PALETTES_Form(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/palette')
    context = {
        "form": form,
    }
    return render(request, "update_palette_form.html", context)


def Palette_category_view(request, **kwargs):
    new_item = get_object_or_404(PALETTE_TABLE, pk=kwargs['pk'])
    id = kwargs['pk']
    queryset = PALETTE_TABLE.objects.select_related().filter(pk=kwargs['pk'])
    cursor = connection.cursor()
    palette_category_call = f'''SELECT palette_category FROM public.app_palette_table where id='{kwargs['pk']}';
            '''
    cursor.execute(palette_category_call)
    palette_table_category = cursor.fetchall()
    for i in palette_table_category:
        if i[0] == 'document':
            return redirect(f'/document_palette/{id}')
        elif i[0] == 'video':
            return redirect(f'/video_palette/{id}')
        elif i[0] == 'image':
            return redirect(f'/image_palette/{id}')
        elif i[0] == 'location':
            return redirect(f'/location_palette/{id}')
        elif i[0] == 'text':
            return redirect(f'/text_palette/{id}')
        else:
            return HttpResponse('Try Again!')


def abc(request):
    if request.method == 'POST':
        form = ABC(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return redirect('/palette')
    else:
        form = ABC()
    return render(request, 'abc.html', {
        'form': form
    })


def document_palette(request):
    upload = get_object_or_404(PALETTE_TABLE, id=13)
    if request.method == 'POST':
        form = Palette_document_send(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            fileLink = form.cleaned_data['fileLink']
            file_data = form1.fileLink.read()
            data = open(str(file_data), "rb").read()
            encoded_data = base64.b64encode(data)
            caption = form.cleaned_data['caption']
            filename = form.cleaned_data['filename']
            mime_type = form.cleaned_data['mime_type']
            # form1.save()
            PALETTE_TABLE.objects.filter(id=13).update(fileLink=fileLink, caption=caption, filename=filename,
                                                       mime_type=mime_type, contentType='ATTACHMENT',
                                                       attachmentType='document', encoded_data=encoded_data)
            return redirect('/document_palette')
    else:
        form = Palette_document_send()
    return render(request, 'document_palette_view_form.html', {
        'form': form
    })


def image_palette(request, pk):
    form = Palette_image_send(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        fileLink = form.cleaned_data['fileLink']
        try:
            data = open(fileLink, "rb").read()
            file_link = base64.b64encode(str(data))
        except:
            file_link = None
        mime_type = form.cleaned_data['mime_type']
        PALETTE_TABLE.objects.filter(id=pk).update(fileLink=str(file_link), mime_type=mime_type,
                                                   contentType='ATTACHMENT', attachmentType='image')
        return redirect('/palette')
    return render(request, 'image_palette_view_form.html', {'form': form})


def video_palette(request, pk):
    form = Palette_video_send(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        fileLink = form.cleaned_data['fileLink']
        try:
            data = open(fileLink, "rb").read()
            file_link = base64.b64encode(str(data))
        except:
            file_link = None
        caption = form.cleaned_data['caption']
        filename = form.cleaned_data['filename']
        mime_type = form.cleaned_data['mime_type']
        PALETTE_TABLE.objects.filter(id=pk).update(fileLink=str(file_link), caption=caption, filename=filename,
                                                   mime_type=mime_type, contentType='ATTACHMENT',
                                                   attachmentType='video')
        return redirect('/palette')
    return render(request, 'video_palette_view_form.html', {'form': form})


def text_palette(request, pk):
    form = Palette_text_send(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        p_text = form.cleaned_data['p_text']
        PALETTE_TABLE.objects.filter(id=pk).update(p_text=p_text, contentType='text')
        return redirect('/palette')
    return render(request, 'text_palette_view_form.html', {'form': form})


def location_palette(request, pk):
    form = Palette_location_send(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        PALETTE_TABLE.objects.filter(id=pk).update(latitude=latitude, contentType='location',
                                                   longitude=longitude)
        return redirect('/palette')
    return render(request, 'location_palette_view_form.html', {'form': form})


def palette_structure_form_view(request):
    form = PALETTE_STRUCTURE_Form(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        p_id = form.cleaned_data['p_id']
        response_text = form.cleaned_data['response_text']
        callback_p_id = form.cleaned_data['callback_p_id']
        form.save()
        return redirect('/palette_structure')
    palette_s_data = PALETTE_STRUCTURE.objects.all()
    return render(request, 'palette_structure_view_form.html', {'form': form, 'palette_s_data': palette_s_data})


def delete_palette_structure(request, **kwargs):
    palette_row = get_object_or_404(PALETTE_STRUCTURE, pk=kwargs['pk'])
    PALETTE_STRUCTURE.objects.filter(p_id=palette_row).delete()
    return redirect('/palette_structure')


def edit_palette_structure(request, **kwargs):
    new_item = get_object_or_404(PALETTE_STRUCTURE, pk=kwargs['pk'])
    queryset = PALETTE_STRUCTURE.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(p_id=i.p_id, response_text=i.response_text, callback_p_id=i.callback_p_id)
    form = PALETTE_STRUCTURE_Form(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/palette_structure')
    context = {
        "form": form,
    }
    return render(request, "update_palette_structure_form.html", context)


def whatsapp_mail(request):
    conn_db = psycopg2.connect(user="w_bot_user", password="password", host="127.0.0.1", port="5433",
                               database="w_bot_db")
    cursor = conn_db.cursor()
    check_msg_id = f'''
                 SELECT id, customer_id, customer_name, email_id, whatsapp_number
                   FROM public.app_whatsapp_mail where active IS NULL
                  '''
    cursor.execute(check_msg_id)
    check_message = cursor.fetchall()
    for data in check_message:
        customer_id = data[1]
        customer_name = data[2]
        email_id = data[3]
        whatsapp_number = data[4]
        optin_link = f'http://vapi.instaalerts.zone/optin?uname=cselectric&pass=Cselectric12345%23&optinid=919999567202&action=optin&mobile={whatsapp_number}'
        try:
            ctx = {
                'optin_link': optin_link,
                'customer_id': customer_id,
                'customer_name': customer_name,
                'email_id': email_id,
                'whatsapp_number': whatsapp_number,
            }
            # Define your data

            message = get_template('whatsapp_mail.html').render(ctx)
            msg = EmailMessage(
                f'C&S now on whatsapp!!',
                message,
                'mailer@cselectric.co.in',  # will be change
                [email_id],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            t1.sleep(2)
            mail_func_update = WHATSAPP_MAIL.objects.filter(customer_id=customer_id).update(active=True)
            t1.sleep(1)
        except:
            pass
    return HttpResponse('Done')


@api_view(['POST'])
def whatsapp_bot_receive(request):
    data = request.data
    f = open('whatsapp_bot.txt', 'w')
    f.write(str(data))
    f.close()
    return HttpResponse("Done")


def function_receive_data(function_query_execute):
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    connection_oracle = cx_Oracle.connect(user=r'apps',
                                          password='apps123',
                                          dsn=dsn_tns, encoding="UTF-8")
    # user = r'cnstech', password = 'cnstech#2016#'
    cursor_conn = connection_oracle.cursor()
    query = f'''
                    {function_query_execute}
                                                      '''
    cur = cursor_conn.execute(query)
    executable_data = cur.fetchall()
    return executable_data