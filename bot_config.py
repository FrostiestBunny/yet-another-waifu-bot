class BotConfig:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.config = {}
        self.config_props = ['spawn_channel_id', 'spawn_rate']

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.load_config()
    
    def load_config(self):
        columns = ', '.join(self.config_props)
        self.cur.execute("SELECT %s FROM bot_config;", (columns,))
        query = self.cur.fetchone()
        if query is None:
            return
        for i, c in enumerate(query):
            self.config[self.config_props[i]] = c
    
    def update_config(self, prop, value):
        if self.config.get(prop, None) is not None:
            self.alter_config(prop, value)
            return
        self.config[prop] = value
        self.cur.execute("INSERT INTO bot_config (%s) VALUES (%s)",
                         (prop, value))
        self.save()

    def alter_config(self, prop, value):
        self.cur.execute("UPDATE bot_config SET %s = %s WHERE %s=%s",
                         (prop, value, prop, self.config[prop]))
        self.save()
        self.config[prop] = value

    def save(self):
        self.conn.commit()


bot_config = BotConfig()
