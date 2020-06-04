import logging
from django_mailbox.models import Mailbox,Message
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
                'Id %s, Subject %s, (from %s)',
                message.id,
                message.subject,
                message.from_address,
                # message.body
            )
            string1 = message.subject
            recv_msg_id = message.id
            print(message.id,message.from_address, message.subject,recv_msg_id,'222222222222222222')
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
                    search_in_mail = f'''SELECT subject FROM public.django_mailbox_message WHERE id ='{recv_msg_id}'
                    '''
                    cursor.execute(search_in_mail)
                    row1 = cursor.fetchall()
                    row_ = str(row1).replace("[(", '')
                    subject_mail = str(row_).replace(",)]", '')
                    if 'Approve Apex Item ID' in subject_mail:
                        print('Approve Apex Item ID-------------------------------------------------------')
                        search_apex_id = f'''
                        SELECT *
                            FROM public.app_apextable
                            WHERE apex_id = '{apex_id}' and apex_status IS NULL order by id desc Limit 1
                        '''
                        cursor.execute(search_apex_id)
                        row3 = cursor.fetchall()
                        print(row3,'dddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                        if row3:
                            print(row3,'wwwwwwwwwwwwwwwwwwww')
                            for i in row3:
                                try:
                                    id_ = i[0]
                                    trx_level = i[1]
                                    forwarded_by = i[2]
                                    item_template = i[4]
                                    email_ = i[11]
                                    item_code = i[8]
                                    print(item_code,'eeeeeeeeeeeeeeeeee')
                                    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
                                    conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex007', dsn=dsn_tns)
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
                                    print(cursor_ora,'eeeeeeeeeeeeeeeeeeeeee')
                                    update_apex_table = f'''UPDATE  public.app_apextable SET apex_status = 'True'
                                                           WHERE id = '{id_}';'''
                                    cursor.execute(update_apex_table)
                                    print(cursor,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                                    update_django_mailbox_message= f'''UPDATE public.django_mailbox_message SET process_data = 'Approve'
                                                                                        WHERE id = '{recv_msg_id}';'''
                                    cursor.execute(update_django_mailbox_message)
                                    print(cursor,'w222222222222222222')
                                    mailbox_subject = f'''SELECT subject FROM public.django_mailbox_message
                                    where id = '{recv_msg_id}';
                                    '''
                                    cursor.execute(mailbox_subject)
                                    mailbox_ =cursor.fetchall()
                                    for subject in mailbox_:
                                        ctx = {
                                            'item_code': item_code,

                                        }
                                        message = get_template('approved_mail.html').render(ctx)
                                        msg = EmailMessage(
                                            f'{subject[0]}',
                                            message,
                                            'harshitaagarwal219@gmail.com',  # will be change
                                            message.from_address,
                                        )
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()
                                except:
                                    print('Approve not---------------------------')
                                    if recv_msg_id:
                                        print(recv_msg_id, 'eeeeeeeeeeeeeeeeeeee')

                                        update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                                                     WHERE id = '{recv_msg_id}';'''
                                        cursor = connection.cursor()
                                        cursor.execute(update_mail_reject)
                                        mailbox_subject_error = f'''SELECT subject FROM public.django_mailbox_message
                                                    where id = '{recv_msg_id}';
                                                           '''
                                        cursor.execute(mailbox_subject_error)
                                        mailbox_error = cursor.fetchall()
                                        for error_subject in mailbox_error:
                                            subject = error_subject[0]
                                            ctx = {
                                                'item_code': item_code,

                                            }
                                            message = get_template('failed_mail.html').render(ctx)
                                            msg = EmailMessage(
                                                f'{subject}',
                                                message,
                                                'harshitaagarwal219@gmail.com',  # will be change
                                                message.from_address,
                                            )
                                            msg.content_subtype = "html"  # Main content is now text/html
                                            msg.send()
                                    # for mailbox in mailboxes:
                                    #     logger.info(
                                    #         'Gathering messages for %s',
                                    #         mailbox.id
                                    #     )
                                    # messages = mailbox.get_new_mail()

                            # conn_ora.commit()
                        else:
                            if recv_msg_id:
                                print(recv_msg_id, 'eeeeeeeeeeeeeeeeeeee')

                                update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                  WHERE id = '{recv_msg_id}';'''
                                cursor = connection.cursor()
                                cursor.execute(update_mail_reject)
                                # mailbox_subject_error = f'''SELECT subject FROM public.django_mailbox_message
                                #                                                             where id = '{recv_msg_id}';
                                #                                                             '''
                                # cursor.execute(mailbox_subject_error)
                                # mailbox_error = cursor.fetchall()
                                search_apex_id = f'''
                                SELECT *
                                    FROM public.app_apextable
                                    WHERE apex_id = '{apex_id}' order by id desc Limit 1
                                '''
                                cursor.execute(search_apex_id)
                                row3 = cursor.fetchall()
                                print(row3, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                                # for error_subject in mailbox_error:
                                mailsubject = message.subject
                                print(subject,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                                ctx = {
                                    'subject': subject,
                                }
                                print(ctx,'ctx===================')
                                message = get_template('failed_mail.html').render(ctx)
                                print(message,'ssssssssssssssssssssssssssssssssssssssssssss')
                                msg = EmailMessage(
                                    f'{subject}',
                                    message,
                                    'harshitaagarwal219@gmail.com',  # will be change
                                    message.from_address,
                                )
                                print(msg,'msg============================================')
                                msg.content_subtype = "html"  # Main content is now text/html
                                msg.send()
                                print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

                    if 'Reject Apex Item ID' in subject_mail:
                        print('Reject Apex Item ID-------------------------------------')
                        search_apex_id_reject = f'''
                                    SELECT id, item_code,email
                                        FROM public.app_apextable
                                        WHERE apex_id = '{apex_id}' and apex_status IS NULL order by id desc Limit 1
                                    '''
                        cursor.execute(search_apex_id_reject)
                        apex_id_reject = cursor.fetchall()
                        print(apex_id_reject,'3333333333333333333333333333333333333')
                        if apex_id_reject:
                            print(apex_id_reject,'ssssssssssssssssssssssssssssss00000000000000000000000')
                            for reject_data in apex_id_reject:
                                reject_apex_id = reject_data[0]
                                item_code = reject_data[1]
                                reject_email_ = reject_data[2]
                                try:

                                    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
                                    conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex007', dsn=dsn_tns)
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
                                    cursor_ora.execute(str(query1))

                                    update_mail = f'''UPDATE public.django_mailbox_message SET process_data = 'Reject'
                                    WHERE id = '{recv_msg_id}';'''
                                    cursor.execute(update_mail)
                                    update_mail = f'''UPDATE  public.app_apextable SET apex_status = 'True'
                                                                                         WHERE id = '{reject_apex_id}';'''
                                    cursor.execute(update_mail)
                                    mailbox_subject = f'''SELECT subject FROM public.django_mailbox_message
                                                                    where id = '{recv_msg_id}';
                                                                    '''
                                    cursor.execute(mailbox_subject)
                                    reject_mailbox_ = cursor.fetchall()
                                    for subject in reject_mailbox_:
                                        ctx = {
                                            'item_code': item_code,

                                        }
                                        message = get_template('rejected_mail.html').render(ctx)
                                        msg = EmailMessage(
                                            f'{subject[0]}',
                                            message,
                                            'harshitaagarwal219@gmail.com',  # will be change
                                            message.from_address,
                                        )
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()
                                except:
                                    if recv_msg_id:
                                        update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                WHERE id = '{recv_msg_id}';'''
                                        cursor.execute(update_mail_reject)
                                        mailbox_subject_error = f'''SELECT subject FROM public.django_mailbox_message
                                                                                                           where id = '{recv_msg_id}';
                                                                                                           '''
                                        cursor.execute(mailbox_subject_error)
                                        mailbox_error = cursor.fetchall()
                                        for error_subject in mailbox_error:
                                            subject = error_subject[0]
                                            ctx = {
                                                'item_code': item_code,

                                            }
                                            message = get_template('failed_mail.html').render(ctx)
                                            msg = EmailMessage(
                                                f'{subject}',
                                                message,
                                                'harshitaagarwal219@gmail.com',  # will be change
                                                message.from_address,
                                            )
                                            msg.content_subtype = "html"  # Main content is now text/html
                                            msg.send()
                                    for mailbox in mailboxes:
                                        logger.info(
                                            'Gathering messages for %s',
                                            mailbox.id
                                        )
                                        messages = mailbox.get_new_mail()
                        else:
                            print('Reject error ======================')
                            if recv_msg_id:
                                print(recv_msg_id,'ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                                update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                                           WHERE id = '{recv_msg_id}';'''
                                cursor.execute(update_mail_reject)
                                mailbox_subject_error = f'''SELECT subject FROM public.django_mailbox_message
                                  where id = '{recv_msg_id}';
                                  '''
                                cursor.execute(mailbox_subject_error)
                                mailbox_error = cursor.fetchall()
                                for error_subject in mailbox_error:
                                    subject = error_subject[0]
                                    ctx = {
                                        'item_code': item_code,

                                    }
                                    message = get_template('failed_mail.html').render(ctx)
                                    msg = EmailMessage(
                                        f'{subject}',
                                        message,
                                        'harshitaagarwal219@gmail.com',  # will be change
                                        message.from_address,
                                    )
                                    msg.content_subtype = "html"  # Main content is now text/html
                                    msg.send()
                            for mailbox in mailboxes:
                                logger.info(
                                    'Gathering messages for %s',
                                    mailbox.id
                                )
                                messages = mailbox.get_new_mail()
                else:
                    for mailbox in mailboxes:
                        logger.info(
                            'Gathering messages for %s',
                            mailbox.id
                        )
                        messages = mailbox.get_new_mail()

            except:
                for mailbox in mailboxes:
                    logger.info(
                        'Gathering messages for %s',
                        mailbox.id
                    )
                    messages = mailbox.get_new_mail()



def approve_error(recv_msg_id,item_code,email_):
    print('Approve not---------------------------')
    if recv_msg_id:
        print(recv_msg_id, 'eeeeeeeeeeeeeeeeeeee')

        update_mail_reject = f'''UPDATE public.django_mailbox_message SET process_data = 'Error'
                                                                                       WHERE id = '{recv_msg_id}';'''
        cursor = connection.cursor()
        cursor.execute(update_mail_reject)
        mailbox_subject_error = f'''SELECT subject FROM public.django_mailbox_message
                                                                    where id = '{recv_msg_id}';
                                                                    '''
        cursor.execute(mailbox_subject_error)
        mailbox_error = cursor.fetchall()
        for error_subject in mailbox_error:
            subject = error_subject[0]
            ctx = {
                'item_code': item_code,

            }
            message = get_template('failed_mail.html').render(ctx)
            msg = EmailMessage(
                f'{subject}',
                message,
                'harshitaagarwal219@gmail.com',  # will be change
                message.from_address,
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
    # for mailbox in mailboxes:
    #     logger.info(
    #         'Gathering messages for %s',
    #         mailbox.id
    #     )
    # messages = mailbox.get_new_mail()