
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "scriptCASE DEFAULT ENDSTATE ENDSWITCH ENDTIMEOUT ENDVARIABLE EXIT GOTO GREATER_EQUAL ID INTEGER LESS_EQUAL MINUS PLUS REAL RETURN SCRIPT SPEAK STATE STR SWITCH TEXT TIMEOUT UPDATE VAR VARIABLE\n        script : SCRIPT ID variables states\n        \n        variables : VARIABLE vars ENDVARIABLE\n        \n        vars : var\n                | vars var\n        \n        var : ID REAL VAR\n                | ID INTEGER VAR\n                | ID TEXT STR\n        \n        states : state\n                | states state\n        \n        state : STATE ID expressions ENDSTATE\n        \n        expressions : expression\n                    | expressions expression\n        \n        expression : switch\n                    | speak\n                    | goto\n                    | timeout\n                    | exit\n                    | update\n        \n        update : UPDATE ID '=' terms\n        \n        switch : SWITCH cases default\n        \n        cases : case\n                | cases case\n        \n        case : CASE STR expressions \n                | CASE RETURN expressions\n                | CASE compare expressions\n        \n            compare : ID '>' term\n                    | ID '<' term\n                    | ID LESS_EQUAL term\n                    | ID GREATER_EQUAL term\n                    | RETURN '>' term\n                    | RETURN '<' term\n                    | RETURN LESS_EQUAL term\n                    | RETURN GREATER_EQUAL term\n        \n        speak : SPEAK terms\n        \n        terms : term\n                | terms '+' term\n                | term PLUS term\n                | term MINUS term\n        \n        term : STR\n        \n        term : VAR\n        \n        term : ID\n        \n        term : RETURN\n        \n        goto : GOTO ID\n        \n        timeout : TIMEOUT VAR expressions ENDTIMEOUT\n        \n        default : DEFAULT expressions ENDSWITCH\n                    | ENDSWITCH\n        \n        exit : EXIT\n        "
    
