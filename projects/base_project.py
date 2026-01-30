
class BaseProject:
    name = "base"
    def run(self, driver, profile):
        raise NotImplementedError
