
"""
Security Module for IRC Bot

This module provides comprehensive security features including:
- Input validation and sanitization
- Rate limiting for commands and users
- Enhanced admin authentication with sessions
- Security event logging and monitoring
- Configurable security flags to enable/disable features

Usage:
    from security import security_manager, input_validator, rate_limiter, admin_authenticator, security_auditor
    
    # Check if input is valid
    is_valid, message = input_validator.validate_input(user_input, "command")
    
    # Check rate limits
    allowed, message = rate_limiter.check_rate_limit(username, channel, command)
    
    # Verify admin privileges
    is_admin, message = admin_authenticator.verify_admin(username, host)
    
    # Log security events
    security_auditor.log_security_event("EVENT_TYPE", user, channel, details)
"""

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
    """
    Central security manager that controls all security features through flags.
    
    This class manages security feature toggles, allowing you to enable or disable
    specific security components without changing code.
    
    Usage:
        # Create security manager (done automatically at module level)
        security = SecurityManager()
        
        # Enable/disable features
        security.set_flag('input_validation', True)
        security.set_flag('rate_limiting', False)
        
        # Check current flags
        current_flags = security.get_flags()
    """
    
    def __init__(self):
        # Rate limit tracking for users and channels
        self.rate_limits = defaultdict(lambda: defaultdict(float))
        # Active admin sessions
        self.admin_sessions = {}
        # Failed authentication attempts per user
        self.failed_attempts = defaultdict(int)
        
        # Security flags - can be enabled/disabled to control features
        # Set these to False to disable specific security features
        self.flags = {
            'input_validation': True,      # Validate all user inputs
            'rate_limiting': True,         # Limit command frequency
            'admin_authentication': True,  # Enhanced admin verification
            'command_logging': True,       # Log security events
            'session_management': True,    # Admin session tokens
            'anti_spam': True             # Anti-spam measures
        }
    
    def set_flag(self, flag_name: str, value: bool):
        """
        Enable or disable security features dynamically.
        
        Args:
            flag_name (str): Name of the security flag
            value (bool): True to enable, False to disable
            
        Returns:
            bool: True if flag was set successfully, False if flag doesn't exist
            
        Example:
            security_manager.set_flag('rate_limiting', False)  # Disable rate limiting
            security_manager.set_flag('input_validation', True)  # Enable input validation
        """
        if flag_name in self.flags:
            self.flags[flag_name] = value
            log.info(f"Security flag {flag_name} set to {value}")
            return True
        return False
    
    def get_flags(self) -> Dict[str, bool]:
        """
        Get current security flag states.
        
        Returns:
            Dict[str, bool]: Copy of current flag states
            
        Example:
            flags = security_manager.get_flags()
            print(f"Input validation: {flags['input_validation']}")
        """
        return self.flags.copy()

