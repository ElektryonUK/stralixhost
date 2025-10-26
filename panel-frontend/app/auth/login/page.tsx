"use client";
import { useState } from "react";

export default function Page() {
  const API = process.env.NEXT_PUBLIC_API_BASE || "";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [totp, setTotp] = useState("");
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const res = await fetch(`${API}/api/auth/login`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, totp: totp || undefined })
    });
    if (res.ok) {
      window.location.href = '/panel';
    } else {
      const msg = await res.json().catch(()=>({detail:'Login failed'}));
      setError(msg.detail || 'Login failed');
    }
  };

  return (
    <section style={{padding:20, maxWidth:480}}>
      <h1>Login</h1>
      <form onSubmit={onSubmit} style={{display:'grid', gap:12}}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
        <input placeholder="TOTP (if enabled)" value={totp} onChange={e=>setTotp(e.target.value)} />
        {error && <p style={{color:'crimson'}}>{error}</p>}
        <button type="submit">Login</button>
      </form>
      <p style={{marginTop:8}}><a href="/auth/forgot-password">Forgot password?</a></p>
    </section>
  );
}
