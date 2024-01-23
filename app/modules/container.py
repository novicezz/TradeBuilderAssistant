class Container:
    def __init__(self, type, info: str):
        self.element = None
        self.type = type
        self.info = info

    def __str__(self):
        return str(self.element)
    
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
    
    def reset_element(self):
        self.element = None

    def set_element(self, element) -> bool:
        try:
            self.element = self.type(element)
        except:
            return False
        return True