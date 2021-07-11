from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from python_hll.hll import HLL
import mmh3
from collections import deque
import psycopg2
import psycopg2.extras


DB_HOST = "localhost"
DB_NAME = "srib"
DB_USER = "pritesh"
DB_PASS = "samsung@0411"


def index(request):
    return render(request, 'index.html',)


@csrf_exempt
def parseData(request):
    if(request.method == "POST"):
        print(request.POST)
        print(request.body)
        data = json.loads(request.body)
        data = data['sql']
        print(type(data))
        x = data.replace("category", "")
        y = x.replace("AND", "&")
        z = y.replace("OR", "|")
        s = z.replace(" ", "")
        exp = s.replace("=", "")
        print(exp)
        z = solve(exp)
        print(z)
        context = {"exp": z}
        print(json.dumps(context))
        return HttpResponse(json.dumps(context))
    else:
        return HttpResponse("Get Method Not Allowed")


def solve(x):
    # l = len(x)
    # # print(l)
    # postexp = ""
    # check = 0
    # check2 = 0
    # oper_stack = deque()

    # for i in range(l):
    #     if (x[i] == ' '):
    #         if check == 1:
    #             postexp += " "
    #             check = 0
    #     elif (x[i] == '('):
    #         oper_stack.append('(')
    #         check2 = 1
    #     elif (x[i] == ')'):
    #         while oper_stack and oper_stack[-1] != '(':
    #             if check == 1:
    #                 postexp += " "
    #             postexp += oper_stack.pop()
    #             check = 1
    #         oper_stack.pop()
    #         check2 = 1
    #     elif (x[i] == '&'):
    #         while oper_stack and oper_stack[-1] == '&':
    #             if check == 1:
    #                 postexp += " "
    #             postexp += oper_stack.pop()
    #             check = 1
    #         oper_stack.append(x[i])
    #         check2 = 1
    #     elif (x[i] == '|'):
    #         while oper_stack and oper_stack[-1] != '(':
    #             if check == 1:
    #                 postexp += " "
    #             postexp += oper_stack.pop()
    #             check = 1
    #         oper_stack.append(x[i])
    #         check2 = 1
    #     else:
    #         if check2 == 1 and check == 1:
    #             postexp += " "
    #             check2 = 0
    #             check = 0
    #         postexp += x[i]
    #         check = 1
    #         check2 = 0

    # while oper_stack:
    #     postexp += " "
    #     postexp += oper_stack.pop()
    # postexp += " "
    # postlen = len(postexp)
    # # print(postexp)
    # # print(postlen)

    # conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
    #                         password=DB_PASS, host=DB_HOST)

    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # cur.execute("CREATE TABLE temp (seg_id INT PRIMARY KEY, target hll);")
    # conn.commit()

    # count = 0
    # eval_stack = deque()
    # table_stack = deque()
    # ck = 0
    # serial = 11
    # for i in range(postlen):
    #     if(postexp[i] == ' '):
    #         if(ck == 1):
    #             eval_stack.append(count)
    #             table_stack.append(1)
    #             ck = 0
    #             count = 0
    #     elif(postexp[i] == '&'):
    #         a1 = eval_stack.pop()
    #         t1 = table_stack.pop()
    #         a2 = eval_stack.pop()
    #         t2 = table_stack.pop()
    #         if(t1 == 1):
    #             cur.execute(
    #                 "INSERT INTO temp (seg_id,target) SELECT seg_id, cardin FROM data_table WHERE seg_id = %s;", (a1,))
    #         if(t2 == 1):
    #             cur.execute(
    #                 "INSERT INTO temp (seg_id,target) SELECT seg_id, cardin FROM data_table WHERE seg_id = %s;", (a2,))
    #         cur.execute("INSERT INTO temp (seg_id) VALUES (%s);", (serial,))
    #         conn.commit()
    #         cur.execute(
    #             "UPDATE temp SET target = (SELECT hll_union_agg(target) FROM temp WHERE seg_id = %s AND seg_id = %s) WHERE seg_id = %s;", (a1, a2, serial,))
    #         conn.commit()
    #         cur.execute(
    #             "DELETE FROM temp WHERE seg_id = %s OR seg_id = %s;", (a1, a2,))
    #         eval_stack.append(serial)
    #         table_stack.append(2)
    #         serial += 1

    #     elif(postexp[i] == '|'):
    #         a1 = eval_stack.pop()
    #         t1 = table_stack.pop()
    #         a2 = eval_stack.pop()
    #         t2 = table_stack.pop()
    #         if(t1 == 1):
    #             cur.execute(
    #                 "INSERT INTO temp (seg_id,target) SELECT seg_id, cardin FROM data_table WHERE seg_id = %s;", (a1,))
    #         if(t2 == 1):
    #             cur.execute(
    #                 "INSERT INTO temp (seg_id,target) SELECT seg_id, cardin FROM data_table WHERE seg_id = %s;", (a2,))
    #         cur.execute("INSERT INTO temp (seg_id) VALUES (%s);", (serial,))
    #         conn.commit()
    #         cur.execute(
    #             "UPDATE temp SET target = (SELECT hll_union_agg(target) FROM temp WHERE seg_id = %s OR seg_id = %s) WHERE seg_id = %s;", (a1, a2, serial,))
    #         conn.commit()
    #         cur.execute(
    #             "DELETE FROM temp WHERE seg_id = %s OR seg_id = %s;", (a1, a2,))
    #         conn.commit()
    #         eval_stack.append(serial)
    #         table_stack.append(2)
    #         serial += 1
    #     else:
    #         b1 = (int)(postexp[i]) - (int)('0')
    #         count *= 10
    #         count += b1
    #         ck = 1

    # if(table_stack[-1] == 1):
    #     cur.execute(
    #         "INSERT INTO temp (seg_id,target) SELECT seg_id, cardin FROM data_table WHERE seg_id = %s;", (eval_stack[-1],))

    # conn.commit()
    # cur.execute(
    #     "SELECT hll_cardinality(target) FROM temp WHERE seg_id = %s;", (eval_stack[-1],))
    # ans = cur.fetchone()

    # cur.execute("DROP TABLE temp;")
    # conn.commit()
    # cur.close()

    # conn.close()
    # return ans[0]
    return len(x)
