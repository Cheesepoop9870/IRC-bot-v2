
import re
import time
import hashlib
import hmac
import secrets
import json
import logging as log
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class SecurityManager:
    def __init__(self):
        self.rate_limits = defaultdict(lambda: defaultdict(float))
        self.admin_sessions = {}
        self.failed_attempts = defaultdict(int)
        
        # Security flags - can be enabled/disabled
        self.flags = {
            'input_validation': True,
            'rate_limiting': True,
            'admin_authentication': True,
            'command_logging': True,
            'session_management': True,
            'anti_spam': True
        }
    
    def set_flag(self, flag_name: str, value: bool):
        """Enable or disable security features"""
        if flag_name in self.flags:
            self.flags[flag_name] = value
            log.info(f"Security flag {flag_name} set to {value}")
            return True
        return False
    
    def get_flags(self) -> Dict[str, bool]:
        """Get current security flag states"""
        return self.flags.copy()

class InputValidator:
    """Input validation with configurable rules"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        
        # Validation patterns
        self.patterns = {
            'channel': re.compile(r'^#[a-zA-Z0-9_-]{1,50}$'),
            'dice': re.compile(r'^\d{1,3}d\d{1,4}(\+\d{1,3})?$'),
            'command': re.compile(r'^[a-zA-Z0-9_-]{1,20}$'),
            'safe_string': re.compile(r'^[a-zA-Z0-9\s\-_.,!?]{1,500}$')
        }
        
        # Length limits
        self.limits = {
            'command': 500,
            'search_query': 200,
            'dice_notation': 20,
            'channel_name': 50,
            'general_input': 500
        }
    
    def validate_input(self, input_text: str, input_type: str = 'general') -> Tuple[bool, str]:
        """Validate input based on type"""
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        if not input_text:
            return False, "Empty input"
        
        # Length check
        max_length = self.limits.get(f'{input_type}_input', self.limits['general_input'])
        if len(input_text) > max_length:
            return False, f"Input too long (max {max_length} characters)"
        
        # Pattern validation
        if input_type in self.patterns:
            if not self.patterns[input_type].match(input_text):
                return False, f"Invalid {input_type} format"
        
        # SQL injection check
        if self._check_sql_injection(input_text):
            return False, "Potentially dangerous input detected"
        
        # XSS check
        if self._check_xss(input_text):
            return False, "Potentially dangerous script detected"
        
        return True, "Valid"
    
    def validate_command_args(self, args: List[str]) -> Tuple[bool, str]:
        """Validate command arguments"""
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        for arg in args:
            is_valid, message = self.validate_input(arg, 'general')
            if not is_valid:
                return False, message
        
        return True, "Valid"
    
    def validate_dice_notation(self, notation: str) -> Tuple[bool, str]:
        """Validate dice notation specifically"""
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        if not self.patterns['dice'].match(notation):
            return False, "Invalid dice notation format"
        
        # Check for reasonable limits
        try:
            if '+' in notation:
                dice_part, modifier = notation.split('+')
                modifier_val = int(modifier)
                if modifier_val > 100:
                    return False, "Modifier too large"
            else:
                dice_part = notation
            
            num_dice, sides = dice_part.split('d')
            num_dice, sides = int(num_dice), int(sides)
            
            if num_dice > 100 or sides > 1000:
                return False, "Dice parameters too large"
            
        except ValueError:
            return False, "Invalid dice notation"
        
        return True, "Valid"
    
    def _check_sql_injection(self, text: str) -> bool:
        """Check for SQL injection patterns"""
        sql_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)',
            r'(\b(UNION|JOIN)\b.*\b(SELECT)\b)',
            r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
            r'(--|#|/\*|\*/)',
            r'(\bEXEC\b|\bEXECUTE\b)'
        ]
        
        text_upper = text.upper()
        for pattern in sql_patterns:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True
        return False
    
    def _check_xss(self, text: str) -> bool:
        """Check for XSS patterns"""
        xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

class RateLimiter:
    """Rate limiting with configurable limits"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        self.user_commands = defaultdict(list)
        self.channel_commands = defaultdict(list)
        
        # Rate limits (commands per time period)
        self.limits = {
            'user_general': (10, 60),  # 10 commands per minute
            'user_expensive': (3, 60),  # 3 expensive commands per minute
            'channel_general': (30, 60),  # 30 commands per minute per channel
            'global_expensive': (10, 60)  # 10 expensive commands per minute globally
        }
        
        # Expensive commands that need special limiting
        self.expensive_commands = {'search', 'latest', 'author', 'google', 'youtube'}
    
    def check_rate_limit(self, user: str, channel: str, command: str) -> Tuple[bool, str]:
        """Check if user/channel has exceeded rate limits"""
        if not self.security.flags['rate_limiting']:
            return True, "Rate limiting disabled"
        
        current_time = time.time()
        
        # Clean old entries
        self._cleanup_old_entries(current_time)
        
        # Check user rate limits
        user_key = f"{user}:{command}"
        if command in self.expensive_commands:
            limit, window = self.limits['user_expensive']
        else:
            limit, window = self.limits['user_general']
        
        user_commands = self.user_commands[user_key]
        recent_commands = [t for t in user_commands if current_time - t < window]
        
        if len(recent_commands) >= limit:
            return False, f"Rate limit exceeded for user {user}"
        
        # Check channel rate limits
        channel_commands = self.channel_commands[channel]
        recent_channel_commands = [t for t in channel_commands if current_time - t < window]
        
        channel_limit, _ = self.limits['channel_general']
        if len(recent_channel_commands) >= channel_limit:
            return False, f"Rate limit exceeded for channel {channel}"
        
        # Record this command
        user_commands.append(current_time)
        channel_commands.append(current_time)
        
        return True, "Within rate limits"
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove old rate limit entries"""
        cutoff_time = current_time - 300  # 5 minutes
        
        for user_key in list(self.user_commands.keys()):
            self.user_commands[user_key] = [
                t for t in self.user_commands[user_key] if t > cutoff_time
            ]
            if not self.user_commands[user_key]:
                del self.user_commands[user_key]
        
        for channel in list(self.channel_commands.keys()):
            self.channel_commands[channel] = [
                t for t in self.channel_commands[channel] if t > cutoff_time
            ]
            if not self.channel_commands[channel]:
                del self.channel_commands[channel]

class AdminAuthenticator:
    """Enhanced admin authentication with sessions and tokens"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        self.sessions = {}
        self.admin_tokens = {}
        self.failed_attempts = defaultdict(int)
        
        # Session timeout (30 minutes)
        self.session_timeout = 1800
        
        # Load admin patterns and users from environment
        import os
        self.admin_users = set(os.getenv('ADMIN_USERS_LIST', '').split(','))
        self.admin_regex_patterns = self._load_admin_patterns()
    
    def _load_admin_patterns(self) -> List[str]:
        """Load admin regex patterns from environment"""
        import os
        try:
            patterns_json = os.getenv('ADMIN_REGEX_PATTERNS', '[]')
            return json.loads(patterns_json)
        except json.JSONDecodeError:
            log.warning("Failed to load admin regex patterns from environment")
            return []
    
    def verify_admin(self, username: str, full_host: str) -> Tuple[bool, str]:
        """Verify admin privileges with enhanced security"""
        if not self.security.flags['admin_authentication']:
            # Fallback to basic check if disabled
            return self._basic_admin_check(username, full_host)
        
        # Check failed attempts
        if self.failed_attempts[username] >= 3:
            return False, "Too many failed attempts"
        
        # Check username whitelist
        if username not in self.admin_users:
            self.failed_attempts[username] += 1
            return False, "User not in admin list"
        
        # Check regex patterns
        is_regex_match = False
        for pattern in self.admin_regex_patterns:
            try:
                if re.search(pattern, full_host):
                    is_regex_match = True
                    break
            except re.error:
                log.warning(f"Invalid regex pattern: {pattern}")
        
        if not is_regex_match:
            self.failed_attempts[username] += 1
            return False, "Host pattern does not match"
        
        # Reset failed attempts on success
        self.failed_attempts[username] = 0
        return True, "Admin verified"
    
    def create_admin_session(self, username: str) -> str:
        """Create admin session with token"""
        if not self.security.flags['session_management']:
            return "session_disabled"
        
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            'username': username,
            'created': time.time(),
            'last_activity': time.time()
        }
        return session_token
    
    def verify_admin_session(self, session_token: str) -> Tuple[bool, str]:
        """Verify admin session is valid"""
        if not self.security.flags['session_management']:
            return True, "Session management disabled"
        
        if session_token not in self.sessions:
            return False, "Invalid session"
        
        session = self.sessions[session_token]
        current_time = time.time()
        
        # Check timeout
        if current_time - session['last_activity'] > self.session_timeout:
            del self.sessions[session_token]
            return False, "Session expired"
        
        # Update last activity
        session['last_activity'] = current_time
        return True, "Session valid"
    
    def _basic_admin_check(self, username: str, full_host: str) -> Tuple[bool, str]:
        """Basic admin check for fallback"""
        # This is the original logic from main.py
        admin_users = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", 
                      "The_Fox_Empress", "Felds", "PineappleOnSleepza", "my.poop.is.cheese", 
                      "illegal.food.combo", "stalking.your.sandbox", "site19.isnt.real.cant.hurt.you", 
                      "the.queen.of.foxes", "Magnileak"}
        
        if username in admin_users:
            return True, "Basic admin check passed"
        return False, "Not an admin user"

