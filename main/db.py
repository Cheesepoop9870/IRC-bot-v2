import sqlite3
import logging as log
from contextlib import contextmanager
from typing import List, Optional, Tuple, Any
import os

class DatabaseManager:
    """A functional database manager for SQLite operations"""

    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the database with required tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Create channels table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS channels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Create logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        log TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                conn.commit()
                log.info("Database initialized successfully")

        except sqlite3.Error as e:
            log.error(f"Error initializing database: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            log.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    # Channel management methods
    def add_channel(self, channel: str) -> bool:
        """Add a channel to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR IGNORE INTO channels (channel) VALUES (?)", (channel,))
                conn.commit()

                if cursor.rowcount > 0:
                    log.info(f"Added channel: {channel}")
                    return True
                else:
                    log.info(f"Channel already exists: {channel}")
                    return False

        except sqlite3.Error as e:
            log.error(f"Error adding channel {channel}: {e}")
            return False

    def del_channel(self, channel: str) -> bool:
        """Delete a channel from the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM channels WHERE channel = ?", (channel,))
                conn.commit()

                if cursor.rowcount > 0:
                    log.info(f"Deleted channel: {channel}")
                    return True
                else:
                    log.info(f"Channel not found: {channel}")
                    return False

        except sqlite3.Error as e:
            log.error(f"Error deleting channel {channel}: {e}")
            return False

    def get_channels(self) -> List[str]:
        """Get all channels from the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT channel FROM channels ORDER BY channel")
                rows = cursor.fetchall()
                channels = [row['channel'] for row in rows]
                log.debug(f"Retrieved {len(channels)} channels")
                return channels

        except sqlite3.Error as e:
            log.error(f"Error getting channels: {e}")
            return []

    def channel_exists(self, channel: str) -> bool:
        """Check if a channel exists in the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM channels WHERE channel = ? LIMIT 1", (channel,))
                return cursor.fetchone() is not None

        except sqlite3.Error as e:
            log.error(f"Error checking channel existence {channel}: {e}")
            return False

    def get_channel_count(self) -> int:
        """Get the total number of channels"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM channels")
                result = cursor.fetchone()
                return result['count'] if result else 0

        except sqlite3.Error as e:
            log.error(f"Error getting channel count: {e}")
            return 0

    # Log management methods
    def add_log(self, log_entry: str) -> bool:
        """Add a log entry to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO logs (log) VALUES (?)", (log_entry,))
                conn.commit()
                log.debug(f"Added log entry")
                return True

        except sqlite3.Error as e:
            log.error(f"Error adding log entry: {e}")
            return False

    def del_log(self, log_entry: str) -> bool:
        """Delete a log entry from the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM logs WHERE log = ?", (log_entry,))
                conn.commit()

                if cursor.rowcount > 0:
                    log.info(f"Deleted log entry")
                    return True
                else:
                    log.info(f"Log entry not found")
                    return False

        except sqlite3.Error as e:
            log.error(f"Error deleting log entry: {e}")
            return False

    def get_logs(self, limit: Optional[int] = None) -> List[Tuple[str, str]]:
        """Get log entries from the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if limit:
                    cursor.execute("SELECT log, created_at FROM logs ORDER BY created_at DESC LIMIT ?", (limit,))
                else:
                    cursor.execute("SELECT log, created_at FROM logs ORDER BY created_at DESC")

                rows = cursor.fetchall()
                logs = [(row['log'], row['created_at']) for row in rows]
                log.debug(f"Retrieved {len(logs)} log entries")
                return logs

        except sqlite3.Error as e:
            log.error(f"Error getting logs: {e}")
            return []

    def clear_logs(self) -> bool:
        """Clear all log entries"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM logs")
                deleted_count = cursor.rowcount
                conn.commit()
                log.info(f"Cleared {deleted_count} log entries")
                return True

        except sqlite3.Error as e:
            log.error(f"Error clearing logs: {e}")
            return False

    # General utility methods
    def full_delete(self) -> bool:
        """Delete all channels (keeping the table structure)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM channels")
                deleted_count = cursor.rowcount
                conn.commit()
                log.info(f"Deleted all {deleted_count} channels")
                return True

        except sqlite3.Error as e:
            log.error(f"Error during full delete: {e}")
            return False

    def get_database_info(self) -> dict:
        """Get general information about the database"""
        try:
            info = {
                'database_path': self.db_path,
                'database_exists': os.path.exists(self.db_path),
                'channel_count': self.get_channel_count(),
                'log_count': len(self.get_logs())
            }

            if info['database_exists']:
                info['database_size'] = os.path.getsize(self.db_path)

            return info

        except Exception as e:
            log.error(f"Error getting database info: {e}")
            return {}

    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            log.info(f"Database backed up to {backup_path}")
            return True

        except Exception as e:
            log.error(f"Error backing up database: {e}")
            return False

# Global database instance
db = DatabaseManager()

# Legacy function compatibility (for existing code)
def add_channel(channel):
    return db.add_channel(channel)

def full_delete():
    return db.full_delete()

def get_channels():
    return db.get_channels()

def del_channel(args):
    return db.del_channel(args)

def add_log(log_entry):
    return db.add_log(log_entry)

def del_log(args):
    return db.del_log(args)

if __name__ == "__main__":
    # Example usage and testing
    print("Database Manager Test")
    print("=" * 30)

    # Test channel operations
    print("Testing channel operations...")
    db.add_channel("#cheesepoop9870")
    db.add_channel("#facility36")
    db.add_channel("#testchannel")

    channels = db.get_channels()
    print(f"Channels: {channels}")
    print(f"Channel count: {db.get_channel_count()}")

    # Test log operations
    print("\nTesting log operations...")
    db.add_log("Bot started")
    db.add_log("Connected to IRC")
    db.add_log("Joined channels")

    logs = db.get_logs(limit=5)
    print(f"Recent logs: {logs}")

    # Database info
    print("\nDatabase information:")
    info = db.get_database_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    print("\nTest completed!")