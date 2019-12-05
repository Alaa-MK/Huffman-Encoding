import queue
class HuffmanTree():
    def __init__(self, filename):
        self.filename=filename
        self.codes={}
        self.freq={}
        self.pq=queue.PriorityQueue()
        self._fill_freq_dict(filename)
        self._fill_pq()
        self._fill_codes()
        
    def save_compressed(self,outfilename):
        with open(self.filename, 'r') as infile:
            with open(outfilename, 'w') as outfile:
                while(True):
                    c=infile.read(1)
                    if not c:
                        break
                    outfile.write(self.codes[c])
                
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
    filename="test.txt"
    h = HuffmanTree(filename)
    h.save_compressed("out.txt")
    
    
    
if __name__=="__main__":
    main()
            