grammar GaiaDSL;

// Parser rules
program: (statement | agentDef | serviceDef | economicInteraction | computationExpression | constraint)+ EOF;

statement: agentDef | serviceDef | economicInteraction | computationExpression | constraint;

agentDef: 'agent' ID '{' agentBody '}';

agentBody: (agentProperty | agentBehavior)*;

agentProperty: 'identity' ':' STRING
             | 'type' ':' STRING
             | 'specialty' ':' STRING
             | 'capabilities' ':' capability (',' capability)*
             | 'reputation' ':' reputationMetric (',' reputationMetric)*;

agentBehavior: 'on' event 'do' action (',' action)*;

event: ID; // Define more specific events as needed

action: 'compute' '(' expression ')'
      | 'sendMessage' '(' STRING ')'
      | 'callContract' '(' contractCall ')';

contractCall: STRING; // Define more specific contract call structure as needed

serviceDef: 'service' ID '{' serviceBody '}';

serviceBody: (serviceProperty | computationExpression)*;

serviceProperty: 'provides' ':' STRING
               | 'cost' ':' NUMBER 'GAIA'
               | 'computedBy' ':' STRING;

economicInteraction: 'requestService' serviceCall 'withPayment' NUMBER 'GAIA'
                   | 'defineCost' serviceCost
                   | 'callContract' contractCall;

serviceCall: ID; // Define more specific service call structure as needed

serviceCost: ID 'costs' NUMBER 'GAIA';

computationExpression: 'computation' '(' expression ')';

constraint: 'constraint' ID '{' constraintBody '}';

constraintBody: (constraintProperty)*;

constraintProperty: 'riskLevel' ':' STRING
                  | 'timeLimit' ':' NUMBER;

// Lexer rules
ID: [a-zA-Z_][a-zA-Z_0-9]*;
STRING: '"' (~["\\] | '\\' .)* '"';
NUMBER: [0-9]+ ('.' [0-9]+)?;
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;