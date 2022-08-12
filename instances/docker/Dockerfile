FROM continuumio/miniconda3

RUN apt-get update

#RUN apt-get install sox ffmpeg libcairo2 libcairo2-dev

#RUN apt-get install texlive-full

#RUN apt install libpython3.9-dev

RUN apt install -y make

RUN conda install -c conda-forge jupyterlab

RUN git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew \
&& mkdir ~/.linuxbrew/bin \
&& ln -s ../Homebrew/bin/brew ~/.linuxbrew/bin \
&& eval $(~/.linuxbrew/bin/brew shellenv) \
&& brew --version

RUN export PATH=$HOME/.linuxbrew/bin:$PATH

RUN conda config --add channels conda-forge

RUN conda config --set channel_priority strict

RUN conda install gcc_linux-64

COPY conda_requirements.txt .

RUN conda install -y --file conda_requirements.txt

RUN conda install -c conda-forge dtale
#RUN conda install -c conda-forge auto-sklearn
RUN conda install -c conda-forge pandas-profiling

COPY pip_requirements.txt .

RUN pip3 install -r pip_requirements.txt

# RUN ngrok authtoken 2DEGDZxDjWuOAR9yVmjir8I9fDB_7szo2ChpoCCk1zRLSnjzD

EXPOSE 8888

# if PYTHONPATH is not included use command below in *.py
# import sys
# sys.path.append('/usr/src')
# ENV PYTHONPATH="/usr/src:$PYTHONPATH"

# WORKDIR /usr/src

# hash password = 1234
# from notebook.auth import passwd
# passwd() <- run this command in notebook to harsh your password

# ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--NotebookApp.token=''", "--NotebookApp.password='sha1:a60aa670ae56:dd1afbc5d9585af67965bc9fe187f315ae31f3d8'","--NotebookApp.allow_password_change=False", "--allow-root"]
ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--NotebookApp.token=''", "--NotebookApp.password=''", "--allow-root", "--autoreload"]
# ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--allow-root"]
