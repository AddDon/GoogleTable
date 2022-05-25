from clickhouse_mgr import ClickHouseMgr



def ch_query(query):
	dbClhMgr = ClickHouseMgr()

	dbClhMgr.setConnParams(
		"srv-cortel-bi", 
		"ui",
		"analiz",
		"bi"
	)

	dbClhMgr.connect()


	items = dbClhMgr.execQuery(query)
	if items == False:
		print(dbClhMgr.getLastError())
			
	return items		
	

