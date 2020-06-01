FROM rocker/r-ver:3.4.2

RUN apt-get update 
RUN apt-get install -y software-properties-common 
RUN apt install -y curl \
	vim.tiny \
	python \
	python-pip

RUN pip install requests==2.23.0
RUN pip install boto3==1.12.40

RUN mkdir -p /usr/workdir
WORKDIR /usr/workdir

RUN echo 'alias ll="ls -ls"' >> ~/.bashrc
RUN echo 'alias vim="vim.tiny"' >> ~/.bashrc

RUN curl -o ~/anaconda.sh https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-x86_64.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh 
RUN ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN /bin/bash -c "source /etc/profile.d/conda.sh"
ENV PATH /opt/conda/bin:$PATH
RUN conda install -y boto3

RUN conda create -y -n r_env r-essentials r-base
RUN echo "conda activate r_env" >> ~/.bashrc

COPY run_analysis.sh .
RUN ["chmod", "+x", "run_analysis.sh"]
COPY download_dataset.py .
COPY set_environment.py .
COPY exec_r_files.R .
COPY save_result_in_dynamo.py .

ARG DOI=doi
ENTRYPOINT sh run_analysis.sh ${DOI}