import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

with open('./samples/2.json', 'r') as f:
    text = f.read()
    text = text.replace("'", '"')
    text = text.replace("None", '""')
    r = json.loads(text)

# pp.pprint(r)
report = {}

# # Preparing data to be presented
report['source_type'] = r["sourceType"]
report['source_format'] = r["sourceFormat"]
report['source_list'] = r["sourceList"]

#meta
if "coveredInstructions" in r["meta"].keys():
    report['n_ins'] = r["meta"]["coveredInstructions"]
if "coveredPaths" in r["meta"].keys():
    report['n_paths'] = r["meta"]["coveredPaths"]
if "selectedCompiler" in r["meta"].keys():
    report['compiler'] = r["meta"]["selectedCompiler"]

#issues
r = r["issues"]
# report['source_map'] = r["locations"][0]["sourceMap"]
# report['severity'] = r["severity"]
# report['swc_id'] = r["swcID"]
# report['swc_title'] = r["swcTitle"]
# report['summary'] = r["description"]["head"]
# report['detail'] = r["description"]["tail"]

with open('./templates/index.md', 'r') as f:
    data = f.read()

new_data = ''
j = 0
while j<len(data):
    if (data[j] == '$' and data[j + 1] == '{'):
        idx = j + 2
        variable = ''
        while (data[idx] != '}'):
            variable = variable + data[idx]
            idx += 1
        j = j + 3 + len(variable) 
        if variable == 'issues':
            new_data += 'Issues' + '\n'
            for i in range(0,len(r)):
                new_data += '### ' + '_' + r[i]["swcTitle"] + '_' + '\n' + r[i]["description"]["head"] + '\n' + '\n' + r[i]["description"]["tail"]
                new_data += '\n' + '\n' + '**Issue ID under Smart Contract Weakness Classification and Test Cases: '
                new_data +=  r[i]["swcID"] + '**' + '\n' + '\n'
                new_data += '**' + r[i]["severity"] + ' Severity**' + '\n' + '\n'
                new_data += '#### Locations' + '\n'
                new_data += 'The compiler generates a mapping from the bytecode to the range in the source code that generated the instruction known as source mapping.' + '\n'
                new_data +=  '\n' + 'For this particular issue the source mapping is <br/>' + '\n'
                new_data += '_' + r[i]["locations"][0]["sourceMap"] + '_' + '\n' + '\n'
                slf = r[i]["locations"][0]["sourceMap"].split(':')
                new_data += 'Where ' + slf[0] + ' is the byte-offset to the start of the range in the source file, '
                new_data += slf[1] + ' is the length of the source range in bytes and ' + slf[2]
                new_data +=  ' is the index in sourceList.' + '\n' + '\n'

        elif variable in report.keys():
            new_data += str(report[variable])
    else:
        new_data += data[j]
        j = j + 1

print(new_data)
with open('./reports/2.md', 'w') as f:
    f.write(new_data)