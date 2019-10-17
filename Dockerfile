FROM python:3
ADD handover_bot.py /
RUN pip install -r requirements.txt
CMD [ "python", "./handover_bot.py" ]
