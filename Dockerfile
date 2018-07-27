
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6.5

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=autocourseinfoextract Version=0.0.1
EXPOSE 3000

WORKDIR /app/Autocourseinfoextract 
COPY . /app/Autocourseinfoextract


<<<<<<< HEAD

# Using pip:
RUN pip install -r requirements.txt

=======


# Using pip:
RUN pip install -r requirements.txt
>>>>>>> f7f3467256c511a1bf074880fc7c9ae6f9afd1a9
#ENV PYTHONPATH="$PYTHONPATH:/app/Autocourseinfoextract"
CMD ["python","./AutoCourseInfo_Wrapper/CourseExtractWrapper.py"]



# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "autocourseinfoextract"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m autocourseinfoextract"
