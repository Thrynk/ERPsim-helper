FROM sphinxdoc/sphinx

WORKDIR /ERPsim-helper

COPY ./django_server django_server/

COPY ./Sphinx/docs /ERPsim-helper/Sphinx/docs

COPY requirements.txt /ERPsim-helper/requirements.txt

RUN pip3 install rst2pdf furo sphinx-rtd-theme

CMD sphinx-build -M html Sphinx/docs/source Sphinx/docs/build