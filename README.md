# dependency
---
- structlog==21.2.0 (2021г.)
- aiologger==0.7.0
- graypy==2.1.0

# How does work?
![Schema](/schema.png)
```
@startuml
Client -> structlog : logger.debug(Message)
structlog -> asynclogger.Adapter : structlog.BoundLogger._proxy_to_logger()
asynclogger.Adapter -> aiologger : aiologger.debug()
aiologger -> asynclogger.ConsoleHandler : aiologger.AsyncStreamHandler
aiologger -> asyncloggerGraylogHandler : aiologger.Handler
@enduml
```
# How to use?

### Setting variables
```.env```
```
LOGGER_CONSOLE=True  # Enable console output
LOGGER_CONSOLE_LEVEL=DEBUG # Level of displayed logs

LOGGER_GRAYLOG=True # Enable output in Graylog
LOGGER_GRAYLOG_LEVEL=DEBUG
LOGGER_GRAYLOG_HOST=localhost
LOGGER_GRAYLOG_PORT=12201
```

### Connecting in project
```
from asynclogger import add_handler
from asynclogger import console_handler
from asynclogger import get_logger
from asynclogger import graylog_handler

from ... import config

if config.LOGGER_CONSOLE:
    add_handler(console_handler(level=config.LOGGER_CONSOLE_LEVEL))

if config.LOGGER_GRAYLOG:
    add_handler(
        graylog_handler(
            host=config.LOGGER_GRAYLOG_HOST,
            port=config.LOGGER_GRAYLOG_PORT,
            level=config.LOGGER_GRAYLOG_LEVEL,
        )
    )


logger = get_logger()

await logger.debug("Debug")
>>> 2023-06-09T08:36:20.601568 DEBUG: Debug
```

### feature ```Field```

```
from asynclogger.fields import Field

logger = get_logger()

await logger.debug("Debug", Field.levelname("DEBUG"))
>>> 2023-06-09T08:44:07.261025 DEBUG: Debug levelname=DEBUG
```
### Displaying specific fields

```
from asynclogger.fields import Field

add_handler(
        console_handler(
            level=LOGGER_CONSOLE_LEVEL,
            fields=[Field.levelname, Field.timestamp, Field.event, 'include']
        )
    )

logger = get_logger()

await logger.debug("Debug", include="Include Field", other="Other")
>>> 2023-06-09T08:42:14.447572 DEBUG: Debug include=Invclude Field
```

### Setting the order, format, and color scheme for display

#### Priority override
```
from asynclogger.fields import FIELDS_SETTINGS, Field

await logger.debug("Debug")
 >>> 2023-06-09T08:42:14.447572 DEBUG: Debug
 
FIELDS_SETTINGS[Field.levelname]["priority"] = 0
FIELDS_SETTINGS[Field.timestamp]["priority"] = 1

await logger.debug("Debug")
 >>> DEBUG: 2023-06-09T08:42:14.447572 Debug
```

#### Format override
```
from asynclogger.fields import FIELDS_SETTINGS, Field

await logger.debug("Debug")
 >>> 2023-06-09T08:42:14.447572 DEBUG: Debug
 
FIELDS_SETTINGS[Field.LevelName] = dict(
    priority=1,
    template=lambda method, key, value: f"{structlog.dev.BRIGHT} || {value} ||"
)

await logger.debug("Debug")
 >>> 2023-06-09T08:42:14.447572 || DEBUG || Debug
```
