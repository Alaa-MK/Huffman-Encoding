import queue
import pickle
import math
import bitarray as ba
import sys

class HuffmanTree():   
    
    class encoding_info():
        def __init__(self, count, codes):
            self.count=count
            self.codes=codes
    
    def __init__(self):
        self._reset()
        
    def _reset(self):
        self.codes={}
        self.freq={}
        self.count=0
        self.pq=queue.PriorityQueue()        
        
    def average_code_length(self):
        s = sum([self.freq[x] for x in self.freq.keys() if len(x)==1])
        return sum([(self.freq[x]/s)*len(self.codes[x]) for x in self.codes.keys()])
        
    def entropy(self):
        s = sum([self.freq[x] for x in self.freq.keys() if len(x)==1])
        return sum([-(self.freq[x]/s)*math.log2(self.freq[x]/s) for x in self.codes.keys()])
    
    def compression_ratio(self):
        return self.average_code_length()/8
    
    def efficiency(self):
        return self.entropy()/self.average_code_length()
    
    def compress(self,infilename, outfilename):
        self._reset()
        self._fill_freq_dict(infilename)
        self._fill_pq()
        self._fill_codes()
        
        #compress the file
        s=""
        with open(infilename, 'r') as infile:
            while(True):
                c=infile.read(1)
                if not c:
                    break
                s+=self.codes[c]
        with open(outfilename, 'wb') as outfile:
            b=ba.bitarray(s)
            b.tofile(outfile)
            
        self.count=len(s)
        #save the codes to file
        pickle.dump(self.encoding_info(self.count, self.codes), open (outfilename+"_encoding.bin", "wb"))
    
    def decompress(self,infilename, outfilename):
        self._reset()
        info=pickle.load(open (infilename+"_encoding.bin", "rb"))
        self.count=info.count
        self.codes=info.codes
        inv_codes = {v: k for k, v in self.codes.items()}
        
        #decompress the file
        b=ba.bitarray()
        s=""
        with open(infilename, 'rb') as infile:
            b.fromfile(infile)
        for i in range(b.length()):
            s+= ("1" if b[i] else "0")
        with open(outfilename, 'w') as outfile:
            temp=""
            for i in range(self.count):
                temp+= s[i]
                c=inv_codes.get(temp)
                if c is not None:
                    outfile.write(c)
                    temp=""

    def _fill_freq_dict(self,filename):
        with open(filename, 'r') as f:
            while(True):
                c=f.read(1)
                if not c:
                    break
                if c not in self.freq.keys():
                    self.freq[c]=1
                    self.codes[c]="";
                else:
                    self.freq[c]+=1
                  
    def _fill_pq(self):
        for key,value in self.freq.items():
            self.pq.put((value, key))
            
    def _fill_codes(self):
        #there is no need to create a tree, since we can update the codes directly
        while self.pq.qsize() > 1:
            first=self.pq.get()[1]
            second=self.pq.get()[1]
            for c in first:
                self.codes[c]='0'+self.codes[c]
            for c in second:
                self.codes[c]='1'+self.codes[c]
            self.freq[first+second]=self.freq[first]+self.freq[second]
            self.pq.put((self.freq[first+second], first+second))
            
            
def main():
    #test
    filename="test.txt"
    h = HuffmanTree()
    h.compress(filename, "out.bin")
    print("Average Code Length: ", h.average_code_length())
    print("Entropy: ", h.entropy())
    print("Compression ratio: ", h.compression_ratio())
    print("Efficiency: ", h.efficiency())
    h.decompress("out.bin", "decoded.txt")
    
    
    
    
if __name__=="__main__":
    main()
            