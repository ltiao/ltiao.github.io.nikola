FROM python:3.5.2

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    locales \
    rubygems && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /usr/src/site
VOLUME /usr/src/site
WORKDIR /usr/src/site

COPY requirements.txt /usr/src/site
RUN pip install --no-cache-dir -r requirements.txt

# Locale settings
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8  
ENV LC_ALL en_US.UTF-8  

RUN sed -i -e "s/# $LANG.*/$LANG UTF-8/" /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    update-locale LANG=$LANG

# Nikola plugin dependencies 
# TODO: Should be read from plugins directory
RUN nikola plugin --user --install sass

RUN gem install sass

EXPOSE 8000
ENTRYPOINT ["nikola"]
