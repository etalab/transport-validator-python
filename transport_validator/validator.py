from transitfeed import SimpleProblemAccumulator

class Accumulator(SimpleProblemAccumulator):
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.notices = []

    def _Report(self, e):
        SimpleProblemAccumulator._Report(self, e)
        if e.IsError():
            self.errors.append(e)
        if e.IsWarning():
            self.warnings.append(e)
        if e.IsNotice():
            self.notices.append(e)

    def __dict__(self):
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "notices": self.notices
        }
