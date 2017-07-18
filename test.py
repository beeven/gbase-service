from suds.client import Client
url = 'http://gdirp3.gdfsc.intra.customs.gov.cn/ChinaCustoms.JGIRP.PerpheralInterface.WcfLib.GBaseService.GBaseService.svc?wsdl'
client = Client(url)

result = client.service.SearchGBaseRtnJson(appName='2', sql='select * from GODS.ENTRY_HEAD limit 1')
print(result)

