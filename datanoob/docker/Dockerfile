FROM continuumio/miniconda3

RUN apt-get update

RUN apt install -y make

RUN conda install -c conda-forge jupyterlab

COPY conda_requirements.txt .

RUN conda install -y --file conda_requirements.txt

COPY pip_requirements.txt .

RUN pip3 install -r pip_requirements.txt

EXPOSE 8888

# if PYTHONPATH is not included use command below in *.py
# import sys
# sys.path.append('/usr/src')
# ENV PYTHONPATH="/usr/src:$PYTHONPATH"

# WORKDIR /usr/src

# hash password = 1234
# from notebook.auth import passwd
# passwd() <- run this command in notebook to harsh your password

# ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--NotebookApp.token=''", "--NotebookApp.password='sha1:a60aa670ae56:dd1afbc5d9585af67965bc9fe187f315ae31f3d8'", "--allow-root"]
ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--NotebookApp.token=''", "--NotebookApp.password='sha1:a60aa670ae56:dd1afbc5d9585af67965bc9fe187f315ae31f3d8'", "--allow-root", "--autoreload"]
# ENTRYPOINT [ "jupyter", "lab", "--ip='*'","--port=8888", "--no-browser","--allow-root"]
