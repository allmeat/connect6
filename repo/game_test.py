import unittest


class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTest, self).__init__(*args, **kwargs)
        self.engine = "mysql+pymysql://root:allmeat@35.233.179.226:3306/playground_log"

