import sys, os, ast, readline, uudb

def main():
    debug = False
    db = uudb.uudb()
    if len(sys.argv) > 1:
        if (sys.argv[1] == "-load"):
            db.load(sys.argv[2])
        elif (sys.argv[1] == "-nuke"):
            db.clear()
        elif (sys.argv[1] == "-debug"):
            debug = True
        elif (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            print("UUDB Usage:")
            print("  python3 main.py [-load inputFile] [-nuke]")
            exit(0)
            
    if debug: print(db)
    run=True
    while run:
        print("Enter Query: ", end="")
        query = input()
        queryRaw = query
        if query == "quit" or query == "q":
            break;
        cmds = query.split(".")
        if len(cmds) < 3 or cmds[0] != "db" or not (cmds[2].startswith("find") or cmds[2].startswith("avg")):
            print("    Error: Invalid query. Try again.")
            continue
        
        qtype = cmds[2].split("(", 1)[0]
        query = cmds[2].split("(", 1)[1].rsplit(")", 1)[0]
        if debug: print(qtype, query)

        if qtype == "find":
            condit = queryRaw.split(".")[2].split(",")[0].split("(", 1)[1]
            fields = [x.strip() for x in query.split(",", 1)[1].split("[")[1].split("]")[0].split(",")]

            recs = db.getRecords(condit)
            proj = db.project(fields, recs)
            db.printRecords(proj, fields)

        elif qtype == "avg":
            print("avg_", query, ": ", db.avg(query), sep="")


    db.close()

main()