_lr_action_items = {'SCRIPT':([0,],[2,]),'$end':([1,6,7,12,36,],[0,-1,-8,-9,-10,]),'ID':([2,5,8,9,10,15,28,29,32,33,34,35,40,58,59,60,62,66,67,68,69,71,72,73,74,],[3,11,13,11,-3,-4,45,47,49,-5,-6,-7,57,45,45,45,45,45,45,45,45,45,45,45,45,]),'VARIABLE':([3,],[5,]),'STATE':([4,6,7,12,14,36,],[8,8,-8,-9,-2,-10,]),'ENDVARIABLE':([9,10,15,33,34,35,],[14,-3,-4,-5,-6,-7,]),'REAL':([11,],[16,]),'INTEGER':([11,],[17,]),'TEXT':([11,],[18,]),'SWITCH':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[27,27,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,27,-20,27,-46,27,27,27,27,27,27,27,27,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'SPEAK':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[28,28,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,28,-20,28,-46,28,28,28,28,28,28,28,28,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'GOTO':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[29,29,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,29,-20,29,-46,29,29,29,29,29,29,29,29,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'TIMEOUT':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[30,30,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,30,-20,30,-46,30,30,30,30,30,30,30,30,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'EXIT':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[31,31,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,31,-20,31,-46,31,31,31,31,31,31,31,31,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'UPDATE':([13,19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,48,50,52,53,54,55,56,61,63,64,65,70,75,76,77,78,79,80,81,82,83,84,85,86,87,88,],[32,32,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,32,-20,32,-46,32,32,32,32,32,32,32,32,-36,-37,-38,-44,-19,-45,-30,-31,-32,-33,-26,-27,-28,-29,]),'VAR':([16,17,28,30,58,59,60,62,66,67,68,69,71,72,73,74,],[33,34,44,48,44,44,44,44,44,44,44,44,44,44,44,44,]),'STR':([18,28,40,58,59,60,62,66,67,68,69,71,72,73,74,],[35,43,54,43,43,43,43,43,43,43,43,43,43,43,43,]),'ENDSTATE':([19,20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,50,53,75,76,77,78,79,80,],[36,-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,-20,-46,-36,-37,-38,-44,-19,-45,]),'ENDTIMEOUT':([20,21,22,23,24,25,26,31,37,41,42,43,44,45,46,47,50,53,61,75,76,77,78,79,80,],[-11,-13,-14,-15,-16,-17,-18,-47,-12,-34,-35,-39,-40,-41,-42,-43,-20,-46,78,-36,-37,-38,-44,-19,-45,]),'ENDSWITCH':([20,21,22,23,24,25,26,31,37,38,39,41,42,43,44,45,46,47,50,51,53,63,64,65,70,75,76,77,78,79,80,],[-11,-13,-14,-15,-16,-17,-18,-47,-12,53,-21,-34,-35,-39,-40,-41,-42,-43,-20,-22,-46,80,-23,-24,-25,-36,-37,-38,-44,-19,-45,]),'DEFAULT':([20,21,22,23,24,25,26,31,37,38,39,41,42,43,44,45,46,47,50,51,53,64,65,70,75,76,77,78,79,80,],[-11,-13,-14,-15,-16,-17,-18,-47,-12,52,-21,-34,-35,-39,-40,-41,-42,-43,-20,-22,-46,-23,-24,-25,-36,-37,-38,-44,-19,-45,]),'CASE':([20,21,22,23,24,25,26,27,31,37,38,39,41,42,43,44,45,46,47,50,51,53,64,65,70,75,76,77,78,79,80,],[-11,-13,-14,-15,-16,-17,-18,40,-47,-12,40,-21,-34,-35,-39,-40,-41,-42,-43,-20,-22,-46,-23,-24,-25,-36,-37,-38,-44,-19,-45,]),'RETURN':([28,40,58,59,60,62,66,67,68,69,71,72,73,74,],[46,55,46,46,46,46,46,46,46,46,46,46,46,46,]),'+':([41,42,43,44,45,46,75,76,77,79,],[58,-35,-39,-40,-41,-42,-36,-37,-38,58,]),'PLUS':([42,43,44,45,46,],[59,-39,-40,-41,-42,]),'MINUS':([42,43,44,45,46,],[60,-39,-40,-41,-42,]),'=':([49,],[62,]),'>':([55,57,],[66,71,]),'<':([55,57,],[67,72,]),'LESS_EQUAL':([55,57,],[68,73,]),'GREATER_EQUAL':([55,57,],[69,74,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'script':([0,],[1,]),'variables':([3,],[4,]),'states':([4,],[6,]),'state':([4,6,],[7,12,]),'vars':([5,],[9,]),'var':([5,9,],[10,15,]),'expressions':([13,48,52,54,55,56,],[19,61,63,64,65,70,]),'expression':([13,19,48,52,54,55,56,61,63,64,65,70,],[20,37,20,20,20,20,20,37,37,37,37,37,]),'switch':([13,19,48,52,54,55,56,61,63,64,65,70,],[21,21,21,21,21,21,21,21,21,21,21,21,]),'speak':([13,19,48,52,54,55,56,61,63,64,65,70,],[22,22,22,22,22,22,22,22,22,22,22,22,]),'goto':([13,19,48,52,54,55,56,61,63,64,65,70,],[23,23,23,23,23,23,23,23,23,23,23,23,]),'timeout':([13,19,48,52,54,55,56,61,63,64,65,70,],[24,24,24,24,24,24,24,24,24,24,24,24,]),'exit':([13,19,48,52,54,55,56,61,63,64,65,70,],[25,25,25,25,25,25,25,25,25,25,25,25,]),'update':([13,19,48,52,54,55,56,61,63,64,65,70,],[26,26,26,26,26,26,26,26,26,26,26,26,]),'cases':([27,],[38,]),'case':([27,38,],[39,51,]),'terms':([28,62,],[41,79,]),'term':([28,58,59,60,62,66,67,68,69,71,72,73,74,],[42,75,76,77,42,81,82,83,84,85,86,87,88,]),'default':([38,],[50,]),'compare':([40,],[56,]),}

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
  ('expression -> update','expression',1,'p_expression','parser.py',117),
  ('update -> UPDATE ID = terms','update',4,'p_update','parser.py',123),
  ('switch -> SWITCH cases default','switch',3,'p_switch','parser.py',129),
  ('cases -> case','cases',1,'p_cases','parser.py',134),
  ('cases -> cases case','cases',2,'p_cases','parser.py',135),
  ('case -> CASE STR expressions','case',3,'p_case','parser.py',144),
  ('case -> CASE RETURN expressions','case',3,'p_case','parser.py',145),
  ('case -> CASE compare expressions','case',3,'p_case','parser.py',146),
  ('compare -> ID > term','compare',3,'p_condition','parser.py',155),
  ('compare -> ID < term','compare',3,'p_condition','parser.py',156),
  ('compare -> ID LESS_EQUAL term','compare',3,'p_condition','parser.py',157),
  ('compare -> ID GREATER_EQUAL term','compare',3,'p_condition','parser.py',158),
  ('compare -> RETURN > term','compare',3,'p_condition','parser.py',159),
  ('compare -> RETURN < term','compare',3,'p_condition','parser.py',160),
  ('compare -> RETURN LESS_EQUAL term','compare',3,'p_condition','parser.py',161),
  ('compare -> RETURN GREATER_EQUAL term','compare',3,'p_condition','parser.py',162),
  ('speak -> SPEAK terms','speak',2,'p_speak','parser.py',168),
  ('terms -> term','terms',1,'p_terms','parser.py',174),
  ('terms -> terms + term','terms',3,'p_terms','parser.py',175),
  ('terms -> term PLUS term','terms',3,'p_terms','parser.py',176),
  ('terms -> term MINUS term','terms',3,'p_terms','parser.py',177),
  ('term -> STR','term',1,'p_term_str','parser.py',187),
  ('term -> VAR','term',1,'p_term_var','parser.py',193),
  ('term -> ID','term',1,'p_term_id','parser.py',199),
  ('term -> RETURN','term',1,'p_term_return','parser.py',205),
  ('goto -> GOTO ID','goto',2,'p_goto','parser.py',212),
  ('timeout -> TIMEOUT VAR expressions ENDTIMEOUT','timeout',4,'p_timeout','parser.py',219),
  ('default -> DEFAULT expressions ENDSWITCH','default',3,'p_default','parser.py',225),
  ('default -> ENDSWITCH','default',1,'p_default','parser.py',226),
  ('exit -> EXIT','exit',1,'p_exit','parser.py',235),
]