class InputValidator:
    """
    Input validation with configurable rules and patterns.
    
    This class validates user inputs to prevent injection attacks, oversized inputs,
    and malformed data. It can be disabled via security flags.
    
    Usage:
        # Validate general input
        is_valid, message = input_validator.validate_input("user input", "general")
        
        # Validate specific types
        is_valid, message = input_validator.validate_dice_notation("2d6+3")
        is_valid, message = input_validator.validate_command_args(["arg1", "arg2"])
    """
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        
        # Regex patterns for different input types
        # Add new patterns here for additional input types
        self.patterns = {
            'channel': re.compile(r'^#[a-zA-Z0-9_-]{1,50}$'),      # IRC channel format
            'dice': re.compile(r'^\d{1,3}d\d{1,4}(\+\d{1,3})?$'),  # Dice notation (e.g., 2d6+3)
            'command': re.compile(r'^[a-zA-Z0-9_-]{1,20}$'),       # Command names
            'safe_string': re.compile(r'^[a-zA-Z0-9\s\-_.,!?]{1,500}$')  # General safe text
        }
        
        # Maximum length limits for different input types
        # Adjust these values based on your needs
        self.limits = {
            'command': 500,        # IRC command length
            'search_query': 200,   # Search query length
            'dice_notation': 20,   # Dice notation length
            'channel_name': 50,    # Channel name length
            'general_input': 500   # Default input length
        }
    
    def validate_input(self, input_text: str, input_type: str = 'general') -> Tuple[bool, str]:
        """
        Validate input based on type and security rules.
        
        Args:
            input_text (str): The text to validate
            input_type (str): Type of input ('general', 'channel', 'command', etc.)
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
            
        Example:
            # Validate a channel name
            is_valid, msg = validator.validate_input("#mychannel", "channel")
            if not is_valid:
                print(f"Invalid channel: {msg}")
        """
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        if not input_text:
            return False, "Empty input"
        
        # Check length limits
        max_length = self.limits.get(f'{input_type}_input', self.limits['general_input'])
        if len(input_text) > max_length:
            return False, f"Input too long (max {max_length} characters)"
        
        # Check against regex patterns
        if input_type in self.patterns:
            if not self.patterns[input_type].match(input_text):
                return False, f"Invalid {input_type} format"
        
        # Security checks
        if self._check_sql_injection(input_text):
            return False, "Potentially dangerous input detected"
        
        if self._check_xss(input_text):
            return False, "Potentially dangerous script detected"
        
        return True, "Valid"
    
    def validate_command_args(self, args: List[str]) -> Tuple[bool, str]:
        """
        Validate a list of command arguments.
        
        Args:
            args (List[str]): List of command arguments to validate
            
        Returns:
            Tuple[bool, str]: (all_valid, error_message)
            
        Example:
            args = ["search", "SCP-173"]
            is_valid, msg = validator.validate_command_args(args)
        """
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        for arg in args:
            is_valid, message = self.validate_input(arg, 'general')
            if not is_valid:
                return False, message
        
        return True, "Valid"
    
    def validate_dice_notation(self, notation: str) -> Tuple[bool, str]:
        """
        Validate dice notation specifically (e.g., "2d6+3", "1d20").
        
        Args:
            notation (str): Dice notation string
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
            
        Example:
            is_valid, msg = validator.validate_dice_notation("2d6+3")
            if is_valid:
                # Proceed with dice roll
                pass
        """
        if not self.security.flags['input_validation']:
            return True, "Validation disabled"
        
        if not self.patterns['dice'].match(notation):
            return False, "Invalid dice notation format"
        
        # Check for reasonable limits to prevent abuse
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
            
            # Prevent excessive dice rolls that could cause performance issues
            if num_dice > 100 or sides > 1000:
                return False, "Dice parameters too large"
            
        except ValueError:
            return False, "Invalid dice notation"
        
        return True, "Valid"
    
    def _check_sql_injection(self, text: str) -> bool:
        """
        Check for common SQL injection patterns.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if potential SQL injection detected
        """
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
        """
        Check for common XSS (Cross-Site Scripting) patterns.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if potential XSS detected
        """
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
    """
    Rate limiting with configurable limits for users and channels.
    
    This class prevents spam and abuse by limiting how frequently users can
    execute commands. Different limits apply to regular vs expensive commands.
    
    Usage:
        # Check if user can execute command
        allowed, message = rate_limiter.check_rate_limit("username", "#channel", "search")
        if not allowed:
            send_message(channel, f"Rate limited: {message}")
            return
    """
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        # Track command timestamps per user
        self.user_commands = defaultdict(list)
        # Track command timestamps per channel
        self.channel_commands = defaultdict(list)
        
        # Rate limits configuration (commands_allowed, time_window_seconds)
        # Adjust these values based on your bot's needs
        self.limits = {
            'user_general': (10, 60),    # 10 commands per minute per user
            'user_expensive': (3, 60),   # 3 expensive commands per minute per user
            'channel_general': (30, 60), # 30 commands per minute per channel
            'global_expensive': (10, 60) # 10 expensive commands per minute globally
        }
        
        # Commands that are considered "expensive" and need stricter limits
        # Add command names here that should have stricter rate limiting
        self.expensive_commands = {'search', 'latest', 'author', 'google', 'youtube'}
    
    def check_rate_limit(self, user: str, channel: str, command: str) -> Tuple[bool, str]:
        """
        Check if user/channel has exceeded rate limits for the given command.
        
        Args:
            user (str): Username executing the command
            channel (str): Channel where command is executed
            command (str): Command being executed
            
        Returns:
            Tuple[bool, str]: (is_allowed, reason_if_denied)
            
        Example:
            allowed, msg = rate_limiter.check_rate_limit("user123", "#general", "search")
            if not allowed:
                print(f"Rate limit exceeded: {msg}")
        """
        if not self.security.flags['rate_limiting']:
            return True, "Rate limiting disabled"
        
        current_time = time.time()
        
        # Clean up old entries to prevent memory buildup
        self._cleanup_old_entries(current_time)
        
        # Determine rate limit based on command type
        user_key = f"{user}:{command}"
        if command in self.expensive_commands:
            limit, window = self.limits['user_expensive']
        else:
            limit, window = self.limits['user_general']
        
        # Check user-specific rate limits
        user_commands = self.user_commands[user_key]
        recent_commands = [t for t in user_commands if current_time - t < window]
        
        if len(recent_commands) >= limit:
            return False, f"Rate limit exceeded for user {user}"
        
        # Check channel-specific rate limits
        channel_commands = self.channel_commands[channel]
        recent_channel_commands = [t for t in channel_commands if current_time - t < window]
        
        channel_limit, _ = self.limits['channel_general']
        if len(recent_channel_commands) >= channel_limit:
            return False, f"Rate limit exceeded for channel {channel}"
        
        # Record this command execution
        user_commands.append(current_time)
        channel_commands.append(current_time)
        
        return True, "Within rate limits"
    
    def _cleanup_old_entries(self, current_time: float):
        """
        Remove old rate limit entries to prevent memory buildup.
        Called automatically by check_rate_limit().
        
        Args:
            current_time (float): Current timestamp
        """
        cutoff_time = current_time - 300  # Keep 5 minutes of history
        
        # Clean user command history
        for user_key in list(self.user_commands.keys()):
            self.user_commands[user_key] = [
                t for t in self.user_commands[user_key] if t > cutoff_time
            ]
            if not self.user_commands[user_key]:
                del self.user_commands[user_key]
        
        # Clean channel command history
        for channel in list(self.channel_commands.keys()):
            self.channel_commands[channel] = [
                t for t in self.channel_commands[channel] if t > cutoff_time
            ]
            if not self.channel_commands[channel]:
                del self.channel_commands[channel]

