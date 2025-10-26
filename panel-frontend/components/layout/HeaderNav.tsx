"use client";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useAuth } from "../auth/AuthProvider";

// Force client render to avoid any SSR header remnants
const ClientOnly: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <>{children}</>;
};

export function HeaderNav() {
  const { user, loading, logout } = useAuth();

  return (
    <ClientOnly>
      <header className="header-gradient" data-test="header-v2">
        <div className="container flex space-between">
          <Link href="/" className="text-dim" style={{fontWeight:700, letterSpacing:0.3}}>Stralix</Link>
          <nav className="flex gap-18" aria-label="Primary">
            <Link href="/" className="text-dim" prefetch={false}>Home</Link>
            <Link href="/pricing" className="text-dim" prefetch={false}>Pricing</Link>
            <Link href="/features" className="text-dim" prefetch={false}>Features</Link>
            <Link href="/panel" className="btn-ghost" prefetch={false}>Panel</Link>
            {!loading && (
              user ? (
                <div className="flex gap-18">
                  <span title={user.email} className="text-dim" style={{fontSize:14, maxWidth:180, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap"}}>{user.email}</span>
                  <button onClick={logout} className="btn-solid">Logout</button>
                </div>
              ) : (
                <div className="flex gap-18">
                  <Link href="/auth/login" className="text-dim" prefetch={false}>Login</Link>
                  <Link href="/auth/register" className="btn-solid" prefetch={false}>Register</Link>
                </div>
              )
            )}
          </nav>
        </div>
      </header>
    </ClientOnly>
  );
}
