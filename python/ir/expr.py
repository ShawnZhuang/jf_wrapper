class TimeUnit:
    SEC = "SECONDS"

class Credentials:
    def __init__(self,credentials_id) -> None:
        pass

class Cron:
    def __init__(self) -> None:
        # MINUTE	HOUR	DOM	MONTH	DOW
        pass
class Condition:
    class CondType:
        # Run the steps in the post section regardless of the completion status of the Pipeline’s or stage’s run.
        always = 0
        # Only run the steps in post if the current Pipeline’s or stage’s run has a different completion status from its previous run.
        changed = 1
        # Only run the steps in post if the current Pipeline’s or stage’s run is successful and the previous run failed or was unstable.
        fixed = 2
        # Only run the steps in post if the current Pipeline’s or stage’s run’s status is failure, unstable, or aborted and the previous run was successful.
        regression = 3
        aborted = 4  # Only run the steps in post if the current Pipeline’s or stage’s run has an "aborted" status, usually due to the Pipeline being manually aborted. This is typically denoted by gray in the web UI.
        # Only run the steps in post if the current Pipeline’s or stage’s run has a "failed" status, typically denoted by red in the web UI.
        failure = 5
        # Only run the steps in post if the current Pipeline’s or stage’s run has a "success" status, typically denoted by blue or green in the web UI.
        success = 6
        unstable = 7  # Only run the steps in post if the current Pipeline’s or stage’s run has an "unstable" status, usually caused by test failures, code violations, etc. This is typically denoted by yellow in the web UI.
        # Only run the steps in post if the current Pipeline’s or stage’s run has not a "success" status. This is typically denoted in the web UI depending on the status previously mentioned.
        unsuccessful = 8
        # Run the steps in this post condition after every other post condition has been evaluated, regardless of the Pipeline or stage’s status.
        cleanup = 9

    def __init__(self, cond, seq) -> None:
        pass

class Sleep:
    def __init__(self, num) -> None:
        self.num = num

class Echo:
    def __init__(self, info) -> None:
        self.info = info


class TimeOut:
    def __init__(self, unit, time, seq) -> None:
        # timeout(unit: 'SECONDS', time: 5) {}
        pass

class Bash:
    def __init__(self, cmd) -> None:
        self.cmd = cmd
    # @property
    # def cmd(self):
    #     return self._cmd

