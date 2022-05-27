# Jenkins cron syntax
class Environment:
    def __init__(self, pairs) -> None:
        self.pairs = pairs


class Options:
    def __init__(self) -> None:
        pass


class Parameters:
    def __init__(self, seq) -> None:
        self.seq = seq

        pass


class Triggers:
    def __init__(self) -> None:
        pass


class Stage:
    # The stage directive goes in the stages section and should contain a steps section, an optional agent section, or other stage-specific directives. Practically speaking, all of the real work done by a Pipeline will be wrapped in one or more stage directives.
    def __init__(self, name, sections, cond=None, agent=None) -> None:
        self.name = name
        self.sections = sections
        self.cond = cond
        self.agent = agent
        pass


class Tools:
    def __init__(self) -> None:
        pass


class Input:
    def __init__(self) -> None:
        pass


class When:
    def __init__(self) -> None:
        pass
