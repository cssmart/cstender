import logging
from django_mailbox.models import Mailbox, Message
import cx_Oracle

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import base64
from django.db import connection
import re
import json
import email.parser

parser = email.parser.FeedParser()
from django.core.mail import EmailMessage
from django.template.loader import get_template


def FirstCronTest():
    mailboxes = Mailbox.active_mailboxes.all()
    for mailbox in mailboxes:
        logger.info(
            'Gathering messages for %s',
            mailbox.id
        )
        messages = mailbox.get_new_mail()

        for message in messages:
            logger.info(
                'Id %s, Subject %s, (from %s), message_id %s',
                message.id,
                message.subject,
                message.from_address,
                message.message_id
                # message.body
            )
            cursor = connection.cursor()
            check_msg_id = f'''
                        SELECT id FROM public.django_mailbox_message
                            where message_id='{message.message_id}' order by id desc limit 1;
                        '''
            cursor.execute(check_msg_id)
            check_message = cursor.fetchall()
            if check_message:
                print(check_message,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                for id in check_message:
                    mail_id = id[0]
                    print(mail_id,'dddddddddddddddddddddddddd')

                    string1 = message.subject
                    try:
                        apex_id = int(re.search(r'\d+', string1).group())
                        cursor = connection.cursor()
                        approval_item = '''SELECT id FROM public.django_mailbox_message WHERE
                        (subject LIKE 'Approve Apex Item ID%' or subject LIKE 'Reject Apex Item ID%')
                        and process_data IS NULL
                        '''
                        cursor.execute(approval_item)
                        row = cursor.fetchall()

                        if row:
                            id_data = row
                            a = str(id_data).replace("[(", '')
                            id_ = str(a).replace(",)]", '')
                            search_in_mail = f'''SELECT subject FROM public.django_mailbox_message WHERE id ='{mail_id}'
                            '''
                            cursor.execute(search_in_mail)
                            row1 = cursor.fetchall()
                            row_ = str(row1).replace("[(", '')
                            subject_mail = str(row_).replace(",)]", '')

                            if 'Approve Apex Item ID' in subject_mail:
                                search_apex_id = f'''
                                SELECT *
                                    FROM public.app_apextable
                                    WHERE apex_id = '{apex_id}' and apex_status IS NULL order by id desc Limit 1
                                '''
                                cursor.execute(search_apex_id)
                                row3 = cursor.fetchall()
                                for i in row3:
                                    id_ = i[0]
                                    trx_level = i[1]
                                    forwarded_by = i[2]
                                    item_template = i[4]
                                    initiator_email = i[12]
                                    item_code = i[8]
                                    try:
                                        dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
                                        conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex007',
                                                                     dsn=dsn_tns)
                                        cursor_ora = conn_ora.cursor()
                                        query = f'''
                                                       declare
                                                       p_entity_trx_id number;
                                                       p_trx_level number;
                                                       p_forward_by number;
                                                       p_forward_to number;
                                                       p_approve_date date;
                                                       p_forward_note varchar2(300);
                                                       p_approve_note varchar2(300);
                                                       p_item_template varchar2(300);
                                                       l_err_status varchar2(300);
                                                       l_err_msg varchar2(300);
                                                        ln_appr_user_id number;
                                                                                                       begin
        
                                                        begin
        
                                                        select APPROVER_USER_ID 
                                                        into ln_appr_user_id
                                                        from apex_ebs_extension.xxapx_103_trx_approvers 
                                                        where REQUEST_USER_ID='{forwarded_by}';
        
                                                        end;
                                                       XXAPX_103_APP_PKG.approval_transaction(p_entity_trx_id => '{apex_id}',
                                                       p_trx_level => '{trx_level}',
                                                       p_forward_by => '{forwarded_by}',
                                                       p_forward_to => ln_appr_user_id,
                                                       p_approve_date => SYSDATE,
                                                       p_forward_note => 'na',
                                                       p_approve_note => NULL,
                                                       p_item_template =>'{item_template}',
                                                       p_err_status => l_err_status,
                                                       p_err_msg => l_err_msg);
                                                       dbms_output.put_line(l_err_msg);
                                                       end;
                                                       '''
                                        cursor_ora.execute(query)
                                        update_apex_table = f'''UPDATE  public.app_apextable SET apex_status = 'True'
                                                               WHERE id = '{id_}';'''
                                        cursor.execute(update_apex_table)

                                        update_django_mailbox_message = f'''UPDATE public.django_mailbox_message SET process_data = 'Approve'
                                                                                            WHERE id = '{mail_id}';'''
                                        cursor.execute(update_django_mailbox_message)

                                        ctx = {
                                            'item_code': item_code,

                                        }
                                        message = get_template('approved_mail.html').render(ctx)
                                        msg = EmailMessage(
                                            f'Item Code {item_code} has been approved',
                                            message,
                                            'harshitaagarwal219@gmail.com',  # will be change
                                            [initiator_email],
                                        )
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()

                                    # conn_ora.commit()
                                    except:
                                        if mail_id:
                                            update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                                                               WHERE id = '{mail_id}';'''
                                            cursor.execute(update_mail_reject)
                                            ctx = {
                                                'item_code': item_code,

                                            }
                                            message = get_template('failed_mail.html').render(ctx)
                                            msg = EmailMessage(
                                                f'Item Code {item_code} could not be processed',
                                                message,
                                                'harshitaagarwal219@gmail.com',  # will be change
                                                [initiator_email],
                                            )
                                            msg.content_subtype = "html"  # Main content is now text/html
                                            msg.send()
                            print('reject=============================')
                            search_apex_id_reject = f'''
                                 SELECT id, item_code,initiator_email
                                     FROM public.app_apextable
                                     WHERE apex_id = '{apex_id}' and apex_status IS NULL order by id desc Limit 1
                                 '''
                            cursor.execute(search_apex_id_reject)
                            apex_id_reject = cursor.fetchall()
                            for reject_data in apex_id_reject:
                                reject_apex_id = reject_data[0]
                                item_code = reject_data[1]
                                reject_email_ = reject_data[2]
                                if 'Reject Apex Item ID' in subject_mail:
                                    try:
                                        dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
                                        conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex007',
                                                                     dsn=dsn_tns)
                                        cursor_ora = conn_ora.cursor()
                                        query1 = f'''
                                                   declare
                                                   p_seq_id number;
                                                   p_forward_note varchar2(300);
                                                   begin
                                                   XXAPX_103_APP_PKG.reject_item(p_seq_id =>'{apex_id}',
                                                   p_forward_note =>'na');
                                                   end;
                                               '''
                                        cursor_ora.execute(query1)
                                        update_mail = f'''UPDATE public.django_mailbox_message SET process_data = 'Reject'
                                        WHERE id = '{mail_id}';'''
                                        cursor.execute(update_mail)
                                        update_mail = f'''UPDATE  public.app_apextable SET apex_status = 'True'
                                                                                             WHERE id = '{reject_apex_id}';'''
                                        cursor.execute(update_mail)
                                        ctx = {
                                            'item_code': item_code,

                                        }
                                        message = get_template('rejected_mail.html').render(ctx)
                                        msg = EmailMessage(
                                            f'Item Code {item_code} has been rejected',
                                            message,
                                            'harshitaagarwal219@gmail.com',  # will be change
                                            [reject_email_],
                                        )
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()
                                        print('end=================================')
                                    except:
                                        print('failed mail[[[[[[[[[[[[[[[[[')
                                        if mail_id:
                                            update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                    WHERE id = '{mail_id}';'''
                                            cursor.execute(update_mail_reject)
                                            ctx = {
                                                'item_code': item_code,

                                            }
                                            message = get_template('failed_mail.html').render(ctx)
                                            msg = EmailMessage(
                                                f'Item code {item_code} could not be processed',
                                                message,
                                                'harshitaagarwal219@gmail.com',  # will be change
                                                [reject_email_],
                                            )
                                            msg.content_subtype = "html"  # Main content is now text/html
                                            msg.send()
                                            print(msg,'ssssssssssssssssssssssssssssssssssssss')
                    except:
                        for mailbox in mailboxes:
                            logger.info(
                                'Gathering messages for %s',
                                mailbox.id
                            )
                    messages = mailbox.get_new_mail()