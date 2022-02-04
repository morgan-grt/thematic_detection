dbs = db.getMongo().getDBNames();
dbname = "mail_db";
if (dbs.includes(dbname))
{
	print("yes");
}
else
{
	print("no");
}