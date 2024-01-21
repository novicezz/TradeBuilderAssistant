class Object:
    def __init__(self, type, info: str):
        self.element = None
        self.type = type
        self.info = info
    
    def is_set(self):
        if self.element == None:
            return False
        return True

    def get_type(self):
        return self.type

    def get_element(self):
        return self.element
    
    def get_info(self):
        return self.info

    def set_element(self, element):
        try:
            self.type(element)
        except:
            return False
        self.element = self.type(element)
        return True