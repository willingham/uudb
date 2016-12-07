import sys, os, ast, readline, uudb

def main():
    debug = False
    db = uudb.uudb()
    if len(sys.argv) > 1:
        if (sys.argv[1] == "-load"): db.load(sys.argv[2])
        elif (sys.argv[1] == "-nuke"): db.clear()
        elif (sys.argv[1] == "-debug"): debug = True
        elif (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            print("UUDB Usage:")
            print("  python3 main.py [-load inputFile] [-nuke]")
            exit(0)
            
    if debug: print(db)
    run=True
    while run:
        query = queryRaw = input("Enter query: ")
        if query == "quit" or query == "q": break
        cmds = query.split(".")
        if len(cmds) < 3 or cmds[0] != "db" or not \
                (cmds[2].startswith("find") or cmds[2].startswith("avg") or \
                 cmds[2].startswith("min") or cmds[2].startswith("count")):
            print("    Error: Invalid query. Try again.")
            continue
        
        qtype = cmds[2].split("(", 1)[0]
        query = cmds[2].split("(", 1)[1].rsplit(")", 1)[0]
        if debug: print(qtype, query)

        if qtype == "find":
            condit = queryRaw.split(".")[2].split(",")[0].split("(", 1)[1]
            fields = [x.strip() for x in query.split(",", 1)[1].split("[")[1].split("]")[0].split(",")]

            recs = db.getRecords(condit)
            if recs == None:
                print("    Error: Invalid query. Try again.")
                continue
            proj = db.project(fields, recs)
            total = db.printRecords(proj, fields)
            if total > 0: print("Records found:", total)

        elif qtype == "avg":
            x = db.avg(query)
            if not x == None: print("avg_", query, ": ", x, sep="")
        
        elif qtype == "min":
            x = db.minimum(query)
            if not x == None: print("min_", query, ": ", x, sep="")

        elif qtype == "count":
            x = db.count(query)
            if not (x == None or x == 0): print("count_", query, ": ", x, sep="")
    db.close()

main()