class AdminAuthenticator:
    """
    Enhanced admin authentication with sessions and tokens.
    
    This class provides secure admin verification using multiple methods:
    - Username whitelist checking
    - Regex pattern matching for hostnames
    - Session token management
    - Failed attempt tracking
    
    Setup:
        Set these environment variables in Replit Secrets:
        - ADMIN_USERS_LIST: comma-separated list of admin usernames
        - ADMIN_REGEX_PATTERNS: JSON array of regex patterns for hostname matching
        
    Usage:
        # Verify admin privileges
        is_admin, msg = admin_authenticator.verify_admin("username", "full_hostname")
        
        # Create admin session
        if is_admin:
            session_token = admin_authenticator.create_admin_session("username")
            
        # Later, verify session
        is_valid, msg = admin_authenticator.verify_admin_session(session_token)
    """
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        # Active admin sessions {token: session_info}
        self.sessions = {}
        # Admin tokens for additional security
        self.admin_tokens = {}
        # Failed authentication attempts per user
        self.failed_attempts = defaultdict(int)
        
        # Session timeout in seconds (30 minutes)
        self.session_timeout = 1800
        
        # Load admin configuration from environment variables
        import os
        admin_list = os.getenv('ADMIN_USERS_LIST', '')
        self.admin_users = set(admin_list.split(',')) if admin_list else set()
        self.admin_regex_patterns = self._load_admin_patterns()
    
    def _load_admin_patterns(self) -> List[str]:
        """
        Load admin regex patterns from ADMIN_REGEX_PATTERNS environment variable.
        
        Expected format: JSON array of regex pattern strings
        Example: ["pattern1", "pattern2"]
        
        Returns:
            List[str]: List of regex patterns
        """
        import os
        try:
            patterns_json = os.getenv('ADMIN_REGEX_PATTERNS', '[]')
            return json.loads(patterns_json)
        except json.JSONDecodeError:
            log.warning("Failed to load admin regex patterns from environment")
            return []
    
    def verify_admin(self, username: str, full_host: str) -> Tuple[bool, str]:
        """
        Verify admin privileges with enhanced security checks.
        
        Args:
            username (str): Username to verify
            full_host (str): Full hostname/hostmask from IRC
            
        Returns:
            Tuple[bool, str]: (is_admin, verification_message)
            
        Example:
            is_admin, msg = admin_authenticator.verify_admin("admin_user", "user@host.com")
            if is_admin:
                # Allow admin command
                pass
            else:
                log.warning(f"Admin verification failed: {msg}")
        """
        if not self.security.flags['admin_authentication']:
            # Fallback to basic check if enhanced auth is disabled
            return self._basic_admin_check(username, full_host)
        
        # Check for too many failed attempts (simple brute force protection)
        if self.failed_attempts[username] >= 3:
            return False, "Too many failed attempts"
        
        # Check if username is in admin whitelist
        if username not in self.admin_users:
            self.failed_attempts[username] += 1
            return False, "User not in admin list"
        
        # Check hostname against regex patterns
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
        
        # Success - reset failed attempts
        self.failed_attempts[username] = 0
        return True, "Admin verified"
    
    def create_admin_session(self, username: str) -> str:
        """
        Create an admin session with a secure token.
        
        Args:
            username (str): Admin username
            
        Returns:
            str: Session token (use this for subsequent session verification)
            
        Example:
            if admin_verified:
                session_token = admin_authenticator.create_admin_session("admin_user")
                # Store session_token for this user's commands
        """
        if not self.security.flags['session_management']:
            return "session_disabled"
        
        # Generate cryptographically secure token
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            'username': username,
            'created': time.time(),
            'last_activity': time.time()
        }
        return session_token
    
    def verify_admin_session(self, session_token: str) -> Tuple[bool, str]:
        """
        Verify that an admin session token is valid and not expired.
        
        Args:
            session_token (str): Token returned by create_admin_session()
            
        Returns:
            Tuple[bool, str]: (is_valid, status_message)
            
        Example:
            is_valid, msg = admin_authenticator.verify_admin_session(stored_token)
            if is_valid:
                # Allow admin command
                pass
            else:
                # Re-authenticate required
                pass
        """
        if not self.security.flags['session_management']:
            return True, "Session management disabled"
        
        if session_token not in self.sessions:
            return False, "Invalid session"
        
        session = self.sessions[session_token]
        current_time = time.time()
        
        # Check if session has expired
        if current_time - session['last_activity'] > self.session_timeout:
            del self.sessions[session_token]
            return False, "Session expired"
        
        # Update last activity time
        session['last_activity'] = current_time
        return True, "Session valid"
    
    def _basic_admin_check(self, username: str, full_host: str) -> Tuple[bool, str]:
        """
        Basic admin check for fallback when enhanced auth is disabled.
        Uses the original hardcoded admin list from main.py.
        
        Args:
            username (str): Username to check
            full_host (str): Full hostname (unused in basic check)
            
        Returns:
            Tuple[bool, str]: (is_admin, status_message)
        """
        # Original admin users from main.py (hardcoded fallback)
        admin_users = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", 
                      "The_Fox_Empress", "Felds", "PineappleOnSleepza", "my.poop.is.cheese", 
                      "illegal.food.combo", "stalking.your.sandbox", "site19.isnt.real.cant.hurt.you", 
                      "the.queen.of.foxes", "Magnileak"}
        
        if username in admin_users:
            return True, "Basic admin check passed"
        return False, "Not an admin user"

