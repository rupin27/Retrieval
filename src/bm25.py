import json, os, sys, time, math

class BM25():
    def __init__(self, file):
        self.start_time = time.time()
        self.fileName = file
        self.tokens = []
        self.dict = {}
        self.sId_cnt = {}
        self.docs_count = {}        
        self.ri = 0
        self.R = 0
        self.k1 = 1.8
        self.k2 = 5
        self.b = 0.75
        self.N = 0     
        self.lenAvgDoc = 0
        self.query_dict = {}
        self.doc_score = {}

    def getInput(self):
        json_file = open(os.path.join(sys.path[0], self.fileName), 'r')
        self.dict = json.load(json_file)
        self.dict = self.dict['corpus']
        #self.dict = json.dumps(self.dict)
        json_file.close()

    #Makes a dictionary with format {word: [[playId, sceneId, sceneNum, count], ....]}
    def terms_Loc_Count(self):
        for items in self.dict:
            text = items['text']
            self.tokens.extend(text.split(' '))
        self.tokens = list(set(self.tokens))
        self.tokens.remove('')
        for word in self.tokens:
            self.sId_cnt[word] = []
            for items in self.dict:
                if word in items['text']:
                    if word not in self.sId_cnt:
                        self.sId_cnt[word].append([items['playId'], items['sceneId'], items['sceneNum'], items['text'].count(word)])
                    else:
                        if items['sceneId'] not in self.sId_cnt[word]:
                            self.sId_cnt[word].append([items['playId'], items['sceneId'], items['sceneNum'], items['text'].count(word)])

   
    def info_averageLen(self):
        listLen = []
        for items in self.dict:
            text = items['text'] 
            tokens = text.split(' ')
            tokens.remove('')
            listLen.append(len(tokens)) 
            self.docs_count[items['sceneId']] = len(tokens)     
        sum = 0
        count = len(listLen)
        for item in listLen:
            sum += item
        self.lenAvgDoc = float(sum) / count
        self.N = len(self.dict)
  
    def process_query(self, file):
        query = open(os.path.join(sys.path[0], file), 'r')
        query_list = []
        for lines in query:
            samp = lines.strip('\n').split(' ')
            query_list.append(samp)
        for elem in query_list:
            self.query_dict[elem[0]] = elem[1:]
    
    def KValue(self, dl):
        self.K = self.k1 * ((1 - self.b) + (self.b * (dl / self.lenAvgDoc)))
        return self.K    
    
    def formula(self, ni, fi, qfi, dl):
        numer = (self.ri + 0.5) / (self.R - self.ri + 0.5)
        denom = (ni - self.ri + 0.5) / (self.N - ni - self.R + self.ri + 0.5)
        frm2 = ((self.k1 + 1) * fi) / (self.KValue(dl) + fi)
        frm3 = ((self.k2 + 1) * qfi) / (self.k2 + qfi)
        result = math.log(numer / denom) * frm2 * frm3
        return result
    
    #Makes a dictionary with format {word: [[playId, sceneId, sceneNum, count], ....]}
    def BM25(self):
        (key, val) = self.query_dict.items()[0]
        unq_vals = list(set(val))
        for item in unq_vals:
            if item in self.sId_cnt:
                word_infos = self.sId_cnt[item]
                word_ni = len(word_infos)
                word_qfi = val.count(item)  
                for elem in word_infos:
                    word_fi = elem[3]
                    if (elem[1] in self.doc_score):
                        self.doc_score[elem[1]] += self.formula(word_ni, word_fi, word_qfi, self.docs_count[elem[1]])
                    else:
                        self.doc_score[elem[1]] = self.formula(word_ni, word_fi, word_qfi, self.docs_count[elem[1]])
                        
        result = sorted(self.doc_score.items(), key = lambda x: x[1], reverse = True)
        return result
    
    def print_output(self, file):
        output = open(os.path.join(sys.path[0].replace('/src', ''), file), 'a')
        x = self.BM25()
        (key, val) = self.query_dict.items()[0]
        i = 1
        for items in x:
            string = "{} skip {:<40} {:<4} {:<15} rm27-bm25\n".format(key, items[0], i, items[1])
            output.write(string)
            i += 1

if __name__ == '__main__':
    file = "shakespeare-scenes.json"
    I = BM25(file)
    I.getInput()
    I.terms_Loc_Count()
    I.info_averageLen()
    I.process_query("query.txt")
    I.print_output("bm251.trecrun")
    print("{} seconds".format(time.time() - I.start_time))

