# Toc-Project2017
Final project

A telegram bot based on a finite state machine

## Setup

### Prerequisite
* Python 3
* spotipy 
* api.ai
### Webhook URL
這次作業我沒有使用助教給的ngrok，因為實驗室剛好需要買一個實體Domain來做chatbot的接口,
故我直接使用實驗是的Domain name, 來當作Webhook的URL
#### Run the server
```sh
python demo.py
```
## Finite State Machine
![fsm](./img/show-fsm.png)

##Usage 
初始State都是在'user'
這次作業我設計了三個功能, 選擇第一項會進入State1 , 第二項會進入到State2, 第三項會進入到State3

1.透過歌手查詢專輯, 輸入歌手會進入State4, Bot會顯示這位歌手歷年專輯，在輸入想要聆聽的專輯進入state5, Bot會顯示這張專輯裡的每一首歌並且詢問使用者是否要聆聽這張專輯, 目前預設是使用者都會打 "yes"

2.透過喜愛的歌手推薦相關歌曲, 輸入歌手會進到State7, Bot 則會顯示相關歌曲並且詢問是否要聆聽這份list, 目前預設是使用者都會打 "yes"

3.透過歌手查詢該歌手Top 10 tracks, 輸入歌手會進到State9,Bot會顯示出Tracks並且詢問是否要聆聽這份list, 目前預設是使用者都會打 "yes" 


##System description 
(./img/system.png)




