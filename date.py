class DateBuilder:

    def __init__(self, filename):
        self.current_date = None
        self.dates = {}
    
    def start_build(self, date_name):
        self.current_date = Date()
        self.dates[date_name] = self.current_date
    
    def add_text(self, text):
        self.current_date.main_text += text
    
    def add_choice(self, choice):
        self.current_date.choices.append(choice)

    def get_date(self, date_name):
        return self.dates[date_name]


class Date:

    def __init__(self):
        self.main_text = ""
        self.choices = []


class Choice:

    def __init__(self):
        self.prompts = None
        self.options = {}
        self.outcomes = {}
    
    def add_prompt(self, prompt):
        self.prompt = prompt
    
    def add_option(self, name, text):
        self.options[name] = text
    
    def add_outcome(self, option_name, text):
        self.outcomes[option_name] = text
    
    def get_outcome(self, option_name):
        return self.outcomes[option_name]
