# Retrieval Implementation
<p>
The purpose of this project is to explore the language modeling and BM25 scoring functions on a small collection of documents.
</p>

# Downloading Dependencies:
<p>
Download the zip and you will find the following components in file: 
</p>

<pre>
1) <b><i>src/*</b></i> : Contains the source code, source text, and a test file to check input the query.
               a)bm25.py
               b)QL.py
               c)shakespeare-scenes.json
               d)query.txt 
              
The results from various test queries are returned as shown below:
<b><i>bm25.trecrun/*</b></i>: Scored for documents based on BM25 modeling using k1 = 1.8, k2 = 5, b = 0.75. (Values can be changed accordingly)
<b><i>ql.trecrun/*</b></i>: Scored for documents based on Query-Likelihood modeling (using Dirichlet Smoothing) using mu = 250.
</pre>
Examples of input Queries:
<ul>
        <li>Q1: the king queen royalty </li>
        <li>Q2: servant guard soldier </li>
        <li>Q3: hope dream sleep </li>
        <li>Q4: ghost spirit </li>
        <li>Q5: fool jester player </li>
        <li>Q6: to be or not to be</li>
</ul>
<p>

To process the queries, the code consists of a general query-processing language for all types of input queries through which it should take very little effort to run minor variations on queries. Once it processes the queries, we find the result according to what is requested based on the information stored in the lists and return it a trecrun format.
</p>

# Building the Code:
To build the code, simply run the bm25.py or QL.py in the src folder to get the result of the query as inserted in the query.txt file:
<pre>
blm.py / QL.py.py : Imports the required file(shakespeare-scenes.json) and builds a simple inverted index with positional information.
                   It does so by storing the data into a list of the format:
                   <i>self.sId_cnt</i>: {word: [[playId, sceneId, sceneNum, count], ....]}    
                      : Stores the word information along with it's count in that text.
</pre>
Input Format: An example scene looks like below:
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code> 

{
  "playId" : "antony_and_cleopatra",
  "sceneId" : "antony_and_cleopatra:2.8",
  "sceneNum" : 549 ,
  "text" : "scene ix another part of the plain enter mark antony and domitiu enobarbu mark antony
            set we our squadron on yond side o the hill in eye of caesar s battle from which place
            we may the number of the ship behold and so proceed accordingly exeunt "
}
</code></pre></div></div>
<div>
The query processor will tokenize the document into a dictionary:
<pre>
{‘Q1’: [‘the’, ‘king’, ‘queen’, ‘royalty’]}
</pre>
For this query, we iterate through each word and calculate the BM24/QL score based on the word for the document and then store the score. We keep doing this based on each term and finally add up to tally the final score for the document.
</div>

# Output:
For both tasks, the submission consists of a single text file in the format used for most TREC submissions where:
<pre>
        "Q2: skip antony_and_cleopatra:4.1                 1    6.30275682757   rm27-bm25"

column 1 is the topic number.
column 2 is currently unused and is assigned "skip".
column 3 is the scene identifier of the retrieved document.
column 4 is the rank the document is retrieved. 
column 5 shows the score that generated the ranking. This score is in descending (non-increasing) order.
column 6 is called the "run tag" and is the OIT identifier.
</pre>
   
# Running the Code:

The src file import the input text file and running the code will return the output file in the main directory. 
The query to be searched needs to be written in the input.txt file.
