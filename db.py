import sqlite3

def get_connection(use_memory=True, db_file="database.db"):
	"""
	Returns a SQLite connection.
	If use_memory is True, uses in-memory DB. Otherwise, uses file-based DB.
	"""
	if use_memory:
		return sqlite3.connect(":memory:")
	else:
		return sqlite3.connect(db_file)


def create_tables(conn):
	"""
	Creates user_profile and chat_history tables if they do not exist.
	user_profile: user_id (auto-increment int), mail_id (varchar)
	chat_history: user_id (int), history (JSON)
	"""
	cursor = conn.cursor()
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS user_profile (
			user_id INTEGER PRIMARY KEY AUTOINCREMENT,
			mail_id VARCHAR(255)
		)
		"""
	)
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS chat_history (
			user_id INTEGER,
			history TEXT,
			FOREIGN KEY(user_id) REFERENCES user_profile(user_id)
		)
		"""
	)
	conn.commit()

