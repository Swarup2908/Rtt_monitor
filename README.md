# RTT Monitor

A Python-based application for monitoring Round Trip Time (RTT) values from different URL endpoints using Celery for distributed task processing.

## Description

RTT Monitor is a lightweight monitoring tool that tracks the response times of various web endpoints. It leverages Celery for asynchronous task execution, allowing you to monitor multiple URLs concurrently without blocking operations.

## Features

- Monitor RTT values from multiple URL endpoints
- Asynchronous processing with Celery
- Easy setup and configuration
- Real-time monitoring capabilities
- Scalable architecture for handling multiple endpoints

## Requirements

- Python 3.7+
- Celery
- Redis or RabbitMQ (message broker for Celery)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Swarup2908/Rtt_monitor.git
cd Rtt_monitor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Redis server** (if using Redis as message broker):
```bash
redis-server
```

2. **Start the application server**:
```bash
python manage.py runserver
```

3. **Start Celery worker** (in a new terminal):
```bash
celery -A rtt_monitor worker --loglevel=info
```

4. **Start Celery beat scheduler** (optional, for periodic tasks):
```bash
celery -A rtt_monitor beat --loglevel=info
```

## Configuration

- Configure your target URLs in the application settings
- Adjust monitoring intervals as needed
- Set up your preferred message broker (Redis/RabbitMQ)


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Author**: Swarup2908  
**Repository**: https://github.com/Swarup2908/Rtt_monitor