class SecurityAuditor:
    """
    Security event logging and monitoring.
    
    This class provides centralized logging for security events, making it easier
    to monitor for abuse, attacks, and suspicious activity.
    
    Usage:
        # Log general security events
        security_auditor.log_security_event("LOGIN_ATTEMPT", "user", "#channel", "details")
        
        # Log specific event types
        security_auditor.log_failed_auth("user", "host", "reason")
        security_auditor.log_rate_limit_violation("user", "#channel", "command")
        security_auditor.log_input_validation_failure("user", "#channel", "bad_input", "reason")
    """
    
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
    
    def log_security_event(self, event_type: str, user: str, channel: str, details: str):
        """
        Log a general security event.
        
        Args:
            event_type (str): Type of security event (e.g., "AUTH_FAILURE", "RATE_LIMIT")
            user (str): Username involved in the event
            channel (str): Channel where event occurred (use "N/A" if not applicable)
            details (str): Additional details about the event
            
        Example:
            security_auditor.log_security_event(
                "SUSPICIOUS_COMMAND", 
                "user123", 
                "#general", 
                "Attempted to execute admin-only command"
            )
        """
        if not self.security.flags['command_logging']:
            return
        
        log.warning(f"SECURITY EVENT - {event_type}: User {user} in {channel} - {details}")
    
    def log_failed_auth(self, user: str, host: str, reason: str):
        """
        Log failed authentication attempts.
        
        Args:
            user (str): Username that failed authentication
            host (str): Hostname/hostmask of the user
            reason (str): Reason for authentication failure
            
        Example:
            security_auditor.log_failed_auth("fake_admin", "malicious.host.com", "Not in admin list")
        """
        self.log_security_event("AUTH_FAILURE", user, "N/A", f"Host: {host}, Reason: {reason}")
    
    def log_rate_limit_violation(self, user: str, channel: str, command: str):
        """
        Log rate limit violations.
        
        Args:
            user (str): Username that exceeded rate limits
            channel (str): Channel where violation occurred
            command (str): Command that was rate limited
            
        Example:
            security_auditor.log_rate_limit_violation("spammer", "#general", "search")
        """
        self.log_security_event("RATE_LIMIT", user, channel, f"Command: {command}")
    
    def log_input_validation_failure(self, user: str, channel: str, input_data: str, reason: str):
        """
        Log input validation failures (potential attacks).
        
        Args:
            user (str): Username that provided invalid input
            channel (str): Channel where invalid input was provided
            input_data (str): The invalid input (truncated for logging)
            reason (str): Reason validation failed
            
        Example:
            security_auditor.log_input_validation_failure(
                "attacker", 
                "#general", 
                "'; DROP TABLE users; --", 
                "SQL injection attempt"
            )
        """
        # Truncate input data for logging (prevent log spam)
        truncated_input = input_data[:50] + "..." if len(input_data) > 50 else input_data
        self.log_security_event("INPUT_VALIDATION", user, channel, f"Input: {truncated_input}, Reason: {reason}")

