from state import LaunchState as S, LaunchStateMachine
import json
machine=LaunchStateMachine()
for stage in [S.READING_SOURCE,S.MAPPING,S.PLAN_READY,S.WAITING_CONFIRMATION,S.SENDING,S.VALIDATING,S.CONFIRMED]:
 machine.transition(stage, 'Simulação local, sem envio externo')
print(json.dumps(machine.snapshot(),ensure_ascii=False,indent=2))
