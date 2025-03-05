FROM python:3.12

  RUN apt-get update &

  RUN pip install --upgrade pip

  COPY requirements_fig4figs6figs7.txt .

  RUN pip install -r requirements_fig4figs6figs7.txt