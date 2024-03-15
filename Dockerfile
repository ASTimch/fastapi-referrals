FROM python:3.10

RUN mkdir /referral

WORKDIR /referral

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod a+x /referral/startup_scripts/*.sh
