-- Migration: 002_user_management_system.sql
-- Version: 2.0.0
-- Created: 2025-10-26
-- Description: Comprehensive user management system with roles, 2FA, and security features
-- Author: Development Team

-- ============================================
-- UP MIGRATION
-- ============================================

-- Create user roles enum
CREATE TYPE user_role AS ENUM ('customer', 'staff', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'suspended', 'banned', 'pending_verification');

-- Enhanced users table for hosting platform
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Authentication fields
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- User information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    avatar_url TEXT,
    
    -- Role and status
    role user_role DEFAULT 'customer',
    status user_status DEFAULT 'pending_verification',
    
    -- Email verification
    email_verified BOOLEAN DEFAULT false,
    email_verification_token VARCHAR(255),
    email_verification_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Password reset
    reset_password_token VARCHAR(255),
    reset_password_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Two-Factor Authentication
    twofa_enabled BOOLEAN DEFAULT false,
    twofa_secret VARCHAR(255), -- Encrypted TOTP secret
    twofa_backup_codes TEXT[], -- Encrypted backup codes
    
    -- Security tracking
    last_login_at TIMESTAMP WITH TIME ZONE,
    last_login_ip INET,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    
    -- Audit timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_username CHECK (username IS NULL OR (LENGTH(username) >= 3 AND username ~* '^[a-zA-Z0-9_-]+$')),
    CONSTRAINT valid_phone CHECK (phone_number IS NULL OR phone_number ~* '^\+?[1-9]\d{1,14}$')
);

-- User sessions table for secure session management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Session data
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE,
    
    -- Expiration
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    refresh_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Security info
    user_agent TEXT,
    ip_address INET,
    
    -- Session state
    is_active BOOLEAN DEFAULT true,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Security audit log
CREATE TABLE security_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Event details
    event_type VARCHAR(50) NOT NULL, -- 'login', 'logout', 'failed_login', 'password_reset', 'role_change', etc.
    event_description TEXT,
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    request_id VARCHAR(100),
    
    -- Additional data (JSON)
    metadata JSONB,
    
    -- Severity level
    severity VARCHAR(20) DEFAULT 'info', -- 'info', 'warning', 'critical'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User preferences table (for UI/UX settings)
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    
    -- UI preferences
    theme VARCHAR(20) DEFAULT 'dark', -- 'light', 'dark', 'system'
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Notification preferences
    email_notifications BOOLEAN DEFAULT true,
    security_notifications BOOLEAN DEFAULT true,
    marketing_notifications BOOLEAN DEFAULT false,
    
    -- Other preferences (JSON)
    custom_settings JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username) WHERE username IS NOT NULL;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_last_login ON users(last_login_at);

CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX idx_sessions_active ON user_sessions(is_active, expires_at);

CREATE INDEX idx_audit_user_id ON security_audit_log(user_id);
CREATE INDEX idx_audit_event_type ON security_audit_log(event_type);
CREATE INDEX idx_audit_created_at ON security_audit_log(created_at);
CREATE INDEX idx_audit_severity ON security_audit_log(severity);

-- Update triggers
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to create user preferences on user creation
CREATE OR REPLACE FUNCTION create_user_preferences()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_preferences (user_id) VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER create_user_preferences_trigger
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_user_preferences();

-- Function to log security events
CREATE OR REPLACE FUNCTION log_security_event(
    p_user_id UUID,
    p_event_type VARCHAR(50),
    p_description TEXT DEFAULT NULL,
    p_ip_address INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL,
    p_metadata JSONB DEFAULT NULL,
    p_severity VARCHAR(20) DEFAULT 'info'
)
RETURNS UUID AS $$
DECLARE
    log_id UUID;
BEGIN
    INSERT INTO security_audit_log (
        user_id, event_type, event_description, ip_address, 
        user_agent, metadata, severity
    ) VALUES (
        p_user_id, p_event_type, p_description, p_ip_address,
        p_user_agent, p_metadata, p_severity
    ) RETURNING id INTO log_id;
    
    RETURN log_id;
END;
$$ LANGUAGE plpgsql;

-- Function to clean expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM user_sessions 
    WHERE expires_at < CURRENT_TIMESTAMP 
       OR (refresh_expires_at IS NOT NULL AND refresh_expires_at < CURRENT_TIMESTAMP);
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Record this migration
INSERT INTO schema_migrations (version, description) 
VALUES ('002', 'User management system with roles, 2FA, and comprehensive security features');

-- ============================================
-- DOWN MIGRATION (for rollback)
-- ============================================

-- DROP TRIGGER create_user_preferences_trigger ON users;
-- DROP FUNCTION create_user_preferences();
-- DROP FUNCTION log_security_event(UUID, VARCHAR(50), TEXT, INET, TEXT, JSONB, VARCHAR(20));
-- DROP FUNCTION cleanup_expired_sessions();
-- DROP TABLE user_preferences;
-- DROP TABLE security_audit_log;
-- DROP TABLE user_sessions;
-- DROP TABLE users;
-- DROP TYPE user_status;
-- DROP TYPE user_role;
