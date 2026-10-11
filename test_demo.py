import unittest
from state import LaunchState as S, LaunchStateMachine
class Tests(unittest.TestCase):
 def test_forbidden_shortcut(self):
  with self.assertRaises(ValueError): LaunchStateMachine().transition(S.CONFIRMED)
 def test_success(self):
  m=LaunchStateMachine()
  for s in [S.READING_SOURCE,S.PLAN_READY,S.SENDING,S.VALIDATING,S.CONFIRMED]: m.transition(s)
  self.assertEqual(m.state,S.CONFIRMED); self.assertEqual(len(m.history),5)
 def test_recovery(self):
  m=LaunchStateMachine()
  for s in [S.READING_SOURCE,S.FAILED,S.RECOVERY,S.SENDING,S.VALIDATING,S.INCONCLUSIVE]: m.transition(s)
  self.assertEqual(m.state,S.INCONCLUSIVE)
 def test_repeated_state(self):
  m=LaunchStateMachine();m.transition(S.IDLE,'novo');self.assertEqual(m.history,[])
 def test_force_is_explicit(self):
  m=LaunchStateMachine();m.force(S.CONFIRMED);self.assertTrue(m.history[-1]['forced'])
if __name__=='__main__': unittest.main()
