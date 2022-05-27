

class Agent:
    class AgentType:
        ANY = "any"
        NONE = "none"
        LABEL = "label"
        NODE = "node"
        DOCKER = "docker"
        DOCKER_FILE = "dockerfile"

    def __init__(self, agent_type: AgentType, value=None) -> None:
        # value is not valid for type any/none
        self.agent_type = agent_type
        self.value = value


class Post:

    def __init__(self,  stages=None, post=None, agent=None) -> None:
        # The post section defines one or more additional steps that are run upon the completion of a Pipeline’s or stage’s run (depending on the location of the post section within the Pipeline). post can support any of the following post-condition blocks: always, changed, fixed, regression, aborted, failure, success, unstable, unsuccessful, and cleanup. These condition blocks allow the execution of steps inside each condition depending on the completion status of the Pipeline or stage. The condition blocks are executed in the order shown below.
        # self.seq = seq
        pass


class Stages:
    def __init__(self,  directives,   agent=None) -> None:
        #  a stage must have one and only one of steps, stages, parallel, or matrix.
        # self.name = name
        self.agent = agent
        self.directives = directives


class Steps:
    def __init__(self, seq) -> None:
        if isinstance(seq , list):
            self.seq = seq
        else:
            self.seq = [seq]
        pass


class Pipeline:
    def __init__(self, agent, seq) -> None:

        self.seq = seq
        self.agent = agent
# class Parallel:
# class Matrix
