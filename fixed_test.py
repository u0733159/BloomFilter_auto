import string
import mmh3
from bitarray import bitarray 

##reutrn true if the chractre is in the string
def find(str, ch):
    if ch in str:
        return True;
    else:
        return False;
###return true if at least one character in the character list is in the string
def contain(str, chlist):
    flag = False;
    for i in range(0, len(chlist)):
        flag = flag or find(str, chlist[i]);
    if flag:
        return True;
    else:
        return False;
##bloom filter
class BloomFilter:
    ##COnstructor
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.filtered_auto = []
       # self.q = Queue.Queue()
        
    def add(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1
    ##look up the string to check if it is in the bit array        
    def lookup(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                return "Nope"
        return "Probably"
    ## Detect the auto parts in each sentence, sentence here is a list of string;
    ## auto parts is replaced with ****, and the output is appended to the filtered_auto list    
    def sentence_auto_detector(self, sentence):
        print("Sentence in detector is: \n");
        print(sentence);
        newstring = '';
        if len(sentence) == 1:
           ss = sentence[0][:-1];
           if self.lookup(ss) == "Nope":
                newstring = ss + sentence[0][len(sentence[0])-1];
                self.filtered_auto.append(newstring);
           else:
                newstring = "****" + sentence[0][len(sentence[0])-1];
                self.filtered_auto.append(newstring)
        if len(sentence) == 2:
           ss = sentence[0] + sentence[1][:-1];
           ss2 = sentence[0].strip();
           ss3 = sentence[1][:-1];
           if self.lookup(ss) == "Nope" and self.lookup(ss2) == "Nope" and self.lookup(ss3) == "Nope":
                newstring = newstring + sentence[0] + sentence[1];
                self.filtered_auto.append(newstring);
           if self.lookup(ss) == "Nope" and self.lookup(ss2) == "Probably" and self.lookup(ss3) == "Probably":
                newstring = newstring + "**** " + "****" + sentence[1][len(sentence[0])-1];
                self.filtered_auto.append(newstring);
           if self.lookup(ss) == "Nope" and self.lookup(ss2) == "Nope" and self.lookup(ss3) == "Probably":
                newstring = newstring + sentence[0] + "****" + sentence[1][len(sentence[0])-1];
                self.filtered_auto.append(newstring);
           if self.lookup(ss) == "Probably":
                newstring = newstring + sentence[0] + sentence[1];
                self.filtered_auto.append(newstring);
        print len(sentence);
        if len(sentence) >= 3:
            print("Enter sentence bigger than 3\n");
            i = 0;
            tri_exist = False;
            big_exist = False;
            uni_exist = False;
            sign = sentence[len(sentence)-1][len(sentence[len(sentence)-1])-1];
            sentence[len(sentence)-1] = sentence[len(sentence)-1][0:(len(sentence[len(sentence)-1])-1)];
            newsentence = '';
            while i < len(sentence):
                if (i + 3) <= len(sentence):
                    trigram = sentence[i:(i+3)];
                    trigram_string = sentence[i] + sentence[i+1] + sentence[i+2].strip();
                    print(trigram_string);
                    tri_exist = True;
                if (i + 2) <= len(sentence):
                    bigram = sentence[i:(i+2)];
                    bigram_string = sentence[i] + sentence[i+1].strip();
                    big_exist = True;
                if (i+1) <= len(sentence):
                    unigram = sentence[i];
                    unigram_string = sentence[i].strip();
                    uni_exist = True;
                    #print("unigram");
                    
                if tri_exist | big_exist | uni_exist:
                    if tri_exist == True:
                        if self.lookup(trigram_string) == "Probably":
                            newsentence =newsentence +  "****" + trigram[2][len(trigram[2])-1];
                            i = i+3;
                        if self.lookup(trigram_string) == "Nope" and self.lookup(bigram_string) == "Probably":
                            newsentence =newsentence + "****" + bigram[1][len(bigram[1])-1];
                            i = i+2;
                        if self.lookup(trigram_string) == "Nope" and self.lookup(bigram_string) == "Nope" and self.lookup(unigram_string) == "Probably":
                            newsentence =newsentence + "****" + unigram[len(unigram)-1];
                            i = i + 1;
                        if self.lookup(trigram_string) == "Nope" and self.lookup(bigram_string) == "Nope" and self.lookup(unigram_string) == "Nope":
                            newsentence = newsentence + trigram[0];
                            print(newsentence);
                            i = i + 1;
                    if tri_exist == False and big_exist == True:
                        if self.lookup(bigram_string) == "Probably":
                            newsentence =newsentence + "****" + bigram[1][len(bigram[1])-1];
                            i = i+2;
                        if self.lookup(bigram_string) == "Nope" and self.lookup(unigram_string) == "Probably":
                            newsentence = newsentence + "****" + unigram[len(unigram)-1] +bigram[1];
                            i = i + 1;
                        if self.lookup(bigram_string) == "Nope" and self.lookup(unigram_string) == "Nope":
                            newsentence = newsentence + bigram[0] + bigram[1];
                            i = i + 1;
                    if tri_exist == False and big_exist == False and uni_exist == True:
                        if self.lookup(unigram_string) == "Probably":
                            newsentence = newsentence + "****" + unigram[0][len(unigram[0])-1];
                            #i = i + 1;
                        i = i + 1;
                tri_exist = False;
                big_exist = False;
                uni_exist = False;
            newsentence = newsentence + sign;
            print("newsentence is: ");
            print(newsentence);
            self.filtered_auto.append(newsentence);

####function returns a list of list of sentences
    def parseText(self, filename):
        wordList = [];
        wordCount = 0;
        filecontent = open(filename, 'rU');
        for line in filecontent:
            for word in line.split():
                wordList.append(word)
                wordCount += 1
        sentences = [];
        print("word list is: ");
        print(wordList);
        s = [];
        signs = ['.', ',', '?', '!', ';', ':']
        flag = True;
        for i in range(0, len(wordList)):
            if contain(wordList[i], signs) != True:
                s.append(wordList[i] + ' ');
            else:
                s.append(wordList[i]);
                sentences.append(s);
                s = [];
        filecontent.close();
        print("sentences is :");
        print(sentences);
        return sentences;

    ##Return a list of strings, this list should has no auto parts after using this function.
    def autoDetector(self, filename):
        print("Enter autoDetector function:\n");
        content = self.parseText(filename);
        print("Content is: \n");
        print content;
        output_content = [];
        for i in range(0, len(content)):
            self.sentence_auto_detector(content[i]);
        print("Result is:");
        print(self.filtered_auto);
        print output_content;



bf = BloomFilter(500000, 7);
autofile = open('auto-words.txt');

for line in autofile:
    bf.add(line[0:(len(line) - 1)])
autofile.close();

bf.autoDetector("test2.txt");




