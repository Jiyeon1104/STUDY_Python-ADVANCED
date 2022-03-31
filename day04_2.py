import sys                     
from PyQt5.QtWidgets import *  
from PyQt5 import uic          
from PyQt5.QtCore import *   
import pybithumb

form_class = uic.loadUiType("day04.ui")[0]   
tickers = ["BTC","ETH","XRP","ADA"]

class MyWindow(QMainWindow, form_class):     
    def __init__(self):                      
        super().__init__()              
        self.setupUi(self)               
        # self.pushButton.clicked.connect(self.btn_clicked)  
        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.timeout)

    def get_market_infos(self, ticker):
        df = pybithumb.get_ohlcv(ticker) # get_ohlcv() 해당 코인의 다양한 정보를 가져옴
        ma5 = df['close'].rolling(window = 5).mean() # 종가들을 5일씩 평균을 전부 계산
        last_ma5 = ma5[-2]                           # 가장 최근 5일치의 평균만 추출
        price = pybithumb.get_current_price(ticker)  # 해당 코인의 현재가

        state = None
        if price > last_ma5:
            state = "상승장"
        else : 
            state = "하락장"

        return price, last_ma5, state

    def timeout(self):
        for i, ticker in enumerate(tickers):

            item = QTableWidgetItem(ticker)
            self.tableWidget.setItem(i, 0, item)

            price, last_ma5, state = self.get_market_infos(ticker)

            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(state)))

        
app = QApplication(sys.argv)                 
window = MyWindow()                          
window.show()                               
app.exec_()                        