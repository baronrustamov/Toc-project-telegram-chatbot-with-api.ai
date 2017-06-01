from transitions.extensions import GraphMachine

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        ##print("check1")
        return text == 'find_album_from_state0'

    def is_going_to_state2(self, update):
        text = update.message.text
        #print("check2")
        return text == 'show_recommendation_from_state0'

    def is_going_to_state3(self, update):
        text = update.message.text    
        return text == 'top_track_from_state0'
    
    def is_going_to_state4(self, update):
        text = update.message.text
        #print ("check 4 ")
        return text == 'find_album_by_enter_singer'     

    def is_going_to_state5(self, update):
        text = update.message.text
        #print ("check 5 ")
        return text == 'list_song_by_album_name'  
    
    def is_going_to_state6(self, update):
        text = update.message.text
        #print ("check 6 ")
        return text == 'play_music'    

    def is_going_to_state7(self, update):
        text = update.message.text
        #print ("check 7 ")
        return text == 'recommend_by_singer'

    def is_going_to_state8(self, update):
        text = update.message.text
        #print ("check 8 ")
        return text == 'play_music'

    def is_going_to_state9(self, update):
        text = update.message.text
        #print ("check 9 ")
        return text == 'find_album_by_enter_singer'                      

    def is_going_to_state10(self, update):
        text = update.message.text
        #print ("check 10 ")
        return text == 'play_music'    
   
    def on_enter_state1(self,update):
        print("enter state 1")
        update.message.reply_text("(I'm entering state1)\nPlease enter the singer\n I will list all the album by this artist")
        #self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("(I'm entering state2)\nPlease enter your favorite singer\nI will recommend some similiar song for you\nThe input format need to be 'recommended by singer' ")
        #self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("(I'm entering state3)\nPlease enter the singer\n I will show his(her) top 10 tracks. ")
        #self.go_back(update)

    def on_exit_state3(self, update):
        print('Leaving state3')     

    def on_enter_state4(self, update):
        update.message.reply_text("(I'm entering state4)\nPlease enter the album you want .I will list all the song in the album for u")
        #self.go_back(update)

    def on_exit_state4(self, update):
        print('Leaving state4')

    def on_enter_state5(self, update):
        update.message.reply_text("(I'm entering state5)\nI'll list all the song in the album!!")
        #self.go_back(update)

    def on_exit_state5(self, update):
        print('Leaving state5')

    def on_enter_state6(self, update):
        update.message.reply_text("(I'm entering state6)\nI'll open the spotify app for you")
        #self.go_back(update)

    def on_exit_state6(self, update):
        #self.go_back(update)
        print('Leaving state6')     

    def on_enter_state7(self, update):
        update.message.reply_text("(I'm entering state7)\n")
        #self.go_back(update)

    def on_exit_state7(self, update):
        print('Leaving state7')    

    def on_enter_state8(self, update):
        update.message.reply_text("(I'm entering state8)\nI'll open the spotify app for you")
        #self.go_back(update)

    def on_exit_state8(self, update):
        print('Leaving state8')
    
    def on_enter_state9(self, update):
        update.message.reply_text("(I'm entering state9)\n")
        #self.go_back(update)

    def on_exit_state9(self, update):
        print('Leaving state9')    
    
    def on_enter_state10(self, update):
        update.message.reply_text("(I'm entering state10)\nI'll open the spotify app for you")
        #self.go_back(update)

    def on_exit_state10(self, update):
        print('Leaving state10')                
    