# Global instances - Import these in your main bot code
# These are ready-to-use instances of all security components
security_manager = SecurityManager()
input_validator = InputValidator(security_manager)
rate_limiter = RateLimiter(security_manager)
admin_authenticator = AdminAuthenticator(security_manager)
security_auditor = SecurityAuditor(security_manager)

def get_security_manager():
    """
    Get the global security manager instance.
    
    Returns:
        SecurityManager: The global security manager
        
    Example:
        sm = get_security_manager()
        sm.set_flag('rate_limiting', False)
    """
    return security_manager

# Example usage functions for your main bot code:

def secure_command_handler(command: str, args: list, user: str, channel: str, host: str):
    """
    Example function showing how to integrate security checks into command handling.
    
    Args:
        command (str): Command name
        args (list): Command arguments
        user (str): Username
        channel (str): Channel name
        host (str): Full hostname
        
    Returns:
        bool: True if command should proceed, False if blocked
        
    Example integration in main.py:
        if not secure_command_handler(cmd, arguments, username, channel, full_host):
            return  # Command was blocked by security
        # Proceed with normal command execution
    """
    # 1. Validate command arguments
    is_valid, msg = input_validator.validate_command_args(args)
    if not is_valid:
        security_auditor.log_input_validation_failure(user, channel, str(args), msg)
        return False
    
    # 2. Check rate limits
    allowed, msg = rate_limiter.check_rate_limit(user, channel, command)
    if not allowed:
        security_auditor.log_rate_limit_violation(user, channel, command)
        return False
    
    # 3. For admin commands, verify admin privileges
    if command in ['setup', 'logs', 'join', 'leave']:  # Add your admin commands here
        is_admin, msg = admin_authenticator.verify_admin(user, host)
        if not is_admin:
            security_auditor.log_failed_auth(user, host, msg)
            return False
    
    # All checks passed
    return True

def validate_dice_input(dice_notation: str, user: str, channel: str):
    """
    Example function for validating dice roll input.
    
    Args:
        dice_notation (str): Dice notation (e.g., "2d6+3")
        user (str): Username
        channel (str): Channel name
        
    Returns:
        bool: True if valid, False if invalid
        
    Example usage:
        if validate_dice_input(user_input, username, channel):
            # Proceed with dice roll
            pass
    """
    is_valid, msg = input_validator.validate_dice_notation(dice_notation)
    if not is_valid:
        security_auditor.log_input_validation_failure(user, channel, dice_notation, msg)
    return is_valid
