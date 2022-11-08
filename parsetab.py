
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'scriptCASE DEFAULT EXIT GOTO ID INTEGER REAL SCRIPT SPEAK STATE STR SWITCH TEXT TIMEOUT VAR VARIABLE\n        script : SCRIPT ID variables states\n        \n        variables : VARIABLE vars\n        \n        vars : var\n                | vars var\n        \n        var : ID REAL VAR\n                | ID INTEGER VAR\n                | ID TEXT STR\n        \n        states : state\n                | states state\n        \n        state : STATE ID expressions\n        \n        expressions : expression\n                    | expressions expression\n        \n        expression : switch\n                    | speak\n                    | goto\n                    | timeout\n                    | default\n                    | exit\n        \n        switch : SWITCH cases\n        \n        cases : case\n                | cases case\n        \n        case : CASE STR expressions \n        \n        speak : SPEAK terms\n        \n        terms : term\n                | terms term\n        \n        term : STR\n                | VAR\n        \n        goto : GOTO ID\n        \n        timeout : TIMEOUT VAR expressions\n        \n        default : DEFAULT expressions\n        \n        exit : EXIT\n        '
    
_lr_action_items = {'SCRIPT':([0,],[2,]),'$end':([1,6,7,12,18,19,20,21,22,23,24,25,31,35,36,37,39,40,41,42,43,45,46,48,49,50,],[0,-1,-8,-9,-10,-11,-13,-14,-15,-16,-17,-18,-31,-12,-19,-20,-23,-24,-26,-27,-28,-30,-21,-25,-29,-22,]),'ID':([2,5,8,9,10,14,28,32,33,34,],[3,11,13,11,-3,-4,43,-5,-6,-7,]),'VARIABLE':([3,],[5,]),'STATE':([4,6,7,9,10,12,14,18,19,20,21,22,23,24,25,31,32,33,34,35,36,37,39,40,41,42,43,45,46,48,49,50,],[8,8,-8,-2,-3,-9,-4,-10,-11,-13,-14,-15,-16,-17,-18,-31,-5,-6,-7,-12,-19,-20,-23,-24,-26,-27,-28,-30,-21,-25,-29,-22,]),'REAL':([11,],[15,]),'INTEGER':([11,],[16,]),'TEXT':([11,],[17,]),'SWITCH':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[26,26,-11,-13,-14,-15,-16,-17,-18,26,-31,-12,-19,-20,-23,-24,-26,-27,-28,26,26,-21,26,-25,26,26,]),'SPEAK':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[27,27,-11,-13,-14,-15,-16,-17,-18,27,-31,-12,-19,-20,-23,-24,-26,-27,-28,27,27,-21,27,-25,27,27,]),'GOTO':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[28,28,-11,-13,-14,-15,-16,-17,-18,28,-31,-12,-19,-20,-23,-24,-26,-27,-28,28,28,-21,28,-25,28,28,]),'TIMEOUT':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[29,29,-11,-13,-14,-15,-16,-17,-18,29,-31,-12,-19,-20,-23,-24,-26,-27,-28,29,29,-21,29,-25,29,29,]),'DEFAULT':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[30,30,-11,-13,-14,-15,-16,-17,-18,30,-31,-12,-19,-20,-23,-24,-26,-27,-28,30,30,-21,30,-25,30,30,]),'EXIT':([13,18,19,20,21,22,23,24,25,30,31,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,],[31,31,-11,-13,-14,-15,-16,-17,-18,31,-31,-12,-19,-20,-23,-24,-26,-27,-28,31,31,-21,31,-25,31,31,]),'VAR':([15,16,27,29,39,40,41,42,48,],[32,33,42,44,42,-24,-26,-27,-25,]),'STR':([17,27,38,39,40,41,42,48,],[34,41,47,41,-24,-26,-27,-25,]),'CASE':([19,20,21,22,23,24,25,26,31,35,36,37,39,40,41,42,43,45,46,48,49,50,],[-11,-13,-14,-15,-16,-17,-18,38,-31,-12,38,-20,-23,-24,-26,-27,-28,-30,-21,-25,-29,-22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'script':([0,],[1,]),'variables':([3,],[4,]),'states':([4,],[6,]),'state':([4,6,],[7,12,]),'vars':([5,],[9,]),'var':([5,9,],[10,14,]),'expressions':([13,30,44,47,],[18,45,49,50,]),'expression':([13,18,30,44,45,47,49,50,],[19,35,19,19,35,19,35,35,]),'switch':([13,18,30,44,45,47,49,50,],[20,20,20,20,20,20,20,20,]),'speak':([13,18,30,44,45,47,49,50,],[21,21,21,21,21,21,21,21,]),'goto':([13,18,30,44,45,47,49,50,],[22,22,22,22,22,22,22,22,]),'timeout':([13,18,30,44,45,47,49,50,],[23,23,23,23,23,23,23,23,]),'default':([13,18,30,44,45,47,49,50,],[24,24,24,24,24,24,24,24,]),'exit':([13,18,30,44,45,47,49,50,],[25,25,25,25,25,25,25,25,]),'cases':([26,],[36,]),'case':([26,36,],[37,46,]),'terms':([27,],[39,]),'term':([27,39,],[40,48,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> script","S'",1,None,None,None),
  ('script -> SCRIPT ID variables states','script',4,'p_script','parser.py',43),
  ('variables -> VARIABLE vars','variables',2,'p_variables','parser.py',49),
  ('vars -> var','vars',1,'p_vars','parser.py',54),
  ('vars -> vars var','vars',2,'p_vars','parser.py',55),
  ('var -> ID REAL VAR','var',3,'p_var','parser.py',64),
  ('var -> ID INTEGER VAR','var',3,'p_var','parser.py',65),
  ('var -> ID TEXT STR','var',3,'p_var','parser.py',66),
  ('states -> state','states',1,'p_states','parser.py',72),
  ('states -> states state','states',2,'p_states','parser.py',73),
  ('state -> STATE ID expressions','state',3,'p_state','parser.py',82),
  ('expressions -> expression','expressions',1,'p_expressions','parser.py',88),
  ('expressions -> expressions expression','expressions',2,'p_expressions','parser.py',89),
  ('expression -> switch','expression',1,'p_expression','parser.py',98),
  ('expression -> speak','expression',1,'p_expression','parser.py',99),
  ('expression -> goto','expression',1,'p_expression','parser.py',100),
  ('expression -> timeout','expression',1,'p_expression','parser.py',101),
  ('expression -> default','expression',1,'p_expression','parser.py',102),
  ('expression -> exit','expression',1,'p_expression','parser.py',103),
  ('switch -> SWITCH cases','switch',2,'p_switch','parser.py',109),
  ('cases -> case','cases',1,'p_cases','parser.py',114),
  ('cases -> cases case','cases',2,'p_cases','parser.py',115),
  ('case -> CASE STR expressions','case',3,'p_case','parser.py',124),
  ('speak -> SPEAK terms','speak',2,'p_speak','parser.py',130),
  ('terms -> term','terms',1,'p_terms','parser.py',136),
  ('terms -> terms term','terms',2,'p_terms','parser.py',137),
  ('term -> STR','term',1,'p_term','parser.py',146),
  ('term -> VAR','term',1,'p_term','parser.py',147),
  ('goto -> GOTO ID','goto',2,'p_goto','parser.py',155),
  ('timeout -> TIMEOUT VAR expressions','timeout',3,'p_timeout','parser.py',161),
  ('default -> DEFAULT expressions','default',2,'p_default','parser.py',167),
  ('exit -> EXIT','exit',1,'p_exit','parser.py',173),
]
