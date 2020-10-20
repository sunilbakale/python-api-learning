


FROM python:alpine3.8 
COPY . /app
WORKDIR /app
RUN python3 -m venv env
#RUN /env/bin/activate
RUN pip install --upgrade pip --user
RUN pip install -r requirements.txt 
EXPOSE 5001
ENTRYPOINT [ "python" ] 
CMD [ "server.py" ] 
