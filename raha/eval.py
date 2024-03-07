import duckdb
import pandas as pd


def do_eval(data, eval_attrs, output_file):
    df_raw = data.dataframe
    df_clean = data.clean_dataframe
    df_repair = data.repaired_dataframe

    column_rename = ", ".join([f"t1.{attr} as {attr}, t2.{attr} as {attr}_gt, t3.{attr} as {attr}_repair" for attr in eval_attrs])

    sql = f'select t1.id, t1.xy, {column_rename} from df_raw t1, df_clean t2, df_repair t3 where t1.id = t2.id and t1.id = t3.id'
    df_eval = duckdb.query(sql).to_df()

    null_count = 0
    wrong_count = 0
    error_count = 0
    repair_count = 0
    correct_repair_count = 0
    eval_stat = []

    for attr in eval_attrs:
        sql_null = f"SELECT count(1) FROM df_eval WHERE {attr} is null"
        sql_wrong = f"SELECT count(1) FROM df_eval WHERE {attr} is not null AND {attr} <> {attr}_gt"
        attr_null_count = duckdb.query(sql_null).fetchone()[0]
        attr_wrong_count = duckdb.query(sql_wrong).fetchone()[0]

        sql_error = f"SELECT count(1) FROM df_eval WHERE {attr} <> {attr}_gt"
        sql_repair = f"SELECT count(1) FROM df_eval WHERE {attr} <> {attr}_repair"
        sql_correct_repair = f"SELECT count(1) FROM df_eval WHERE {attr} <> {attr}_gt AND {attr}_repair = {attr}_gt"
        attr_error_count = duckdb.query(sql_error).fetchone()[0]
        attr_repair_count = duckdb.query(sql_repair).fetchone()[0]
        attr_correct_repair_count = duckdb.query(sql_correct_repair).fetchone()[0]

        null_count += attr_null_count
        wrong_count += attr_wrong_count
        error_count += attr_error_count
        repair_count += attr_repair_count
        correct_repair_count += attr_correct_repair_count

        if attr_repair_count == 0:
            precision = -1
        else:
            precision = attr_correct_repair_count / attr_repair_count
        recall = attr_correct_repair_count / attr_error_count

        attr_stat = {
            "attr": attr,
            "null_count": attr_null_count,
            "wrong_count": attr_wrong_count,
            "error_count": attr_error_count,
            "repair_count": attr_repair_count,
            "correct_repair_count": attr_correct_repair_count,
            "precision": precision,
            "recall": recall,
            "f1": 2 * precision * recall / (precision + recall),
        }
        eval_stat.append(attr_stat)

    if repair_count == 0:
        precision = -1
    else:
        precision = correct_repair_count / repair_count
    recall = correct_repair_count / error_count
    overall_stat = {
        "attr": "overall",
        "null_count": null_count,
        "wrong_count": wrong_count,
        "error_count": error_count,
        "repair_count": repair_count,
        "correct_repair_count": correct_repair_count,
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall),
    }
    eval_stat.append(overall_stat)

    df_eval_stat = pd.DataFrame(eval_stat)
    df_eval_stat = df_eval_stat[["attr", "precision", "recall", "f1", "null_count", "wrong_count", "error_count", "repair_count", "correct_repair_count"]]
    t = df_eval_stat.set_index("attr").T
    t = t.rename_axis("metric", axis=1)
    t = t[["overall"] + eval_attrs]
    pd.set_option("display.precision", 3)
    print(t)

    t.to_csv(output_file, float_format="%.3f")