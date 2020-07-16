FROM continuumio/miniconda

RUN apt-get update
RUN apt-get install -y software-properties-common

RUN apt install -y curl     vim.tiny     python     python-pip
RUN pip install requests==2.23.0
RUN pip install boto3==1.12.40

RUN mkdir -p /usr/workdir
WORKDIR /usr/workdir

RUN echo 'alias ll="ls -ls"' >> ~/.bashrc
RUN echo 'alias vim="vim.tiny"' >> ~/.bashrc

RUN conda init bash
RUN conda create -y --name r_3.2.1 -c conda-forge r=3.2.1 r-essentials
RUN conda create -y --name r_3.6.0 -c r r=3.6.0 r-essentials
RUN conda create -y -n r_4.0.1 -c conda-forge r-base=4.0.1 r-essentials

#RUN conda create -y --name py3 python=3.5
#RUN apt-get install -y libncurses5

ARG r_ver=r_4.0.1 
RUN echo "conda activate $r_ver" >> ~/.bashrc
ENV PATH="/opt/conda/envs/$r_ver/bin:${PATH}"

COPY run_analysis.sh .
RUN ["chmod", "+x", "run_analysis.sh"]
COPY download_dataset.py .
COPY set_environment.py .
COPY exec_r_files.R .
COPY save_result_in_dynamo.py .

ARG DOI=doi
ARG TEST=FALSE

ENTRYPOINT sh run_analysis.sh ${DOI} ${TEST}
