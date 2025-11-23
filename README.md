# Zanvar's SQL Tool

## 🌟 Features

- **Multi-Database Query Execution**: Execute SQL queries across multiple databases simultaneously
- **Intuitive User Interface**: Modern, clean design with dark-themed result viewer
- **Query History Management**: Automatic saving and retrieval of executed queries
- **Real-time Results**: Stream results as they become available with formatted tabular display
- **Result Export**: Export query results to formatted text files
- **Non-blocking Operations**: Threading-based architecture ensures UI responsiveness
- **Comprehensive Error Handling**: Detailed error messages with graceful failure recovery
- **Keyboard Shortcuts**: Quick query execution with Ctrl+Enter
- **Connection Management**: Secure database authentication with connection testing

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- SQL Server 2012 or higher
- Windows, macOS, or Linux operating system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/zanvar-sql-tool.git
   cd zanvar-sql-tool
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Requirements

```txt
pyodbc>=4.0.30
pillow>=9.0.0
```

## 📖 Usage

### Connecting to SQL Server

1. Launch the application
2. Enter your SQL Server connection details:
   - **Server**: SQL Server instance name (e.g., `localhost` or `SERVER\INSTANCE`)
   - **Username**: SQL Server authentication username
   - **Password**: Your password
3. Click "Connect"

### Executing Queries

1. **Select databases**: Check the databases you want to query in the left panel
2. **Write query**: Type your SQL query in the editor (top-right panel)
3. **Execute**: Click "Execute Query" or press `Ctrl+Enter`
4. **View results**: Results appear in the bottom panel with execution summary

### Multi-Database Queries

```sql
-- This query will run on ALL selected databases
SELECT COUNT(*) as RecordCount FROM YourTable

-- Compare data across environments
SELECT DB_NAME() as Database, COUNT(*) as TableCount
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Execute Query |
| `Ctrl+A` | Select All Text |
| Double-click history | Load Previous Query |

## 🏗️ Project Structure

```
zanvar-sql-tool/
├── app/
│   ├── core/
│   │   ├── app_controller.py    # Main application controller
│   │   └── config.py             # Configuration constants
│   ├── database/
│   │   ├── connection.py         # Database connection manager
│   │   └── query_executor.py    # Query execution engine
│   ├── ui/
│   │   └── components/
│   │       ├── connection_ui.py  # Login interface
│   │       ├── main_ui.py        # Main application UI
│   │       ├── database_explorer.py  # Database selector
│   │       ├── query_editor.py   # SQL editor
│   │       └── result_viewer.py  # Results display
│   └── utils/
│       ├── query_history.py      # Query history management
│       ├── file_operations.py    # File I/O operations
│       └── validators.py         # Input validation
├── assets/
│   └── logo.png
├── main.py
├── requirements.txt
└── README.md
```

## 🔧 Architecture

The application follows a modular MVC-inspired architecture:

- **Controller Layer**: Manages application state and coordinates components
- **Database Layer**: Handles all SQL Server connectivity and query execution
- **UI Layer**: Tkinter-based user interface components
- **Utility Layer**: Support functions for history, validation, and file operations

### Threading Model

```
Main Thread (UI)  <--Message Queue-->  Worker Thread (Query Execution)
```

Queries execute in separate threads to maintain UI responsiveness, with results communicated via a thread-safe message queue.

## 🎯 Use Cases

- **Database Migration**: Validate data consistency across environments
- **Performance Benchmarking**: Compare query performance across databases
- **Schema Verification**: Check table structures and relationships
- **Multi-tenant Applications**: Query multiple tenant databases simultaneously
- **Routine Maintenance**: Execute maintenance scripts across database sets
- **Data Analysis**: Compare data across development, testing, and production


### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guidelines
- Add docstrings to all classes and methods
- Include unit tests for new features
- Update documentation as needed

## 🐛 Known Limitations

- Currently supports SQL Server only (MySQL/PostgreSQL support planned)
- Large result sets (>50,000 rows) may impact memory usage
- Complex stored procedures require careful handling
- Requires stable network connection for database operations

## 👥 Authors

**Team Members:**
- Shardul Prashant Mane (1022031140)
- Yash Ajay Kadav (23032006)
- Narayan Vishnu Sangale (23032012)
- Sakshi Jagannath Pawar (23032004)

**Supervisors:**
- Prof. P.B. More
- Mr. Sanam Tamboraji

**Institution:**
Department of Computer Science and Engineering  
Annasaheb Dange College of Engineering & Technology, Ashta, Sangli  
(Affiliated to Shivaji University, Kolhapur)

## 🙏 Acknowledgments

- Microsoft SQL Server team for comprehensive documentation
- Python community for excellent libraries and support
- Our mentors and colleagues for valuable feedback and guidance

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact the development team through the university

## 📊 Project Stats

- **Language**: Python
- **GUI Framework**: Tkinter
- **Database**: SQL Server (PyODBC)
- **Lines of Code**: ~3,000+
- **Development Time**: 6 months (Academic Year 2025-26)

---

**Note**: This project was developed as part of a B.Tech final year project in Computer Science and Engineering. It demonstrates practical application of database management, GUI design, threading, and software engineering principles.

Made with ❤️ by CSE Students at ADCET
