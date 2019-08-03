import re


class DateBuilder:

    def __init__(self, filename):
        self.dates = {}
    
    def start_build(self, date_name, date_text):
        date = Date()
        date.main_text = date_text
        self.dates[date_name] = date
        self.extract_choices(date)
    
    def extract_choices(self, date):
        text = date.main_text
        exp = re.compile(r'\[.*?\]')
        choices_text = re.findall(exp, text)
        for text in choices_text:
            date.add_choice(Choice(text))
    
    def get_date(self, date_name):
        return self.dates[date_name]


class Date:

    def __init__(self):
        self.main_text = None
        self.choices = []
    
    def add_choice(self, choice):
        self.choices.append(choice)


class Choice:

    def __init__(self, text):
        self.build_choice(text)
    
    def build_choice(self, text):
        pass
