import time


class Timers:

    def __init__(self):
        self.waifu_claim_timer = None
    
    def set_waifu_claim_timer(self):
        self.waifu_claim_timer = time.time()
    
    def get_waifu_claim_timer(self):
        return self.waifu_claim_timer
    
    def get_time(self):
        return time.time()


timers = Timers()
