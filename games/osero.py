import random

class boards:

    def __init__(self):
        self.frame = "×"
        self.air = "."
        self.status = {0:"○", 1:"●"}
        self.bord = [[self.frame if i in [0,9] or j in [0,9] else self.air for i in range(10)] for j in range(10)]
        self.turn = 0
        self.dir = [
            [1,-1],
            [1,0],
            [1,1],
            [0,1],
            [-1,1],
            [-1,0],
            [-1,-1],
            [0,-1]
        ]

        self.bord[4][4] = self.status[0]
        self.bord[5][5] = self.status[0]
        self.bord[5][4] = self.status[1]
        self.bord[4][5] = self.status[1]

    def view_bord(self):
        '''
        盤面を表示する関数
        '''
        print(" ", " ".join(map(str, range(8))))
        for i, bo in enumerate(self.bord[1:9]):
            print(i, " ".join(bo[1:9]))

    def set(self,koma:int,x:int,y:int):
        '''
        駒を配置・更新する関数
        
        koma : 駒の種類
        x : x座標
        y : y座標
        ---
        '''
        self.bord[x][y] = self.status[koma]
    
    def check_st_line(self,x:int,y:int,d:int,swapable:list):
        '''
        指定座標を始点として直線状に走査する関数
        
        x : x座標
        y : y座標
        d : 方向
        swapable : ひっくり返し可能な座標
        ---
        swapable : ひっくり返し可能な座標
        '''
        next = self.bord[x][y]
        if next not in ("×","."):
            if self.status[self.turn] == next:
                return swapable
            else:
                swapable.append((x,y))
                self.check_st_line(x+self.dir[d][0],y+self.dir[d][1],d,swapable)
        else: 
            swapable.clear()
        return swapable

    def check_radiation(self,x:int,y:int):
        '''
        指定座標を中心として放射状に走査する関数
        
        x : x座標
        y : y座標
        ---
        swapable : ひっくり返し可能な座標
        '''
        swapables = []
        for index,d in enumerate(self.dir):
            swapable = self.check_st_line(x+d[0],y+d[1],index,[])
            swapables.extend(swapable)
        return swapables
    
    def swap(self,x:int,y:int):
        '''
        駒をひっくり返す関数
        
        x : x座標
        y : y座標
        '''
        swap_list = self.check_radiation(x,y)
        for s in swap_list:
            self.set(self.turn,s[0],s[1])

    def setable(self,x:int,y:int):
        '''
        指定座標に駒を置けるか否かを返す関数
        
        x : x座標
        y : y座標
        ---
        1 : 配置可能
        0 : 配置不可能
        '''
        swapable_list = self.check_radiation(x,y)
        return 1 if swapable_list and self.bord[x][y] is self.air else 0
    
    def check_bord(self):
        '''
        盤面上に関する情報を返す関数
        
        ---
        hint : 配置可能な座標
        air_exists : 駒の置き場所
        white : 白の駒の数
        black : 黒の駒の数
        '''
        hint,air_exists = [],False
        white, black = 0, 0

        for i,col in enumerate(self.bord[1:9]):
            for j,d in enumerate(col[1:9]):
                if self.setable(i+1,j+1) : hint.append((j,i))
                if d == self.air : air_exists = True
                elif d == self.status[0] : black+=1
                elif d == self.status[1] : white+=1

        random.shuffle(hint)
        return hint,air_exists,black,white
    
    def screen_win_or_lose(self,bk:int,wh:int):
        '''
        勝敗を表示する関数
        
        bk : 黒の駒数
        wh : 白の駒数
        ---
        '''
        if bk > wh:
            t = f"「{self.status[0]}」の勝利でした"
        elif bk < wh:
            t = f"「{self.status[1]}」の勝利でした"
        else :
            t = "両者引き分けでした"
        print(f"黒{bk}、白{wh}により、"+t)


def main(player:bool=True): 

    error_message = ""
    b = boards()

    while True:

        b.view_bord()
        print("\n")
        hint,exists,bk,wh = b.check_bord()

        if not exists:
            b.screen_win_or_lose(bk,wh)
            break

        if player and b.turn:
            if hint:
                b.set(b.turn,hint[-1][1]+1,hint[-1][0]+1)
                b.swap(hint[-1][1]+1,hint[-1][0]+1)
                b.turn = not b.turn
                error_message = ""
                continue

        if not hint:
            error_message="置くことができません、再び"
            b.turn = not b.turn
            hint,_,_,_ = b.check_bord()
            if not hint:
                b.screen_win_or_lose(bk,wh)
                break
            continue

        print(f'{error_message}「{b.status[b.turn]}」の番です')
        print("ヒント：",*hint)
        i = list(map(int, input('「横 縦」のように入力してください：').split()))
        print("\n\n")

        if not b.setable(i[1]+1,i[0]+1):
            error_message = '置くことができません、'
            continue

        b.set(b.turn,i[1]+1,i[0]+1)
        b.swap(i[1]+1,i[0]+1)
        b.turn = not b.turn
        error_message = ""

if __name__=="__main__":
    main()