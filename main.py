import csv
with open('trades.csv', newline='') as csvfile:
    lines = csv.reader(csvfile, delimiter=' ')
    rows=[]
    for row in lines:
        rows.append(row[0].split(','))
##print(rows[1:])
"""
    Structure for unmatched order book
    {
        Symbol:{
                Buy-Min-Heap named as buy: 
                        Contains a min heap with respect to Buy time
                        where each node has the following Structure-
                                Node[
                                    Buy Time,
                                    Quantity,
                                    Price
                                ]
                ,Sell-Min-Heap named as sell: 
                        Contains a min heap with respect to Sell time
                        where each node has the following Structure-
                                Node[
                                    Sell Time,
                                    Quantity,
                                    Price
                                ]
                }
    }

"""
import heapq
inventory={}
total_profit=0
print("OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE")
for row in rows:
    time=row[0]
    symbol=row[1]
    side=row[2]
    price=row[3]
    quantity=row[4]
    if symbol not in inventory:
        inventory[symbol]=dict()
        inventory[symbol]["buy"]=[]
        inventory[symbol]["sell"]=[]
    Node=[
            time,
            quantity,
            price
        ]
    if side=='B':
        heapq.heappush(inventory[symbol]["buy"],Node)
    else:
        heapq.heappush(inventory[symbol]["sell"],Node)

    #Now we have added the new trade in our inventor, and we can now check if they match or not.

    if len(inventory[symbol]['buy'])>0 and len(inventory[symbol]['sell'])>0:
        buy_order=heapq.heappop(inventory[symbol]['buy'])
        sell_order=heapq.heappop(inventory[symbol]['sell'])
        buy_amt=float(buy_order[1])
        buy_time=float(buy_order[0])
        buy_price=float(buy_order[2])
        sell_amt=float(sell_order[1])
        sell_time=float(sell_order[0])
        sell_price=float(sell_order[2])
##        print(sell_price,buy_price)
        matched_order=[]
        profit=round((sell_price-buy_price)*min(buy_amt,sell_amt),2)
        total_profit+=profit
        profit="{:.2f}".format(profit)
        if(buy_time<sell_time):
            matched_order=[buy_time,sell_time,symbol,min(buy_amt,sell_amt),profit,'B','S',buy_price,sell_price]
        else:
            matched_order=[sell_time,buy_time,symbol,min(buy_amt,sell_amt),profit,'S','B',sell_price,buy_price]
        if buy_amt<sell_amt:
            sell_amt-=buy_amt
            sell_order[1]=sell_amt
            heapq.heappush(inventory[symbol]['sell'],sell_order)
        elif sell_amt<buy_amt:
            buy_amt-=sell_amt
            buy_order[1]=buy_amt
            heapq.heappush(inventory[symbol]['buy'],buy_order)
##        print(symbol, buy_order, sell_order)
##        print(matched_order)
        for i in range(len(matched_order)-1):
            print(str(matched_order[i])+",",end="")
        print(matched_order[-1])
total_profit="{:.2f}".format(total_profit)
print(total_profit)        
    
    
        
    
