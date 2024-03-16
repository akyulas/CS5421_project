
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BOOLEAN COMMA COMMENT DECIMAL EQUAL HEAD_AND_BODY_SEPARATOR IDENTIFIER INTEGER LEFT_BRACKET NOT_EQUAL QUESTION_MARK RIGHT_BRACKET STRING TILDE VARIABLE\n    program : statement program\n            | statement\n            | empty\n    empty :\n    statement : assertion\n              | retraction\n              | query\n              | requirement\n    \n    assertion : clause DECIMAL\n    \n    retraction : clause TILDE\n    \n    query : literal QUESTION_MARK\n    \n    requirement : LEFT_BRACKET IDENTIFIER RIGHT_BRACKET\n    \n    clause : literal HEAD_AND_BODY_SEPARATOR body\n           | literal\n    \n    body : literal COMMA body\n         | literal\n    \n    literal : predicate LEFT_BRACKET RIGHT_BRACKET\n            | predicate LEFT_BRACKET terms RIGHT_BRACKET\n            | predicate\n            | term EQUAL term\n            | term NOT_EQUAL term\n            | VARIABLE HEAD_AND_BODY_SEPARATOR IDENTIFIER LEFT_BRACKET terms RIGHT_BRACKET\n    \n    predicate : IDENTIFIER\n              | STRING\n    \n    terms : term COMMA terms\n          | term\n    \n    term : VARIABLE\n         | constant\n    \n    constant : IDENTIFIER\n             | STRING\n             | INTEGER\n             | BOOLEAN\n    '
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,19,20,21,22,31,],[-4,0,-2,-3,-5,-6,-7,-8,-1,-9,-10,-11,-12,]),'LEFT_BRACKET':([0,2,4,5,6,7,11,12,15,20,21,22,31,40,],[10,10,-5,-6,-7,-8,-23,25,-24,-9,-10,-11,-12,44,]),'VARIABLE':([0,2,4,5,6,7,20,21,22,23,25,26,27,31,41,43,44,],[14,14,-5,-6,-7,-8,-9,-10,-11,14,35,35,35,-12,14,35,35,]),'IDENTIFIER':([0,2,4,5,6,7,10,20,21,22,23,25,26,27,28,31,41,43,44,],[11,11,-5,-6,-7,-8,24,-9,-10,-11,11,36,36,36,40,-12,11,36,36,]),'STRING':([0,2,4,5,6,7,20,21,22,23,25,26,27,31,41,43,44,],[15,15,-5,-6,-7,-8,-9,-10,-11,15,37,37,37,-12,15,37,37,]),'INTEGER':([0,2,4,5,6,7,20,21,22,23,25,26,27,31,41,43,44,],[17,17,-5,-6,-7,-8,-9,-10,-11,17,17,17,17,-12,17,17,17,]),'BOOLEAN':([0,2,4,5,6,7,20,21,22,23,25,26,27,31,41,43,44,],[18,18,-5,-6,-7,-8,-9,-10,-11,18,18,18,18,-12,18,18,18,]),'DECIMAL':([8,9,11,12,15,16,17,18,29,30,32,35,36,37,38,39,42,45,48,],[20,-14,-23,-19,-24,-28,-31,-32,-16,-13,-17,-27,-29,-30,-20,-21,-18,-15,-22,]),'TILDE':([8,9,11,12,15,16,17,18,29,30,32,35,36,37,38,39,42,45,48,],[21,-14,-23,-19,-24,-28,-31,-32,-16,-13,-17,-27,-29,-30,-20,-21,-18,-15,-22,]),'QUESTION_MARK':([9,11,12,15,16,17,18,32,35,36,37,38,39,42,48,],[22,-23,-19,-24,-28,-31,-32,-17,-27,-29,-30,-20,-21,-18,-22,]),'HEAD_AND_BODY_SEPARATOR':([9,11,12,14,15,16,17,18,32,35,36,37,38,39,42,48,],[23,-23,-19,28,-24,-28,-31,-32,-17,-27,-29,-30,-20,-21,-18,-22,]),'COMMA':([11,12,15,16,17,18,29,32,34,35,36,37,38,39,42,48,],[-23,-19,-24,-28,-31,-32,41,-17,43,-27,-29,-30,-20,-21,-18,-22,]),'EQUAL':([11,13,14,15,16,17,18,],[-29,26,-27,-30,-28,-31,-32,]),'NOT_EQUAL':([11,13,14,15,16,17,18,],[-29,27,-27,-30,-28,-31,-32,]),'RIGHT_BRACKET':([16,17,18,24,25,33,34,35,36,37,46,47,],[-28,-31,-32,31,32,42,-26,-27,-29,-30,-25,48,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,2,],[1,19,]),'statement':([0,2,],[2,2,]),'empty':([0,2,],[3,3,]),'assertion':([0,2,],[4,4,]),'retraction':([0,2,],[5,5,]),'query':([0,2,],[6,6,]),'requirement':([0,2,],[7,7,]),'clause':([0,2,],[8,8,]),'literal':([0,2,23,41,],[9,9,29,29,]),'predicate':([0,2,23,41,],[12,12,12,12,]),'term':([0,2,23,25,26,27,41,43,44,],[13,13,13,34,38,39,13,34,34,]),'constant':([0,2,23,25,26,27,41,43,44,],[16,16,16,16,16,16,16,16,16,]),'body':([23,41,],[30,45,]),'terms':([25,43,44,],[33,46,47,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement program','program',2,'p_program','parser.py',6),
  ('program -> statement','program',1,'p_program','parser.py',7),
  ('program -> empty','program',1,'p_program','parser.py',8),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',18),
  ('statement -> assertion','statement',1,'p_statement','parser.py',23),
  ('statement -> retraction','statement',1,'p_statement','parser.py',24),
  ('statement -> query','statement',1,'p_statement','parser.py',25),
  ('statement -> requirement','statement',1,'p_statement','parser.py',26),
  ('assertion -> clause DECIMAL','assertion',2,'p_assertion','parser.py',32),
  ('retraction -> clause TILDE','retraction',2,'p_retraction','parser.py',38),
  ('query -> literal QUESTION_MARK','query',2,'p_query','parser.py',44),
  ('requirement -> LEFT_BRACKET IDENTIFIER RIGHT_BRACKET','requirement',3,'p_requirement','parser.py',50),
  ('clause -> literal HEAD_AND_BODY_SEPARATOR body','clause',3,'p_clause','parser.py',56),
  ('clause -> literal','clause',1,'p_clause','parser.py',57),
  ('body -> literal COMMA body','body',3,'p_body','parser.py',66),
  ('body -> literal','body',1,'p_body','parser.py',67),
  ('literal -> predicate LEFT_BRACKET RIGHT_BRACKET','literal',3,'p_literal','parser.py',76),
  ('literal -> predicate LEFT_BRACKET terms RIGHT_BRACKET','literal',4,'p_literal','parser.py',77),
  ('literal -> predicate','literal',1,'p_literal','parser.py',78),
  ('literal -> term EQUAL term','literal',3,'p_literal','parser.py',79),
  ('literal -> term NOT_EQUAL term','literal',3,'p_literal','parser.py',80),
  ('literal -> VARIABLE HEAD_AND_BODY_SEPARATOR IDENTIFIER LEFT_BRACKET terms RIGHT_BRACKET','literal',6,'p_literal','parser.py',81),
  ('predicate -> IDENTIFIER','predicate',1,'p_predicate','parser.py',94),
  ('predicate -> STRING','predicate',1,'p_predicate','parser.py',95),
  ('terms -> term COMMA terms','terms',3,'p_terms','parser.py',101),
  ('terms -> term','terms',1,'p_terms','parser.py',102),
  ('term -> VARIABLE','term',1,'p_term','parser.py',111),
  ('term -> constant','term',1,'p_term','parser.py',112),
  ('constant -> IDENTIFIER','constant',1,'p_constant','parser.py',118),
  ('constant -> STRING','constant',1,'p_constant','parser.py',119),
  ('constant -> INTEGER','constant',1,'p_constant','parser.py',120),
  ('constant -> BOOLEAN','constant',1,'p_constant','parser.py',121),
]