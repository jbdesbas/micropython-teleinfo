from os import dupterm
from machine import UART  

class Teleinfo:
    def __init__(self, uart):   
        #dupterm(None, 1) #  Detech REPL
        self.uart = uart
    
    def get_next_trame(self):
        self.uart.init(1200, bits=7, parity=0, stop=1,rxbuf=200,timeout=100)
        self.uart.read(); #Flush serial
        trame = []
        while True:
            if self.uart.any():
                t=self.uart.read(1)
                if t != b'\x02' and len(trame) == 0:
                    continue
                if len(trame) > 0 and t == b'\x03':
                    return Trame(trame)
                trame.append(t)


class Trame:
    def __init__(self, arr):
        self.arr=arr
        self.infos=self._get_group_info()
        self.infos_dict=dict()
        for i in self.infos:
            self.infos_dict[i.lib]=i.val
    
    def _get_group_info(self):
        offset=0
        out=[]
        while True:
            try :
                start=self.arr.index(b'\x0A',offset)
                stop=self.arr.index(b'\x0D',offset+1)
                out.append(GroupInfo(self.arr[start+1:stop]))
                offset = stop
            except ValueError:
                return out


class GroupInfo:
    def __init__(self, arr):
        self.arr=arr
        d = self._extract_info()
        self.lib = d['lib']
        self.val = d['val']
    
    def _extract_info(self):
        lib_pos = (0, self.arr.index(b'\x20') )
        data_pos = (lib_pos[1]+1, self.arr.index(b'\x20', lib_pos[1]+1))
        checksum_pos = (data_pos[1]+1, len(self.arr))
        
        lib = ''.join( [x.decode() for x in self.arr[lib_pos[0]:lib_pos[1]] ])
        data = ''.join( [x.decode() for x in self.arr[data_pos[0]:data_pos[1]] ] )
        checksum = ''.join( [x.decode() for x in self.arr[ checksum_pos[0]: ] ])
        return {'lib':lib, 'val':data, 'ck':checksum}

    #TODO checksum
    
    def __repr__(self):
        return '<GroupInfo {} : {} >'.format(self.lib, self.val)
