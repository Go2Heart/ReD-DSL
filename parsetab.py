
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'scriptCASE DEFAULT ENDSTATE ENDSWITCH ENDTIMEOUT ENDVARIABLE EXIT GOTO ID INTEGER REAL SCRIPT SPEAK STATE STR SWITCH TEXT TIMEOUT VAR VARIABLE\n        script : SCRIPT ID variables states\n        \n        variables : VARIABLE vars ENDVARIABLE\n        \n        vars : var\n                | vars var\n        \n        var : ID REAL VAR\n                | ID INTEGER VAR\n                | ID TEXT STR\n        \n        states : state\n                | states state\n        \n        state : STATE ID expressions ENDSTATE\n        \n        expressions : expression\n                    | expressions expression\n        \n        expression : switch\n                    | speak\n                    | goto\n                    | timeout\n                    | exit\n        \n        switch : SWITCH cases default\n        \n        cases : case\n                | cases case\n        \n        case : CASE STR expressions \n        \n        speak : SPEAK terms\n        \n        terms : term\n                | terms term\n        \n        term : STR\n        \n        term : VAR\n        \n        term : ID\n        \n        goto : GOTO ID\n        \n        timeout : TIMEOUT VAR expressions ENDTIMEOUT\n        \n        default : DEFAULT expressions ENDSWITCH\n        \n        exit : EXIT\n        '
    
