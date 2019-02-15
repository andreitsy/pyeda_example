import os
import random
import pandas as pd

from collections import namedtuple
from argparse import ArgumentParser
from pyeda import inter as eda
from pathlib import Path
from pyeda.boolalg.boolfunc import Function
from graphviz import Source

RESULT_FIELD = 'result'

TruthTable = namedtuple("TruthTable", ['table', 'variables'])

def bdd_visualization(expression: eda.Expression, output_file_path: Path):
    """function which create pnd file with expression"""
    graph = Source(expression.to_dot())
    graph.render(output_file_path, view=False, format="pdf")


def get_random_unit_expr(variables: eda.farray):
    """
    Get 1 by using random variable
    :param variables: tupple of variables which we can use
    :return: pyeda expr
    """
    rnd_var = random.choice(variables)
    if random.randint(0, 100) % 2 == 0:
        return rnd_var | ~rnd_var
    else:
        return eda.Or(eda.And(rnd_var, ~rnd_var, simplify=False), eda.expr(1), simplify=False)


def generate_random_expression(expression_base: eda.Expression):
    """
    Generate random expression from base expressiong
    :param expression_base: base expresion which used to generate random expression from it
    :return:
    """
    random_expressions = list()
    current_expr = expression_base
    for x in TruthTable.variables:
        cofactor_by_x = Function.cofactors(current_expr, vs=[x])
        restrict_1 = cofactor_by_x[0]
        restrict_0 = cofactor_by_x[1]

        def one(): return get_random_unit_expr(TruthTable.variables)  # for short expression
        # from Boole's expansion theorem:
        # expression_base == restrict_0 & x | restrict_1 & ~x
        # in the following statement I multiply by 1 several terms in Boole's expansion
        random_expr = one() & restrict_0 & one() & x & one() | one() & restrict_1 & one() & ~x & one()
        random_expressions.append(random_expr)

    return random.choice(random_expressions)


def convert_df_to_truthtable(df: pd.DataFrame):
    """
    Convert obtained data frame to truthtable
    :param df: dataframe with truthtable
    :return TruthTable: truthtable from pyeda
    """

    not_result_column_names = list(df.drop(RESULT_FIELD, axis=1))
    # let us sort the data in expected format for pyeda
    result_column = df.sort_values(by=not_result_column_names, ascending=True)

    # truthtable func expect '-' as nan value
    result = [str(int(val)) if not isnull else "-"
              for isnull, val in zip(result_column[RESULT_FIELD].isnull(), result_column[RESULT_FIELD])]
    x = eda.exprvars('x', len(not_result_column_names))
    result_str = "".join(result)

    return TruthTable(eda.truthtable(x, result_str), x)


def read_csv(file_path: Path):
    """
    Read csv file with truth table in format:
    x,y,result
    0,0,1
    0,1,0
    1,0,0
    1,1,1

    :param file_path: path to csv file with truth table
    :return: pandas data frame with content of the file
    """
    content = pd.read_csv(file_path, delimiter=",")
    if RESULT_FIELD not in content:
        raise ValueError('Field "{}" is not present in the file {}'.format(RESULT_FIELD, file_path))
    return content


def parse_args():
    parser = ArgumentParser(description='Generate random expresion from csv table')
    parser.add_argument('-s', '--random-seed', type=int, help='random seed value', default=42)
    parser.add_argument('-f', '--file-path', type=str, help='path to file with truth table')
    parser.add_argument('-o', '--output-file-picture', type=str, help='path to file where will be saved png picture',
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    random.seed(a=args.random_seed)

    df_truthtable = read_csv(Path(args.file_path))
    TruthTable = convert_df_to_truthtable(df_truthtable)

    expression_base = eda.truthtable2expr(TruthTable.table)
    expression_min, = eda.espresso_exprs(expression_base)
    expression_random = generate_random_expression(expression_base)

    print("Generated random expression for table:\n", expression_random)
    print("Minimize boolean expressions:\n", expression_min)

    bdd_visualization(expression_min, args.output_file_picture)

    #print(expression_min.equivalent(expression_random))
