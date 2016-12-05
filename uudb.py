import json, re, uuid, sys

class uudb:
    def __init__(self, inFile=None):
        self._inFile = inFile
        self._record = None
        if inFile:
            processIn()
        with open("final.json", "r") as jsonData:
            self._db = json.load(jsonData)

    def insertRecord(self, d): #takes a dictionary
        self._db["final"].append(d)

    def meetsCond(self, record, cond):
        x = cond.split("=")
        op = "="
        if len(x) < 2:
            x = cond.split("<>")
            op = "<>"
        if len(x) < 2:
            x = cond.split("<")
            op = "<"
        if len(x) < 2:
            x = cond.split(">")
            op = ">"
        var = str(x[0])
        val = str(x[1])
        if op == "=":
            if record.get(var) == val:
                return True
            else:
                return False
        elif op == "<>":
            if not record.get(var) == val:
                return True
            else:
                return False
        elif op == "<":
            return record.get(var) and int(record.get(var)) < int(val)
        elif op == ">":
            return record.get(var) and int(record.get(var)) > int(val)
        else:
            return False

    def rep(self, match):
        x = "self.meetsCond(" + str(self._record) + ", \"" + match.group() + "\")"
        return x

    def getRecords(self, conds):
        if conds == "()":
            return self._db["final"]
        result = []
        for record in self._db["final"]:
            self._record = record
            cond = re.sub(r'\w+([>=<]|<>)\w+', self.rep, conds)
            if eval(cond):
                result.append(record)
        return result

    def project(self, fields, records=None): # takes a list of fields to project
        if fields[0] == "":
            return records
        result = []
        p = 1
        for record in records:
            for field in fields:
                if record.get(field):
                    result.append(record)
                    break;
        return result

    def printRecords(self, records, fields=[]):
        if fields[0] == "":
            for record in records:
                print(" ".join([x + ": " + record[x] for x in record.keys()]))
        else:
            for record in records:
                for field in fields:
                    if record.get(field) != None:
                        print(field, ": ", record[field], sep="", end=" ")
                print()

    def avg(self, field):
        values = []
        for record in self._db["final"]:
            if record.get(field) != None:
                values.append(record[field])
        values = [int(x) for x in values]
        return sum(values)/len(values) 
        
    def load(self, fName):
        records = []
        with open(fName, "r") as fil:
            for line in fil:
                print("Importing:", line, end="")
                record = {}
                line = line.strip().split(" ")
                if len(line) % 2 != 0:
                    print("Error: Invalid Line -->", str(line))
                    exit(1)
                line = [x.strip() for x in line]
                line = [x.strip(":") for x in line]
                record["ID"] = str(uuid.uuid4().int)
                for i in range(0, len(line), 2):
                    record[line[i]] = line[i+1]
                records.append(record)

        for record in records:
            self._db["final"].append(record)

    def clear(self):
        self._db = {"final": []}

    def close(self):
        with open("final.json", "w+") as outFile:
            json.dump(self._db, outFile)

    def __str__(self):
        return str(self._db)
