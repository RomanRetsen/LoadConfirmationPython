[comment]: <> (<p align="center">)
[comment]: <> (  <a href="https://github.com/RomanRetsen/LoadConfirmationPython" title="Load Confirmation Application">)
[comment]: <> (    <img src="./resources/icons/logo.png" alt="Load Confirmation" />)
[comment]: <> (  </a>)
[comment]: <> (</p>)
[comment]: <> (<h3 align="center">Load Confirmation</h3>)
![GitHub Logo](/resources/icons/logo.png)
Format: ![Load Confirmation](https://github.com/RomanRetsen/LoadConfirmationPython)

Load Confirmation application is a free, open source accounting software designed for small businesses. It's responsible for generating load tender/confirmation used in transportation industry .....

## Requirements

* PyQt5
* ORACLE Database (12C)
* cx_oracle 8.2.1
* pyreportjasper 2.1.2

## Installation

* Install rdbms Oracle and import sample schema by executing files:
  * create_schema_loadconfirmation_ddl.sql (as a SYSTEM user)
  * import_data_loadconfirmation_dmp.sql (as a loadconfirmation user)
* Install python module dependencies from the file:
  * `pip install -r requirements.txt`