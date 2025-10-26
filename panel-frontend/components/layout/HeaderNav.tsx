"use client";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";

export function HeaderNav() {
  const { user, loading, logout } = useAuth();

  return (
    <header style={{padding:'12px 20px', borderBottom:'1px solid #eee', display:'flex', justifyContent:'space-between'}}>
      <div style={{fontWeight:600}}>Stralix Cloud</div>
      <nav style={{display:'flex', gap:16, alignItems:'center'}}>
        <Link href="/">Home</Link>
        <Link href="/pricing">Pricing</Link>
        <Link href="/features">Features</Link>
        <Link href="/panel">Panel</Link>
        {loading ? null : user ? (
          <>
            <span style={{opacity:.8}}>{user.email}</span>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link href="/auth/login">Login</Link>
            <Link href="/auth/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}
