import xmltodict
import json

with open("reports/mailxray_report.xml") as f:
    junit_xml = xmltodict.parse(f.read())

with open("results.json", "w") as f:
    json.dump(junit_xml, f, indent=2)