_lr_action_items = {'SCRIPT':([0,],[2,]),'$end':([1,6,7,12,34,],[0,-1,-8,-9,-10,]),'ID':([2,5,8,9,10,15,27,28,31,32,33,39,40,41,42,43,50,],[3,11,13,11,-3,-4,43,44,-5,-6,-7,43,-23,-25,-26,-27,-24,]),'VARIABLE':([3,],[5,]),'STATE':([4,6,7,12,14,34,],[8,8,-8,-9,-2,-10,]),'ENDVARIABLE':([9,10,15,31,32,33,],[14,-3,-4,-5,-6,-7,]),'REAL':([11,],[16,]),'INTEGER':([11,],[17,]),'TEXT':([11,],[18,]),'SWITCH':([13,19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,],[26,26,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,26,-18,26,26,-24,26,26,26,-29,-30,]),'SPEAK':([13,19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,],[27,27,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,27,-18,27,27,-24,27,27,27,-29,-30,]),'GOTO':([13,19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,],[28,28,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,28,-18,28,28,-24,28,28,28,-29,-30,]),'TIMEOUT':([13,19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,],[29,29,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,29,-18,29,29,-24,29,29,29,-29,-30,]),'EXIT':([13,19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,],[30,30,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,30,-18,30,30,-24,30,30,30,-29,-30,]),'VAR':([16,17,27,29,39,40,41,42,43,50,],[31,32,42,45,42,-23,-25,-26,-27,-24,]),'STR':([18,27,38,39,40,41,42,43,50,],[33,41,49,41,-23,-25,-26,-27,-24,]),'ENDSTATE':([19,20,21,22,23,24,25,30,35,39,40,41,42,43,44,46,50,54,55,],[34,-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,-18,-24,-29,-30,]),'ENDTIMEOUT':([20,21,22,23,24,25,30,35,39,40,41,42,43,44,46,50,51,54,55,],[-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,-18,-24,54,-29,-30,]),'ENDSWITCH':([20,21,22,23,24,25,30,35,39,40,41,42,43,44,46,50,52,54,55,],[-11,-13,-14,-15,-16,-17,-31,-12,-22,-23,-25,-26,-27,-28,-18,-24,55,-29,-30,]),'DEFAULT':([20,21,22,23,24,25,30,35,36,37,39,40,41,42,43,44,46,47,50,53,54,55,],[-11,-13,-14,-15,-16,-17,-31,-12,48,-19,-22,-23,-25,-26,-27,-28,-18,-20,-24,-21,-29,-30,]),'CASE':([20,21,22,23,24,25,26,30,35,36,37,39,40,41,42,43,44,46,47,50,53,54,55,],[-11,-13,-14,-15,-16,-17,38,-31,-12,38,-19,-22,-23,-25,-26,-27,-28,-18,-20,-24,-21,-29,-30,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'script':([0,],[1,]),'variables':([3,],[4,]),'states':([4,],[6,]),'state':([4,6,],[7,12,]),'vars':([5,],[9,]),'var':([5,9,],[10,15,]),'expressions':([13,45,48,49,],[19,51,52,53,]),'expression':([13,19,45,48,49,51,52,53,],[20,35,20,20,20,35,35,35,]),'switch':([13,19,45,48,49,51,52,53,],[21,21,21,21,21,21,21,21,]),'speak':([13,19,45,48,49,51,52,53,],[22,22,22,22,22,22,22,22,]),'goto':([13,19,45,48,49,51,52,53,],[23,23,23,23,23,23,23,23,]),'timeout':([13,19,45,48,49,51,52,53,],[24,24,24,24,24,24,24,24,]),'exit':([13,19,45,48,49,51,52,53,],[25,25,25,25,25,25,25,25,]),'cases':([26,],[36,]),'case':([26,36,],[37,47,]),'terms':([27,],[39,]),'term':([27,39,],[40,50,]),'default':([36,],[46,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> script","S'",1,None,None,None),
  ('script -> SCRIPT ID variables states','script',4,'p_script','parser.py',46),
  ('variables -> VARIABLE vars ENDVARIABLE','variables',3,'p_variables','parser.py',54),
  ('vars -> var','vars',1,'p_vars','parser.py',61),
  ('vars -> vars var','vars',2,'p_vars','parser.py',62),
  ('var -> ID REAL VAR','var',3,'p_var','parser.py',73),
  ('var -> ID INTEGER VAR','var',3,'p_var','parser.py',74),
  ('var -> ID TEXT STR','var',3,'p_var','parser.py',75),
  ('states -> state','states',1,'p_states','parser.py',81),
  ('states -> states state','states',2,'p_states','parser.py',82),
  ('state -> STATE ID expressions ENDSTATE','state',4,'p_state','parser.py',93),
  ('expressions -> expression','expressions',1,'p_expressions','parser.py',99),
  ('expressions -> expressions expression','expressions',2,'p_expressions','parser.py',100),
  ('expression -> switch','expression',1,'p_expression','parser.py',112),
  ('expression -> speak','expression',1,'p_expression','parser.py',113),
  ('expression -> goto','expression',1,'p_expression','parser.py',114),
  ('expression -> timeout','expression',1,'p_expression','parser.py',115),
  ('expression -> exit','expression',1,'p_expression','parser.py',116),
  ('switch -> SWITCH cases default','switch',3,'p_switch','parser.py',122),
  ('cases -> case','cases',1,'p_cases','parser.py',127),
  ('cases -> cases case','cases',2,'p_cases','parser.py',128),
  ('case -> CASE STR expressions','case',3,'p_case','parser.py',137),
  ('speak -> SPEAK terms','speak',2,'p_speak','parser.py',143),
  ('terms -> term','terms',1,'p_terms','parser.py',149),
  ('terms -> terms term','terms',2,'p_terms','parser.py',150),
  ('term -> STR','term',1,'p_term_str','parser.py',160),
  ('term -> VAR','term',1,'p_term_var','parser.py',166),
  ('term -> ID','term',1,'p_term_id','parser.py',172),
  ('goto -> GOTO ID','goto',2,'p_goto','parser.py',178),
  ('timeout -> TIMEOUT VAR expressions ENDTIMEOUT','timeout',4,'p_timeout','parser.py',190),
  ('default -> DEFAULT expressions ENDSWITCH','default',3,'p_default','parser.py',196),
  ('exit -> EXIT','exit',1,'p_exit','parser.py',202),
]
