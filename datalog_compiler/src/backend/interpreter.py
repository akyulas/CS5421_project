from backend.sql_statement_generator import *
from common.node_names import *
from backend.views import Views
from backend.comparison import Comparison
from backend.body_processed_results import BodyProcessedResults
from backend.constants import *
import traceback

# Rule Types
INTERPRET_RULE_TYPE = "INTERPRET RULE"
CREATE_AND_INSERT_RULE_TYPE = "CREATE AND INSERT"
QUERY_RULE_TYPE = "QUERY"
UNSUPPORTED_RULE_TYPE = "UNSUPPORTED"

# Statement Types
CREATE_TABLE_STATEMENT_TYPE = "CREATE TABLE"
INSERT_TABLE_STATEMENT_TYPE = "INSERT TABLE"
CREATE_VEW_STATEMENT_TYPE = "CREATE VIEW"
DROP_VIEW_STATEMENT_TYPE = "DROP VIEW"
QUERY_STATEMENT_TYPE = "QUERY"

COMPARISON_OPERATORS = {'>', '<', '=', '!=', '<>', '>=', '<='}

class Interpreter:
    def __init__(self):
        self.tables_dic = {}
        self.views_dic = {}

    def get_node_name(self, tup):
        return tup[0]

    def get_value(self, node_val, tup, idx=1):
        assert tup[0] == node_val
        return tup[idx]

    def check_value_of_statement(self, statement):
        if self.get_node_name(statement) == ASSERTION_NODE:
            if self.traverse_and_get_value([ASSERTION_NODE, CLAUSE_NODE], statement) == ':-':
                return INTERPRET_RULE_TYPE
            return CREATE_AND_INSERT_RULE_TYPE
        if self.get_node_name(statement) == QUERY_NODE:
            return QUERY_RULE_TYPE
        return UNSUPPORTED_RULE_TYPE

    def traverse_and_get_value(self, list_of_node_names, node, list_of_idx=None):
        node_val = node
        for idx, node_name in enumerate(list_of_node_names):
            if list_of_idx is not None:
                node_val = self.get_value(node_name, node_val, list_of_idx[idx])
            else:
                node_val = self.get_value(node_name, node_val)
        return node_val
    
    def get_name_of_view_or_table(self, statement):
        if statement[0] == ASSERTION_NODE:
            return self.traverse_and_get_value(
                [ASSERTION_NODE, CLAUSE_NODE, LITERAL_NODE, PREDICATE_NODE],
                statement
            )
        return self.traverse_and_get_value(
            [LITERAL_NODE, PREDICATE_NODE],
            statement
        )
    
    def get_terms_of_view_or_table(self, statement):
        if statement[0] == ASSERTION_NODE:
            return self.traverse_and_get_value(
                [ASSERTION_NODE, CLAUSE_NODE, LITERAL_NODE, TERMS_NODE],
                statement,
                [1, 1, 3, 1]
            )
        return self.traverse_and_get_value(
            [LITERAL_NODE, TERMS_NODE],
            statement,
            [3, 1]
        )

    def interpret_create_and_insert_table_statement(self, statement):
        table_name = self.get_name_of_view_or_table(statement)
        terms = self.get_terms_of_view_or_table(statement)
        columns = []
        for term in terms:
            columns.append(self.traverse_and_get_value([TERM_NODE, CONSTANT_NODE], term))
        if table_name in self.tables_dic:
            return [(INSERT_TABLE_STATEMENT_TYPE, table_name, get_insert_statement(table_name, columns))]
        self.tables_dic[table_name] = len(columns)
        return self.get_create_and_insert_table_statement(table_name, columns)
    
    def get_create_and_insert_table_statement(self, table_name, columns):
        sql_statements = []
        sql_statements.append((CREATE_TABLE_STATEMENT_TYPE, table_name, get_create_statement(table_name, columns)))
        sql_statements.append((INSERT_TABLE_STATEMENT_TYPE, table_name, get_insert_statement(table_name, columns)))
        return sql_statements
    
    def clean_up_view_statements(self, newly_created_view_statements_tuple, existing_sql_translations):
        # Used to remove CREATE VIEW statements that still haven't been executed in postgres to avoid redundant CREATE VIEW and DROP VIEW
        view_statements_tuple_to_extend_with = []
        indexes_in_existing_sql_translations_to_delete = []
        for newly_created_view_statement_tuple in newly_created_view_statements_tuple:
            statement_type, view_name, _ = newly_created_view_statement_tuple
            if statement_type == DROP_VIEW_STATEMENT_TYPE:
                extra_indexes_to_delete = [i for i in range(len(existing_sql_translations)) if existing_sql_translations[i][0] == CREATE_VEW_STATEMENT_TYPE and existing_sql_translations[i][1] == view_name]
                if extra_indexes_to_delete:
                    indexes_in_existing_sql_translations_to_delete.extend(extra_indexes_to_delete)
                    continue
            view_statements_tuple_to_extend_with.append(newly_created_view_statement_tuple)
        for index in sorted(indexes_in_existing_sql_translations_to_delete, reverse=True):
            del existing_sql_translations[index]
        existing_sql_translations.extend(view_statements_tuple_to_extend_with)
        return existing_sql_translations
    
    def process_head_when_creating_view(self, head):
        view_name = self.get_name_of_view_or_table(head)
        terms_of_head = self.get_terms_of_view_or_table(head)
        columns_of_head = [
            self.get_value(TERM_NODE, term) for term in terms_of_head
        ]
        return view_name, columns_of_head
    
    def process_comparison_term(self, comparison_term, columns_seen):
        term = self.get_value(TERM_NODE, comparison_term)
        if not isinstance(term, tuple):
            if term not in columns_seen:
                raise Exception("Assessing a column that is not seen yet")
            return [(VAR_KEY, term)]
        if term[0] == CONSTANT_NODE:
            return [(CONSTANT_KEY, self.get_value(CONSTANT_NODE, term))]
        raise Exception("Comparison term is not supported yet")
    
    def process_constraints(self, literal, columns_seen):
        left_side = self.get_value(LITERAL_NODE, literal, 1)
        operator =  self.get_value(LITERAL_NODE, literal, 2)
        right_side = self.get_value(LITERAL_NODE, literal, 3)
        return Comparison(self.process_comparison_term(left_side, columns_seen), operator, self.process_comparison_term(right_side, columns_seen))
    
    def process_body_when_creating_view(self, body):
        results = BodyProcessedResults()
        literals = self.get_value(BODY_NODE, body)
        columns_seen = set()
        for literal in literals:
            if len(literal) == 4 and literal[2] in COMPARISON_OPERATORS:
                results.constraints.append(self.process_constraints(literal, columns_seen))
                continue
            table_or_view_name = self.get_name_of_view_or_table(literal)
            terms = self.get_terms_of_view_or_table(literal)
            columns_of_body = [
                self.get_value(TERM_NODE, term) for term in terms
            ]
            results.table_or_view_name_to_columns_dic[table_or_view_name] = columns_of_body
            columns_seen.update(columns_of_body)
        return results
    
    def validate_view_graph(self, columns_of_view, body_dic):
        unreferenced_column = set(columns_of_view)
        referenced_column = set()
        for table_or_view_name, cols in body_dic.items():
            if table_or_view_name not in self.tables_dic and table_or_view_name not in self.views_dic:
                raise Exception("Referencing a view or table not created previously")
            for col in cols:
                if col in unreferenced_column:
                    referenced_column.add(col)
        assert unreferenced_column.difference(referenced_column) == set()
    
    def create_view_graph_and_create_view(self, statement):
        head = self.get_value(ASSERTION_NODE, statement)[2]
        body = self.get_value(ASSERTION_NODE, statement)[3]
        view_name, columns_of_view = self.process_head_when_creating_view(head)
        body_processed_result = self.process_body_when_creating_view(body)
        self.validate_view_graph(columns_of_view, body_processed_result.table_or_view_name_to_columns_dic)
        if view_name in self.views_dic:
            view = self.views_dic[view_name]
            assert view.cols == columns_of_view
            view.body_processed_results.append(body_processed_result)
        else:
            self.views_dic[view_name] = Views(view_name, columns_of_view, False, [body_processed_result])
        return self.interpret_creation_of_view(view_name)

    def interpret_creation_of_view(self, view_name):
        statements = []
        view = self.views_dic[view_name]
        if view.is_executed:
            statements.append((DROP_VIEW_STATEMENT_TYPE, view_name, get_drop_view_statement(view_name)))
        for body in view.body_processed_results:
            for dependent_table_or_view_name in body.table_or_view_name_to_columns_dic.keys():
                if dependent_table_or_view_name == view_name:
                    continue
                if dependent_table_or_view_name in self.tables_dic:
                    continue
                if dependent_table_or_view_name in self.views_dic:
                    if not self.views_dic[dependent_table_or_view_name].is_executed:
                        # Shouldn't reach here ideally after lazy evaluation of rule, but no harm processing this code
                        statements.extend(self.interpret_creation_of_view(dependent_table_or_view_name))
                    continue
                # Shouldn't reached here
                raise Exception("Referencing a view or table not created previously")
        statements.append((CREATE_VEW_STATEMENT_TYPE, view_name, create_view_statement(view)))
        view.is_executed = True
        return statements
    
    def interpret_query_statement(self, statement):
        statements = []
        table_or_view_name = self.traverse_and_get_value(
            [QUERY_NODE, LITERAL_NODE, PREDICATE_NODE],
            statement
        )
        if table_or_view_name in self.tables_dic:
            len_of_columns = self.tables_dic[table_or_view_name]
        else:
            len_of_columns = len(self.views_dic[table_or_view_name].cols)
        terms = self.traverse_and_get_value(
            [QUERY_NODE, LITERAL_NODE, TERMS_NODE],
            statement,
            [1, 3, 1]
        )
        assert len(terms) == len_of_columns
        constraints = {}
        for i in range(len_of_columns):
            term = self.get_value(TERM_NODE, terms[i])
            if type(term) is tuple:
                constraints[i] = (self.get_value(CONSTANT_NODE, term))
        statements.append((QUERY_STATEMENT_TYPE, table_or_view_name, get_basic_query_statement(table_or_view_name, constraints)))
        return statements

    def interpret_statements(self, statements):
        sql_translation_tuples = []
        for statement_node, statement in statements:
            assert statement_node == STATEMENT_NODE
            type_of_statement = self.check_value_of_statement(statement)
            if type_of_statement not in {CREATE_AND_INSERT_RULE_TYPE, INTERPRET_RULE_TYPE, QUERY_RULE_TYPE}:
                raise Exception("Unsupported statement type")
            try:
                if type_of_statement == CREATE_AND_INSERT_RULE_TYPE:
                    sql_translation_tuples.extend(self.interpret_create_and_insert_table_statement(statement))
                elif type_of_statement == INTERPRET_RULE_TYPE:
                    interpret_rules_statements_tuple = self.create_view_graph_and_create_view(statement)
                    sql_translation_tuples = self.clean_up_view_statements(interpret_rules_statements_tuple, sql_translation_tuples)
                else:
                    sql_translation_tuples.extend(self.interpret_query_statement(statement))
            except Exception:
                traceback.print_exc()
                sql_translation_tuples.append((None, None, '---- Invalid statement'))
        sql_translations = [sql_translation_tuple[2] for sql_translation_tuple in sql_translation_tuples]
        return sql_translations

    def interpret(self, ast):
        assert self.get_node_name(ast) == PROGRAM_NODE
        return self.interpret_statements(ast[1])