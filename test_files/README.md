# Test Files for Agentic Scheduler

This directory contains sample files for testing the file parsing functionality implemented in Sprint 2.

## 📁 Available Test Files

### 📊 Excel File (`sample_schedule.xlsx`)
- **Format**: Excel spreadsheet (.xlsx)
- **Content**: Sample class schedule with multiple events
- **Columns**: Title, Date, Start Time, End Time, Location, Type
- **Note**: You'll need to create this file manually using the data from `sample_schedule.csv`

### 📄 CSV File (`sample_schedule.csv`)
- **Format**: Comma-separated values (.csv)
- **Content**: Same data as the Excel file, can be opened in Excel
- **Use**: Open this in Excel and save as .xlsx for testing

### 📄 Text File for PDF Testing (`sample_schedule.txt`)
- **Format**: Plain text (.txt) - rename to .pdf for testing
- **Content**: Sample schedule text that can be parsed
- **Use**: Rename to `sample_schedule.pdf` and upload (will use text extraction)

## 🧪 How to Test File Upload

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Open the chat interface:**
   - Go to `http://localhost:8000/chat`
   - Or go to `http://localhost:8000` and click "Go to Chat"

3. **Upload a test file:**
   - Click "Choose File" next to "Upload Schedule"
   - Select one of the test files
   - Click "Upload Schedule"

4. **Expected Results:**
   - PDF/Text files: Should extract events from text patterns
   - Excel files: Should parse rows into calendar events
   - Images: Should use AI vision to extract schedule information

## 📋 Sample Data Structure

The test files contain events with the following structure:

| Title | Date | Start Time | End Time | Location | Type |
|-------|------|------------|----------|----------|------|
| Mathematics 101 | 2025-09-01 | 09:00 | 10:30 | Room 101 | class |
| Physics Lab | 2025-09-02 | 14:00 | 16:00 | Lab 205 | lab |
| Chemistry Lecture | 2025-09-03 | 11:00 | 12:00 | Auditorium A | class |

## 🔧 Creating Your Own Test Files

### Excel Format:
1. Open Excel or Google Sheets
2. Create columns: Title, Date, Start Time, End Time, Location, Type
3. Add your schedule data
4. Save as `.xlsx` file

### PDF Format:
1. Create a text document with schedule information
2. Use patterns like: "Class Name - Date - Location"
3. Save as PDF or upload as text file

### Image Format:
1. Take a photo or screenshot of a schedule
2. Save as PNG, JPG, or other supported format
3. The AI vision will attempt to extract the schedule

## 🎯 Expected Sprint 2 Behavior

- **File Validation**: Files are checked for type and size
- **Parsing**: Different parsers for PDF, Excel, and images
- **Calendar Integration**: Successfully parsed events are added to calendar
- **Error Handling**: Clear messages for parsing failures
- **Mock Implementation**: Current implementation uses mock responses

## 📝 Notes

- The current implementation (Sprint 2) uses mock calendar creation
- Real Google Calendar integration would require proper API setup
- Image parsing uses mock AI vision responses
- Full production implementation would be completed in later sprints

## 🐛 Troubleshooting

If upload fails:
1. Check file size (max 10MB)
2. Verify file extension is supported
3. Check browser console for errors
4. Verify all dependencies are installed
