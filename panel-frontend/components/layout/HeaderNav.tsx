"use client";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";

export function HeaderNav() {
  const { user, loading, logout } = useAuth();

  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 50,
        background: "linear-gradient(to bottom, rgba(0,0,0,0.6), rgba(0,0,0,0.0))",
        backdropFilter: "saturate(140%) blur(6px)",
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: "0 auto",
          padding: "12px 20px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {/* Brand */}
        <Link
          href="/"
          style={{
            color: "#dbeafe",
            fontWeight: 700,
            letterSpacing: 0.3,
            textDecoration: "none",
          }}
        >
          Stralix
        </Link>

        {/* Nav */}
        <nav
          aria-label="Primary"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
          }}
        >
          <Link href="/" style={linkStyle}>
            Home
          </Link>
          <Link href="/pricing" style={linkStyle}>
            Pricing
          </Link>
          <Link href="/features" style={linkStyle}>
            Features
          </Link>
          <Link href="/panel" style={buttonGhost}>
            Panel
          </Link>

          {!loading && (
            <>
              {user ? (
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span
                    title={user.email}
                    style={{
                      color: "#cbd5e1",
                      fontSize: 14,
                      maxWidth: 180,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {user.email}
                  </span>
                  <button onClick={logout} style={buttonSolid}>
                    Logout
                  </button>
                </div>
              ) : (
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <Link href="/auth/login" style={linkStyle}>
                    Login
                  </Link>
                  <Link href="/auth/register" style={buttonSolid}>
                    Register
                  </Link>
                </div>
              )}
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

const linkStyle: React.CSSProperties = {
  color: "#cbd5e1",
  textDecoration: "none",
};

const buttonSolid: React.CSSProperties = {
  color: "#0b1220",
  background: "linear-gradient(90deg, #7dd3fc, #a78bfa)",
  border: "none",
  borderRadius: 8,
  padding: "8px 14px",
  fontWeight: 600,
  cursor: "pointer",
  textDecoration: "none",
};

const buttonGhost: React.CSSProperties = {
  color: "#dbeafe",
  border: "1px solid rgba(148,163,184,0.3)",
  borderRadius: 8,
  padding: "7px 13px",
  textDecoration: "none",
};
