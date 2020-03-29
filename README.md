# Time-Matters-Query
Time matters query is the result of a research conducted by Ricardo Campos during his [PhD](http://www.ccc.ipt.pt/~ricardo/ficheiros/PhDThesis_RCampos.pdf) at the [University of Porto](https://www.up.pt/). It builds on top of Time matters algorithm, which was originally implemented in C#. Current version, however, is now available as a [Python package](https://github.com/LIAAD/Time-Matters), developed by [Jorge Mendes](https://github.com/JMendes1995) under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree of the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

## What is Time-Matters-Query?
Time matters query is a [python package](https://github.com/LIAAD/Time-Matters-Query) that aims to score the relevance of temporal expressions found (through time matters [package](https://github.com/LIAAD/Time-Matters)) within a set of texts. To get these texts, users are given the chance to query a system. The current version of this package offers users the chance to get results from the [Arquivo.pt](http://arquivo.pt), portuguese web archive, yet other systems may be easily added.

## Where can I find Time-Matters-Query?
`Time-Matters-Query` can be found as a standalone installation on [github](https://github.com/LIAAD/Time-Matters-Query) and as an API [http://time-matters-query.inesctec.pt/api].

## How to Install Time Matters Query
### Install Time-Matters-Query library

``` bash
pip install git+https://github.com/LIAAD/Time-Matters-Query.git
```
<br>

### Install External Dependencies
You will need to install nltk:

Go to the command line and install nltk through the following command:
``` bash
pip install nltk
```
Then open your python interpreter and write the following code (you can set the download_dir folder to /home/nltk_data when using linux)

``` bash
import nltk
nltk.download('punkt', download_dir='c:/nltk_data')
```

More about this [here](https://medium.com/@vardhmanandroid2015/nltk-how-to-install-nltk-nltk-data-on-window-machine-56cddb05b872)

Time-Matters-Query rests on the extraction of relevant keywords and temporal expressions found in the text.

For the first (that is, the extraction of relevant keywords), we resort to [YAKE!](https://github.com/LIAAD/yake) keyword extractor.

``` bash
pip install git+https://github.com/LIAAD/yake
```

For the latter (that is, the extraction of temporal expressions), we resort to two possibilities:
- [rule-based approach](https://github.com/JMendes1995/py_rule_based)
- [heideltime python wrapper](https://github.com/JMendes1995/py_heideltime)

The first, is an internal self-defined rule-based approach developed in regex. The latter is a Python wrapper for the well-known Heideltime temporal tagger.

To work with the Time-Matters-Query package the following packages should be installed:
``` bash
pip install git+https://github.com/JMendes1995/py_rule_based
pip install git+https://github.com/JMendes1995/py_heideltime
```

You should also have java JDK and perl installed in your machine for heideltime dependencies (note that none of this is needed should your plan is to only use a rule-based approach).

##### Windows users
To install java JDK begin by downloading it [here](https://www.oracle.com/technetwork/java/javase/downloads/index.html). Once it is installed don't forget to add the path to the environment variables. On `user variables for Administrator` add the `JAVA_HOME` as the `Variable name:`, and the path (e.g., `C:\Program Files\Java\jdk-12.0.2\bin`) as the Variable value. Then on `System variables` edit the `Path` variable and add (e.g., `;C:\Program Files\Java\jdk-12.0.2\bin`) at the end of the `variable value`.

For Perl we recomment you to download and install the following [distribution](http://strawberryperl.com/). Once it is installed don't forget to restart your PC.

Note that perl doesn't need to be installed if you are using Anaconda instead of pure Python distribution.

##### Linux users
Perl usually comes with Linux, thus you don't need to install it.

If your user does not have permission executions on python lib folder, you should execute the following command:
sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*

## How to use Time-Matters-Query to query Arquivo.pt
User's are offered the chance to either issue a query or to provide an URL where to look for information. To make this happen, we make use of the textsearch and of the versionHistory feature provided by Arquivo.pt (a description of both APIs is available [here](https://github.com/arquivo/pwa-technologies/wiki/Arquivo.pt-API-v.0.2)).

We highly recommend you to resort to this [Python Notebook](notebook-time-matters-query.ipynb) should you want to play with Time-Matters-Query when using the standalone version.
