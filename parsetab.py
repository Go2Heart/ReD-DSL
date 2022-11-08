
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'scriptCASE DEFAULT EXIT GOTO ID INTEGER REAL SCRIPT SPEAK STATE STR TEXT TIMEOUT VAR VARIABLE\n        script : SCRIPT ID variables states\n        \n        variables : VARIABLE vars\n        \n        vars : var\n                | vars var\n        \n        var : ID REAL VAR\n                | ID INTEGER VAR\n                | ID TEXT STR\n        \n        states : state\n                | states state\n        \n        state : STATE ID expressions\n        \n        expressions : expression\n                    | expressions expression\n        \n        expression : cases\n                    | speak\n                    | goto\n                    | timeout\n                    | default\n                    | exit\n        \n        cases : case\n                | cases case\n        \n        case : CASE STR expressions \n        \n        speak : SPEAK terms\n        \n        terms : term\n                | terms term\n        \n        term : STR\n                | VAR\n        \n        goto : GOTO ID\n        \n        timeout : TIMEOUT VAR expressions\n        \n        default : DEFAULT expressions\n        \n        exit : EXIT\n        '
    
_lr_action_items = {'SCRIPT':([0,],[2,]),'$end':([1,6,7,12,18,19,20,21,22,23,24,25,26,31,36,37,38,39,40,41,42,44,46,47,48,],[0,-1,-8,-9,-10,-11,-13,-14,-15,-16,-17,-18,-19,-30,-12,-20,-22,-23,-25,-26,-27,-29,-24,-28,-21,]),'ID':([2,5,8,9,10,14,28,33,34,35,],[3,11,13,11,-3,-4,42,-5,-6,-7,]),'VARIABLE':([3,],[5,]),'STATE':([4,6,7,9,10,12,14,18,19,20,21,22,23,24,25,26,31,33,34,35,36,37,38,39,40,41,42,44,46,47,48,],[8,8,-8,-2,-3,-9,-4,-10,-11,-13,-14,-15,-16,-17,-18,-19,-30,-5,-6,-7,-12,-20,-22,-23,-25,-26,-27,-29,-24,-28,-21,]),'REAL':([11,],[15,]),'INTEGER':([11,],[16,]),'TEXT':([11,],[17,]),'SPEAK':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[27,27,-11,-13,-14,-15,-16,-17,-18,-19,27,-30,-12,-20,-22,-23,-25,-26,-27,27,27,27,-24,27,27,]),'GOTO':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[28,28,-11,-13,-14,-15,-16,-17,-18,-19,28,-30,-12,-20,-22,-23,-25,-26,-27,28,28,28,-24,28,28,]),'TIMEOUT':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[29,29,-11,-13,-14,-15,-16,-17,-18,-19,29,-30,-12,-20,-22,-23,-25,-26,-27,29,29,29,-24,29,29,]),'DEFAULT':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[30,30,-11,-13,-14,-15,-16,-17,-18,-19,30,-30,-12,-20,-22,-23,-25,-26,-27,30,30,30,-24,30,30,]),'EXIT':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[31,31,-11,-13,-14,-15,-16,-17,-18,-19,31,-30,-12,-20,-22,-23,-25,-26,-27,31,31,31,-24,31,31,]),'CASE':([13,18,19,20,21,22,23,24,25,26,30,31,36,37,38,39,40,41,42,43,44,45,46,47,48,],[32,32,-11,32,-14,-15,-16,-17,-18,-19,32,-30,-12,-20,-22,-23,-25,-26,-27,32,32,32,-24,32,32,]),'VAR':([15,16,27,29,38,39,40,41,46,],[33,34,41,43,41,-23,-25,-26,-24,]),'STR':([17,27,32,38,39,40,41,46,],[35,40,45,40,-23,-25,-26,-24,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'script':([0,],[1,]),'variables':([3,],[4,]),'states':([4,],[6,]),'state':([4,6,],[7,12,]),'vars':([5,],[9,]),'var':([5,9,],[10,14,]),'expressions':([13,30,43,45,],[18,44,47,48,]),'expression':([13,18,30,43,44,45,47,48,],[19,36,19,19,36,19,36,36,]),'cases':([13,18,30,43,44,45,47,48,],[20,20,20,20,20,20,20,20,]),'speak':([13,18,30,43,44,45,47,48,],[21,21,21,21,21,21,21,21,]),'goto':([13,18,30,43,44,45,47,48,],[22,22,22,22,22,22,22,22,]),'timeout':([13,18,30,43,44,45,47,48,],[23,23,23,23,23,23,23,23,]),'default':([13,18,30,43,44,45,47,48,],[24,24,24,24,24,24,24,24,]),'exit':([13,18,30,43,44,45,47,48,],[25,25,25,25,25,25,25,25,]),'case':([13,18,20,30,43,44,45,47,48,],[26,26,37,26,26,26,26,26,26,]),'terms':([27,],[38,]),'term':([27,38,],[39,46,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> script","S'",1,None,None,None),
  ('script -> SCRIPT ID variables states','script',4,'p_script','parser.py',37),
  ('variables -> VARIABLE vars','variables',2,'p_variables','parser.py',43),
  ('vars -> var','vars',1,'p_vars','parser.py',48),
  ('vars -> vars var','vars',2,'p_vars','parser.py',49),
  ('var -> ID REAL VAR','var',3,'p_var','parser.py',58),
  ('var -> ID INTEGER VAR','var',3,'p_var','parser.py',59),
  ('var -> ID TEXT STR','var',3,'p_var','parser.py',60),
  ('states -> state','states',1,'p_states','parser.py',66),
  ('states -> states state','states',2,'p_states','parser.py',67),
  ('state -> STATE ID expressions','state',3,'p_state','parser.py',76),
  ('expressions -> expression','expressions',1,'p_expressions','parser.py',82),
  ('expressions -> expressions expression','expressions',2,'p_expressions','parser.py',83),
  ('expression -> cases','expression',1,'p_expression','parser.py',92),
  ('expression -> speak','expression',1,'p_expression','parser.py',93),
  ('expression -> goto','expression',1,'p_expression','parser.py',94),
  ('expression -> timeout','expression',1,'p_expression','parser.py',95),
  ('expression -> default','expression',1,'p_expression','parser.py',96),
  ('expression -> exit','expression',1,'p_expression','parser.py',97),
  ('cases -> case','cases',1,'p_cases','parser.py',103),
  ('cases -> cases case','cases',2,'p_cases','parser.py',104),
  ('case -> CASE STR expressions','case',3,'p_case','parser.py',113),
  ('speak -> SPEAK terms','speak',2,'p_speak','parser.py',119),
  ('terms -> term','terms',1,'p_terms','parser.py',125),
  ('terms -> terms term','terms',2,'p_terms','parser.py',126),
  ('term -> STR','term',1,'p_term','parser.py',135),
  ('term -> VAR','term',1,'p_term','parser.py',136),
  ('goto -> GOTO ID','goto',2,'p_goto','parser.py',144),
  ('timeout -> TIMEOUT VAR expressions','timeout',3,'p_timeout','parser.py',150),
  ('default -> DEFAULT expressions','default',2,'p_default','parser.py',156),
  ('exit -> EXIT','exit',1,'p_exit','parser.py',162),
]
