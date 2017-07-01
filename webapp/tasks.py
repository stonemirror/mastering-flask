from flask import current_app, render_template
from webapp.extensions import celery
from webapp.models import Reminder, Post
import smtplib
import datetime
from email.mime.text import MIMEText


@celery.task()
def log(msg):
    return msg


@celery.task()
def multiply(x, y):
    return x * y


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    msg = MIMEText(reminder.text)
    server = current_app.config['EMAIL_SERVER']
    user = current_app.config['EMAIL_USER']
    password = current_app.config['EMAIL_PASSWORD']
    msg['Subject'] = "Your reminder"
    msg['From'] = user
    msg['To'] = reminder.email
    try:
        smtp_server = smtplib.SMTP(server)
        smtp_server.starttls()
        smtp_server.login(user, password)
        smtp_server.sendmail(
            user,
            [reminder.email],
            msg.as_string()
        )
        smtp_server.close()
    except Exception, e:
        self.retry(exc=e)


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    year, week = datetime.datetime.now().isocalendar()[0:2]
    date = datetime.date(year, 1, 1)
    if (date.weekday() > 3):
        date = date + datetime.timedelta(days=7 - date.weekday())
    else:
        date = date - datetime.timedelta(days=date.weekday())
    delta = datetime.timedelta(days=(week - 1) * 7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)
    posts = Post.query.filter(
        Post.publish_date >= start,
        Post.publish_date <= end
    ).all()
    if len(posts) == 0:
        return
    msg = MIMEText(
        render_template("digest.html", posts=posts),
        'html'
    )
    msg['Subject'] = "Weekly Digest"
    msg['From'] = current_app.config['EMAIL_USER']
    try:
        server = current_app.config['EMAIL_SERVER']
        user = current_app.config['EMAIL_USER']
        password = current_app.config['EMAIL_PASSWORD']
        smtp_server = smtplib.SMTP(server)
        smtp_server.starttls()
        smtp_server.login(user, password)
        smtp_server.sendmail(
            user,
            ["stonemirror@me.com"],
            msg.as_string()
        )
        smtp_server.close()
        return
    except Exception, e:
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.date)
