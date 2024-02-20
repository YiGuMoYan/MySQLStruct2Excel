import pymysql
import openpyxl

host = ''
port = 3306
user = ''
password = ''
database_name = ''


db = pymysql.connect(host=host, port=port, user=user, password=password, db=database_name, charset='utf8')
cursor = db.cursor()

def get_tables():
    sql = "show tables"
    cursor.execute(sql)
    tables = cursor.fetchall()
    return [table_name[0] for table_name in tables]

def get_struct(table_name):
    sql = "SELECT " \
        "COLUMN_NAME 列名, COLUMN_TYPE 数据类型, IS_NULLABLE 是否为空, COLUMN_DEFAULT 默认值, COLUMN_COMMENT 备注 " \
        "FROM " \
        "INFORMATION_SCHEMA.COLUMNS " \
        "where " \
        f"table_schema ='{database_name}'" \
        "AND " \
        f"table_name = '{table_name}'" \
        "ORDER BY " \
        "ORDINAL_POSITION"

    cursor.execute(sql)
    structure = cursor.fetchall()
    print(structure)
    return structure


if __name__ == '__main__':
    wb = openpyxl.Workbook()
    ws = wb['Sheet']
    wb.remove(ws)

    for table in get_tables():
        structs = get_struct(table)

        ws = wb.create_sheet(table)
        ws.append(['列名', '数据类型', '空', '默认值', '备注'])
        fields = [list(struct) for struct in structs]

        for field in fields:
            ws.append(field)
    
    wb.save(f'{database_name}.xlsx')
