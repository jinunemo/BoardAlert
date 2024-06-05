import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# SendGrid API 키 설정
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

def get_env_variable(variable_name):
    value = os.environ.get(variable_name)
    if value is None:
        raise ValueError(f"환경 변수 '{variable_name}'를 찾을 수 없습니다.")
    return value



def test_sendingemail():
    # 이메일 전송
    try:
        response = sg.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending the email: {e}")    

def get_new_posts(prev_content):
    url = 'http://www.qldvision.com.au/bbs/board.php?bo_table=job'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the content from {url}")

    soup = BeautifulSoup(response.content, 'html.parser')

    title_element = soup.find('div', class_='tbl_head01')

    target_row = None
    for row in title_element.select('tr'):
        td_num = row.select_one('td.td_num')
        if td_num and td_num.get_text(strip=True).isdigit():
            target_row = row
            break

    # 상위 제목 가져오기
    if target_row:
        td_subject = target_row.select_one('td.td_subject')
        if td_subject:
            top_title = td_subject.get_text(strip=True)
            print(top_title)
    
    return top_title != prev_content, top_title

def main():
    prev_content = ""
    sender_email = os.environ.get('SENDER_EMAIL')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    while True:
        result, new_content = get_new_posts(prev_content)
        if result:
            
            print("새로운 글이 올라왔습니다!")
            # 여기에 알람을 주는 로직을 추가하면 됩니다. (이메일, 푸시 알림 등)
            try:
                message = Mail(
                    from_email = sender_email,
                    to_emails = recipient_email,
                    subject = 'New post alarm',
                    html_content = f"<strong>{new_content}</strong> <br> \
                    http://www.qldvision.com.au/bbs/board.php?bo_table=job")
                response = sg.send(message)
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error sending the email: {e}")   

        prev_content = new_content
        time.sleep(60)  # 1분에 한 번씩 게시판 상태 확인

if __name__ == '__main__':
    main()
