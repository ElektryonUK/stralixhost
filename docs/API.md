# Stralixhost API Documentation

**Version:** 0.5.0  
**Base URL:** `https://api.stralix.cloud` or `http://localhost:8000` (development)  
**Last Updated:** October 26, 2025

## Table of Contents
- [Authentication](#authentication)
- [Health Check](#health-check)
- [Auth Endpoints](#auth-endpoints)
- [Account Management](#account-management)
- [Session Management](#session-management)
- [User Endpoints](#user-endpoints)
- [Error Responses](#error-responses)
- [Rate Limiting](#rate-limiting)

## Authentication

The API uses Bearer token authentication for protected endpoints. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

**Session Management:** The API supports both Bearer tokens and secure HTTP-only cookies for session management.

## Health Check

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "ok"
}
```

## Auth Endpoints

All auth endpoints are prefixed with `/api/auth`.

### POST /api/auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123",
  "first_name": "John",        // optional
  "last_name": "Doe"           // optional
}
```

**Response (201 Created):**
```json
{
  "message": "Registered. Please verify your email."
}
```

**Validation:**
- `email`: Valid email format required
- `password`: Minimum 8 characters
- `first_name`, `last_name`: Optional strings

### POST /api/auth/login

Authenticate user and create session.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123",
  "totp": "123456"              // optional, required if 2FA enabled
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAi...",
  "refresh_token": "dGhpc2lz...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401`: Invalid credentials
- `400`: TOTP required (when 2FA is enabled)
- `401`: Invalid TOTP

### POST /api/auth/logout

Invalidate current session.

**Headers:** `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
{
  "message": "Logged out"
}
```

### GET /api/auth/me

**⚠️ Status:** Placeholder endpoint (returns 401)

Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

## Account Management

All account endpoints are prefixed with `/api/account`.

### POST /api/account/verify-email

Verify user email address using verification token.

**Request Body:**
```json
{
  "token": "verification_token_here"
}
```

**Response (200 OK):**
```json
{
  "message": "Email verified"
}
```

**Error Response:**
- `400`: Invalid token

### POST /api/account/forgot-password

Request password reset link.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "If the email exists, a reset link has been sent."
}
```

**Note:** Always returns success for security (no user enumeration).

### POST /api/account/reset-password

Reset password using reset token.

**Request Body:**
```json
{
  "token": "reset_token_here",
  "new_password": "newstrongpassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password has been reset"
}
```

**Error Responses:**
- `400`: Invalid or expired token

**Side Effects:**
- All active user sessions are invalidated
- User must log in again

### POST /api/account/2fa/setup

Setup two-factor authentication.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "otpauth_url": "otpauth://totp/Stralix:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Stralix"
}
```

**Usage:**
- Use the `otpauth_url` with QR code generators
- Use the `secret` for manual entry in authenticator apps

### POST /api/account/2fa/verify

Verify and enable two-factor authentication.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "code": "123456"
}
```

**Response (200 OK):**
```json
{
  "message": "2FA enabled"
}
```

**Error Responses:**
- `400`: 2FA not initialized
- `400`: Invalid code

## Session Management

Cookie-based session endpoints prefixed with `/api/auth`.

### POST /api/auth/refresh

Refresh session using refresh token cookie.

**Cookies Required:** `sx_r` (refresh token)

**Response (200 OK):**
```json
{
  "message": "refreshed"
}
```

**Side Effects:**
- Sets new `sx_s` (session) and `sx_r` (refresh) cookies
- Old tokens are invalidated

**Error Responses:**
- `401`: No refresh token
- `401`: Invalid refresh token

### POST /api/auth/logout (Cookie Version)

Logout using cookie-based authentication.

**Cookies:** `sx_s` and/or `sx_r` (optional)

**Response (200 OK):**
```json
{
  "message": "logged out"
}
```

**Side Effects:**
- Invalidates session in database
- Clears authentication cookies

## User Endpoints

User management endpoints prefixed with `/api/users`.

### GET /api/users/me

Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "role": "customer",
  "first_name": "John",
  "last_name": "Doe",
  "email_verified": true,
  "status": "active"
}
```

**User Roles:**
- `customer`: Regular user
- `staff`: Staff member
- `admin`: Administrator

**User Statuses:**
- `pending_verification`: Email not verified
- `active`: Active user
- `suspended`: Suspended account
- `banned`: Banned account

## Error Responses

Standard HTTP status codes are used. Error responses follow this format:

```json
{
  "detail": "Error description"
}
```

**Common Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `422`: Validation Error
- `429`: Too Many Requests (rate limited)
- `500`: Internal Server Error

## Rate Limiting

**Authentication Endpoints:**
- Login attempts: 10 per minute per IP
- Email verification: 10 per minute per IP  
- Password reset: 5 per minute per IP

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

## Security Features

### Session Security
- Sessions bound to IP address and User-Agent (optional)
- Secure, HTTP-only cookies
- Automatic token rotation on refresh
- Session invalidation on password reset

### Password Security
- Bcrypt hashing with salt
- Minimum 8 character requirement
- Secure password reset flow

### 2FA Security
- TOTP-based (Google Authenticator compatible)
- 1-minute validation window
- Secrets stored encrypted (production)

## Development Notes

**Base URLs:**
- Production: `https://api.stralix.cloud`
- Development: `http://localhost:8000`

**CORS:**
- Configured for frontend domains
- Credentials supported for cookie authentication

**Request IDs:**
- Each request gets a unique ID for tracing
- Check `X-Request-ID` header in responses

---

**Maintenance:** This documentation should be updated whenever new endpoints are added or existing ones are modified. See [INSTRUCTIONS.md](../INSTRUCTIONS.md) for guidelines.
