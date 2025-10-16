# from googlesearch import search
# print(list(search("Google", advanced=True)))
import logging

# 1. Define the custom level
logging.VERBOSE = 15

# 2. Associate the name with the level
logging.addLevelName(logging.VERBOSE, "VERBOSE")

# 3. Add a convenience method (optional)
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.VERBOSE):
        self._log(logging.VERBOSE, message, args, **kwargs)

logging.Logger.verbose = verbose

# Configure basic logging
logging.basicConfig(
  level=logging.DEBUG,  
  format='[%(asctime)s,%(msecs)d] [%(levelname)s]: %(message)s',
  filename='test.log',  # Log to a file named 'app.log'
  filemode='w',         # Append to the file (default is 'a', 'w' for overwrite)
  datefmt='%H:%M:%S',
)
# Get a logger instance
logger = logging.getLogger(__name__)

# Use the custom level
logger.debug("This is a DEBUG message.")
logger.verbose("This is a VERBOSE message.")
logger.info("This is an INFO message.")