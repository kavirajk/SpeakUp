##SpeakUp

> Kaviraj

A Simple blog application using webpy and postgresql. It features simple login/signup mechanism using sessions.

##Requirements
<ol>
  
  <li>python 2.7.5 or above</li>
  <li>posgresql 9.3.4</li>
  <li>web.py 0.37</li>
  
</ol>

##How to Run

###Make postgresql ready

<pre>
bash-4.2$ createdb -U postgres speakup
bash-4.2$ pg_restore -U postgres -d speakup schema.sql
</pre>

###From the project root directory and execute following command.

<pre>
bash-4.2$ python bin/speakup.py
</pre>





