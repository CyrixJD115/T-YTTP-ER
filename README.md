# T(YTTP)ER - YouTube Transcript Processor

## Overview
**T(YTTP)ER** (pronounced "Typer") is a complete revamp of [YTTP-AI](https://github.com/CyrixJD115/YTTP-AI), rebuilt from the ground up with PySide6 for a smoother, faster experience. This application maintains all the powerful features of the original while delivering noticeable performance improvements and a more polished interface.

Key enhancements:
- ⚡ **Smoother performance** with PySide6 interface
- ✍️ **Improved typewriter effect** for better readability
- 📜 **New History feature** for tracking processed videos
- 🎨 **Refined modern UI** with cleaner design
- 🚀 **Optimized processing pipeline** for faster results

## Requirements

### Software Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- Ollama model of your choice (recommended: `llama3.2` or `deepseek-r1`)

### Hardware Recommendations
For optimal performance:
- **CPU**: Intel i5/Ryzen 5 or better
- **RAM**: 8GB+ (16GB recommended)
- **GPU**: 4GB+ VRAM
- **Storage**: SSD with 100MB free space

For `llama3.2` model:
- Minimum: 4GB RAM + 2GB VRAM
- Recommended: 8GB RAM + 4GB VRAM

## Installation & Setup

1. **Install Ollama**:
   - Download from https://ollama.com/download
   - Launch and keep running in background

2. **Download model**:
   ```bash
   ollama pull llama3.2  # Optimal balance of speed/quality
   ```

3. **Launch T(YTTP)ER**:
   ```bash
   python Start_tyttper.py
   ```

The application will:
- Auto-install Python dependencies
- Configure optimized defaults
- Prepare processing environment

## Key Features

### 🆕 History System
- Track previously processed videos
- Quick access to past sessions
- Organized workflow management

### ✨ Enhanced Processing
- Optimized text chunk handling
- Smoother typewriter animation
- Improved memory management

### 🎛️ Modern Interface
- Professional PySide6 framework
- Responsive and polished UI
- Intuitive navigation

## Quick Start Guide

1. **Launch the application**:
   ```bash
   python Start_tyttper.py
   ```

2. **Process videos**:
   1. Enter YouTube URL in Start screen
   2. Monitor real-time AI processing
   3. Access history via new menu

3. **Workflow**:
   - Simplified interface
   - Focused functionality

## Performance Tips

### Recommended Configurations
| Hardware Profile       | Model       | Chunk Size | Overlap |
|------------------------|-------------|------------|---------|
| Basic (4GB RAM)        | llama3.2    | 250 words  | 30      |
| Balanced (8GB RAM)     | deepseek-r1 | 400 words  | 50      |
| Advanced (16GB+ RAM)   | llama3      | 700 words  | 75      |

### Optimization Tips
- Use smaller models for faster processing
- Adjust chunk size based on RAM
- Close other applications during processing

## Troubleshooting

### Common Solutions
1. **Transcript issues**:
   - Verify video has captions
   - Try different video URL format

2. **Performance tuning**:
   - Reduce chunk size
   - Use llama3.2 model
   - Restart application periodically

3. **Ollama connection**:
   - Ensure Ollama is running
   - Check `ollama serve` status

### Temporary Files
The application automatically clears temporary files. Manual cleanup:
```bash
rm -rf temp/
```
Or simply delete the folder

## Why Choose T(YTTP)ER?

### Improvements Over Previous Version
- **Modern interface**: PySide6 vs Tkinter
- **History feature**: Track processed videos
- **Performance**: Optimized processing pipeline
- **Typewriter effect**: Smoother text display

## Contribution
We welcome contributions:
- Bug reports
- UI improvements
- Documentation updates
- Performance optimizations

## License
MIT License - see [LICENSE](LICENSE) for details.

---

**Note**: This application uses YouTube's public API. Please respect content creators' rights and adhere to YouTube's Terms of Service.