class SecurityAuditor:
    """Security event logging and monitoring"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
    
    def log_security_event(self, event_type: str, user: str, channel: str, details: str):
        """Log security events"""
        if not self.security.flags['command_logging']:
            return
        
        log.warning(f"SECURITY EVENT - {event_type}: User {user} in {channel} - {details}")
    
    def log_failed_auth(self, user: str, host: str, reason: str):
        """Log failed authentication attempts"""
        self.log_security_event("AUTH_FAILURE", user, "N/A", f"Host: {host}, Reason: {reason}")
    
    def log_rate_limit_violation(self, user: str, channel: str, command: str):
        """Log rate limit violations"""
        self.log_security_event("RATE_LIMIT", user, channel, f"Command: {command}")
    
    def log_input_validation_failure(self, user: str, channel: str, input_data: str, reason: str):
        """Log input validation failures"""
        self.log_security_event("INPUT_VALIDATION", user, channel, f"Input: {input_data[:50]}..., Reason: {reason}")

# Initialize security components
security_manager = SecurityManager()
input_validator = InputValidator(security_manager)
rate_limiter = RateLimiter(security_manager)
admin_authenticator = AdminAuthenticator(security_manager)
security_auditor = SecurityAuditor(security_manager)

def get_security_manager():
    """Get the global security manager instance"""
    return security_manager
