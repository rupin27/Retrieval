import json, os, sys, time, math

class QL():
    def __init__(self, file):
        self.start_time = time.time()
        self.fileName = file
        self.tokens = []
        self.dict = {}
        self.sId_cnt = {}
        self.docs_count = {}        
        self.mu = 250        
        self.tlWrdAccur = 0
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

   
    def info_docCount(self):
        listLen = []
        for items in self.dict:
            text = items['text'] 
            tokens = text.split(' ')
            tokens.remove('')
            listLen.append(len(tokens)) 
            self.docs_count[items['sceneId']] = len(tokens) 
        for item in listLen:
            self.tlWrdAccur += item    
  
    def process_query(self, file):
        query = open(os.path.join(sys.path[0], file), 'r')
        query_list = []
        for lines in query:
            samp = lines.strip('\n').split(' ')
            query_list.append(samp)
        for elem in query_list:
            self.query_dict[elem[0]] = elem[1:]


    def formula(self, f_qid, cqi, D):
        numer = f_qid + (self.mu * (float(cqi) / self.tlWrdAccur))
        denom = D + self.mu
        result = math.log(numer/ denom)
        return result

    #Makes a dictionary with format {word: [[playId, sceneId, sceneNum, count], ....]}
    def ql(self):
        (key, val) = self.query_dict.items()[0]
        for item in val: #each query word
            if item in self.sId_cnt:  #count dictionary for qWord i
                word_infos = self.sId_cnt[item] #list of files and count
                word_fqid = 0
                word_D = 0
                word_cqi = 0
                for elem in word_infos:
                    word_cqi += elem[3]
                for items in word_infos:
                    word_fqid = items[3] 
                    word_D = self.docs_count[items[1]]
                    if (items[1] in self.doc_score):
                        self.doc_score[items[1]] += self.formula(word_fqid, word_cqi, word_D)
                    else:
                        self.doc_score[items[1]] = self.formula(word_fqid, word_cqi, word_D)
        result = sorted(self.doc_score.items(), key=lambda x: x[1], reverse = True)
        return result

    def print_output(self, file):
        output = open(os.path.join(sys.path[0].replace('/src', ''), file), 'a')
        x = self.ql()
        (key, val) = self.query_dict.items()[0]
        i = 1
        for items in x:
            string = "{} skip {:<40} {:<4} {:<15} rm27-bm25\n".format(key, items[0], i, items[1])
            output.write(string)
            i += 1
    
if __name__ == '__main__':
    file = "shakespeare-scenes.json"
    I = QL(file)
    I.getInput()
    I.terms_Loc_Count()
    I.info_docCount()
    I.process_query("query.txt")
    I.print_output("ql.trecrun")
    print("{} seconds".format(time.time() - I.start_time))

