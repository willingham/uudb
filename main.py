import sys, os, ast, uudb

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
            
    if debug: print(db)
    new = {}
    new["EID"] = "222"
    #db.insertRecord(new)
    if debug: print(db)
    var = ["EID"]
    val = ["777"]
    fields = ["EID", "Dept"]
    recs = db.getRecords(var, val)
    proj = db.project(fields, recs)
    #db.printRecords(proj, fields)
    #db.printRecords(db.project(["EID"]), ["EID"])
    run=True
    while run:
        print("Enter Query: ", end="")
        query = input()
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
            condit = [x.strip() for x in query.split(",", 1)[0].split("(")[1].split(")")[0].split("and")]
            fields = [x.strip() for x in query.split(",", 1)[1].split("[")[1].split("]")[0].split(",")]

            recs = db.getRecords(var, val, operator)
            proj = db.project(fields, recs)
            db.printRecords(proj, fields)

        elif qtype == "avg":
            print("avg_", query, ": ", db.avg(query), sep="")


    db.close()

main()
